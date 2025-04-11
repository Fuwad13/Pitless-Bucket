import asyncio
import json
import os
import time
from typing import Dict, List, Optional, Tuple
import uuid
import tempfile
from pathlib import Path

import aiofiles
from redis import asyncio as aioredis
from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from backend.chunk_strategy.strategy import FixedSizeChunkStrategy
from backend.db.models import FileChunk, FileInfo, StorageProvider
from backend.storage_provider.abstract_provider import AbstractStorageProvider
from backend.log.logger import get_logger
from backend.storage_provider.factory import get_provider
from .schemas import UploadFileResponse

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")


fixed_size_chunk_strategy = FixedSizeChunkStrategy()

CHUNK_SIZE = 1024 * 1024 * 5


class FileManagerService:

    async def upload_file(
        self, session: AsyncSession, redis_client: aioredis.Redis, file: UploadFile, firebase_uid: str
    ) -> UploadFileResponse:
        """
        Upload a file to the User's storage
        Args:
            session (AsyncSession): Async database session
            redis_client (aioredis.Redis): Redis cache client
            file (UploadFile): File to be uploaded
            firebase_uid (str): Firebase UID of the User
        Returns:
            dict: Response message
        """
        try:
            temp_file_path = await self.save_to_temp_file(file)
            # TODO: implement chunk strategy selection here later
            # Get the info of the user's linked storage providers and select a distribution strategy
            chunk_strat = fixed_size_chunk_strategy  # TODO: use Strategy pattern to select chunk strategy

            loop = asyncio.get_event_loop()
            chunk_paths = await loop.run_in_executor(
                None, chunk_strat.split_file, temp_file_path
            )
            storage_providers = await self.get_storage_providers(session, firebase_uid)
            if len(storage_providers) == 0:
                raise HTTPException(
                    status_code=400, detail="No storage providers linked"
                )

            uploaded_chunks = await self._upload_chunks(
                session, file.filename, chunk_paths, storage_providers
            )

            file_ = self._extract_file_metadata(
                file.filename, file.content_type, file.size, firebase_uid
            )
            session.add(file_)
            await session.commit()
            await session.refresh(file_)
            await redis_client.delete(f"files:{firebase_uid}")
            await redis_client.delete(f"storage_usage:{firebase_uid}")
            await self._persist_file_chunks(session, file_, uploaded_chunks)
            self._cleanup_temp_files(temp_file_path, chunk_paths)

            response = UploadFileResponse(**file_.model_dump())
            return response

        except Exception as e:
            logger.error(f"Error in upload_file: {e}")
            await session.rollback()
            if "temp_file_path" in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if "chunk_paths" in locals():
                for chunk_path in chunk_paths:
                    if os.path.exists(chunk_path):
                        os.remove(chunk_path)
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    async def save_to_temp_file(self, file: UploadFile) -> str:
        """
        Save the uploaded file to a temporary file
        Args:
            file (UploadFile): File to be saved
        Returns:
            str: Path to the temporary file
        """
        async with aiofiles.tempfile.NamedTemporaryFile(
            "wb", delete=False
        ) as temp_file:
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break
                await temp_file.write(chunk)
            return temp_file.name

    async def get_storage_providers(
        self, session: AsyncSession, firebase_uid: str
    ) -> List[Tuple[str, AbstractStorageProvider]]:
        """
        Get the storage providers linked to the User
        Args:
            session (AsyncSession): Async database session
            firebase_uid (str): Firebase UID of the User
        Returns:
            List[Tuple[str, AbstractStorageProvider]]: List of tuples containing the storage provider ID and the provider object
        """
        stmt = select(StorageProvider).where(
            StorageProvider.firebase_uid == firebase_uid
        )
        results = await session.exec(stmt)
        storage_providers = []
        for res in results:
            storage_provider = get_provider(
                res.provider_name, credentials=json.loads(res.creds)
            )
            storage_providers.append((str(res.uid), storage_provider))
        return storage_providers

    async def _upload_chunks(
        self,
        session: AsyncSession,
        filename: str,
        chunk_paths: List[str],
        storage_providers: List[Tuple[str, AbstractStorageProvider]],
    ) -> List[Dict]:
        """
        Upload the chunks to the storage providers
        Args:
            session (AsyncSession): Async database session
            filename (str): Name of the file
            chunk_paths (List[str]): List of paths to the chunks
            storage_providers (List[Tuple[str, AbstractStorageProvider]]): List of tuples containing the storage provider ID and the provider object
        Returns:
            List[Dict]: List of dictionaries containing the uploaded chunk details
        """
        uploaded_chunks = []
        for idx, chunk_path in enumerate(chunk_paths):
            chunk_name = f"{filename}_{int(time.time())}.part{idx+1:03d}"

            # TODO :Select storage provider based on strategy
            storage_provider_id, storage_provider = storage_providers[
                idx % len(storage_providers)
            ]

            chunk_id_in_provider = await asyncio.to_thread(
                storage_provider.upload_chunk, chunk_path, chunk_name
            )
            uploaded_chunks.append(
                {
                    "chunk_number": idx + 1,
                    "chunk_name": chunk_name,
                    "provider_file_id": chunk_id_in_provider,
                    "provider_id": storage_provider_id,
                    "size": os.path.getsize(chunk_path),
                }
            )

        return uploaded_chunks

    def _extract_file_metadata(
        self, filename: str, content_type: str, size: int, firebase_uid: str
    ) -> FileInfo:
        """
        Extract the file metadata and create a FileInfo object
        Args:
            filename (str): Name of the file
            content_type (str): Content type of the file
            size (int): Size of the file
            firebase_uid (str): Firebase UID of the User
        Returns:
            FileInfo: FileInfo object
        """
        file_extension = filename.split(".")[-1] if "." in filename else "unknown"
        return FileInfo(
            firebase_uid=firebase_uid,
            file_name=filename,
            content_type=content_type,
            extension=file_extension,
            size=size,
        )

    async def _persist_file_chunks(
        self, session: AsyncSession, file: FileInfo, uploaded_chunks: List[Dict]
    ):
        """
        Persist/Save the file chunks information to the database
        Args:
            session (AsyncSession): Async database session
            file (FileInfo): FileInfo object
            uploaded_chunks (List[Dict]): List of dictionaries containing the uploaded chunk details
        """
        for chunk in uploaded_chunks:
            chunk_to_add = FileChunk(
                file_id=file.uid,
                chunk_name=chunk["chunk_name"],
                chunk_number=chunk["chunk_number"],
                provider_file_id=chunk["provider_file_id"],
                provider_id=uuid.UUID(chunk["provider_id"]),
                size=chunk["size"],
            )
            session.add(chunk_to_add)
        await session.commit()

    def _cleanup_temp_files(self, temp_file_path: str, chunk_paths: List[str]):
        """Helper method to clean up temporary files"""
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        if chunk_paths:
            for chunk_path in chunk_paths:
                if os.path.exists(chunk_path):
                    os.remove(chunk_path)

    async def delete_file(self, session: AsyncSession, file_id: str, firebase_uid: str):
        """
        Delete a file from the User's storage (by file_id)
        Args:
            session (AsyncSession): Async database session
            file_id (str): File ID
            firebase_uid (str): Firebase UID of the User
        Returns:
            dict: Response message

        """
        try:
            stmt = select(FileInfo).where(FileInfo.uid == file_id)
            result = (await session.exec(stmt)).first()
            if not result:
                raise HTTPException(status_code=404, detail="File not found")
            if result.firebase_uid != firebase_uid:
                raise HTTPException(status_code=403, detail="Unauthorized")

            stmt = select(FileChunk).where(FileChunk.file_id == file_id)
            chunks = await session.exec(stmt)

            for chunk in chunks:
                stmt = select(StorageProvider).where(
                    StorageProvider.uid == chunk.provider_id
                )
                res_sp = (await session.exec(stmt)).first()
                provider = get_provider(
                    res_sp.provider_name,
                    credentials=json.loads(res_sp.creds),
                )
                await asyncio.to_thread(provider.delete_chunk, chunk.provider_file_id)
            await session.delete(result)
            await session.commit()
            return {"message": f"{result.file_name} deleted successfully"}

        except Exception as e:
            await session.rollback()
            logger.error(f"Error in delete_file: {e}")
            raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")

    async def rename_file(
        self, session: AsyncSession, file_id: str, firebase_uid: str, new_name: str
    ):
        """
        Rename a file in the User's storage
        Args:
            session (AsyncSession): Async database session
            file_id (str): File ID
            firebase_uid (str): Firebase UID of the User
            new_name (str): New name for the file
        Returns:
            dict: Response message
        """
        try:
            stmt = select(FileInfo).where(FileInfo.uid == file_id)
            result = (await session.exec(stmt)).first()
            if not result:
                raise HTTPException(status_code=404, detail="File not found")
            if result.firebase_uid != firebase_uid:
                raise HTTPException(status_code=403, detail="Unauthorized")

            result.file_name = new_name
            await session.commit()
            return {"message": "File renamed successfully"}

        except Exception as e:
            await session.rollback()
            logger.error(f"Error in rename_file: {e}")
            raise HTTPException(status_code=500, detail=f"Rename failed: {str(e)}")

    async def list_files(self, session: AsyncSession, redis_client : aioredis.Redis, firebase_uid: str):
        """
        List all files in the User's storage
        Args:
            session (AsyncSession): Async database session
            redis_client (aioredis.Redis): Redis cache client
            firebase_uid (str): Firebase UID of the User
        Returns:
            List[FileInfo]: List of FileInfo objects
        """
        cached = await self.get_cached_files(redis_client, firebase_uid)
        if cached:
            cached_files = json.loads(cached)
            return [FileInfo(**file) for file in cached_files]
        stmt = select(FileInfo).where(FileInfo.firebase_uid == firebase_uid)
        result = (await session.exec(stmt)).all()
        await self.set_cached_files(redis_client, firebase_uid, result)
        return result
    
    async def get_cached_files(self, redis_client: aioredis.Redis, firebase_uid: str):
        """
        Get cached files from Redis
        Args:
            redis_client (aioredis.Redis): Redis cache client
            firebase_uid (str): Firebase UID of the User
        Returns:
            Optional[List[FileInfo]]: List of cached FileInfo objects or None if not found
        """
        key = f"files:{firebase_uid}"
        return await redis_client.get(key)
    
    async def set_cached_files(self, redis_client: aioredis.Redis, firebase_uid: str, files: List[FileInfo]):
        """
        Set cached files in Redis
        Args:
            redis_client (aioredis.Redis): Redis cache client
            firebase_uid (str): Firebase UID of the User
            files (List[FileInfo]): List of FileInfo objects to cache
        """
        key = f"files:{firebase_uid}"
        await redis_client.set(key, json.dumps([file.model_dump(mode='json') for file in files]), ex=600)

    async def download_file(
        self, session: AsyncSession, file_id: str, firebase_uid: str
    ):
        """
        Download a file from the User's storage
        Args:
            session (AsyncSession): Async database session
            file_id (str): File ID
            firebase_uid (str): Firebase UID of the User
        Returns:
            FileResponse: FileResponse object
        """
        try:
            stmt = select(FileInfo).where(FileInfo.uid == file_id)
            result = (await session.exec(stmt)).first()
            if not result:
                raise HTTPException(status_code=404, detail="File not found")
            if result.firebase_uid != firebase_uid:
                raise HTTPException(status_code=403, detail="Unauthorized")

            stmt = select(FileChunk).where(FileChunk.file_id == file_id)
            chunks = await session.exec(stmt)
            if not chunks:
                raise HTTPException(status_code=404, detail="File Chunks not found")
            async with aiofiles.tempfile.NamedTemporaryFile(
                "wb", delete=False, delete_on_close=True
            ) as temp_file:
                for chunk in chunks:
                    stmt = select(StorageProvider).where(
                        StorageProvider.uid == chunk.provider_id
                    )
                    res_sp = (await session.exec(stmt)).first()
                    provider = get_provider(
                        res_sp.provider_name,
                        credentials=json.loads(res_sp.creds),
                    )
                    chunk_path = await asyncio.to_thread(
                        provider.download_chunk, chunk.provider_file_id
                    )
                    async with aiofiles.open(chunk_path, "rb") as f:
                        await temp_file.write(await f.read())
                    os.remove(chunk_path)
                return FileResponse(
                    temp_file.name,
                    headers={
                        "Content-Disposition": f'attachment; filename="{result.file_name}"',
                        "Content-Type": result.content_type,
                        "Content-Length": str(result.size),
                    },
                )

        except Exception as e:
            logger.error(f"Error in download_file: {e}")
            raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")

    async def create_folder(
        self, session: AsyncSession, folder_name: str, firebase_uid: str
    ):
        pass

    async def delete_folder(
        self, session: AsyncSession, folder_id: str, firebase_uid: str
    ):
        pass

    async def rename_folder(
        self, session: AsyncSession, folder_id: str, firebase_uid: str, new_name: str
    ):
        pass

    async def move_file(
        self, session: AsyncSession, file_id: str, firebase_uid: str, new_folder_id: str
    ):
        pass

    async def move_folder(
        self,
        session: AsyncSession,
        folder_id: str,
        firebase_uid: str,
        new_folder_id: str,
    ):
        pass

    async def get_storage_usage(self, session: AsyncSession, redis_client: aioredis.Redis, firebase_uid: str) -> Dict:
        """
        Get the storage usage of the User
        Args:
            session (AsyncSession): Async database session
            firebase_uid (str): Firebase UID of the User
        Returns:
            Dict: Dictionary containing the storage usage details
        """
        cached = await self.get_cached_storage_usage(redis_client, firebase_uid)
        if cached:
            return json.loads(cached)
        
        stmt = select(StorageProvider).where(
            StorageProvider.firebase_uid == firebase_uid
        )
        results = await session.exec(stmt)
        if not results:
            raise HTTPException(status_code=400, detail="No storage providers linked")
        usage = {
            "used": 0,
            "available": 0,
            "total": 0,
        }
        for res in results:
            storage_provider = get_provider(
                res.provider_name, credentials=json.loads(res.creds)
            )
            stat_dict = await asyncio.to_thread(storage_provider.get_stats)
            usage["used"] += stat_dict["used"]
            usage["available"] += stat_dict["available"]
            usage["total"] += stat_dict["total"]
        await self.set_cached_storage_usage(redis_client, firebase_uid, usage)
        return usage
    
    async def get_cached_storage_usage(self, redis_client: aioredis.Redis, firebase_uid: str):
        """
        Get cached storage usage from Redis
        Args:
            redis_client (aioredis.Redis): Redis cache client
            firebase_uid (str): Firebase UID of the User
        """
        key = f"storage_usage:{firebase_uid}"
        return await redis_client.get(key)
    
    async def set_cached_storage_usage(self, redis_client: aioredis.Redis, firebase_uid: str, usage: Dict):
        """
        Set cached storage usage in Redis
        Args:
            redis_client (aioredis.Redis): Redis cache client
            firebase_uid (str): Firebase UID of the User
            usage (Dict): Dictionary containing the storage usage details
        """
        key = f"storage_usage:{firebase_uid}"
        await redis_client.set(key, json.dumps(usage), ex=600)

    async def sync_storage_stats(self, session: AsyncSession, firebase_uid: str):
        pass

    async def add_new_storage_provider(
        self,
        session: AsyncSession,
        provider_name: str,
        credentials: Dict,
        firebase_uid: str,
    ):
        pass


class MetaDataManagerService:

    async def save_file_metadata(self):
        pass

    async def get_file_metadata(self):
        pass

    async def delete_file_metadata(self):
        pass

    async def update_file_metadata(self):
        pass

    async def save_chunk_metadata(self):
        pass

    async def get_chunk_metadata(self):
        pass

    async def delete_chunk_metadata(self):
        pass

    async def update_chunk_metadata(self):
        pass


metadata_manager_service = MetaDataManagerService()
