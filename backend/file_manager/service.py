import asyncio
import json
import os
import time
from typing import Dict, List, Tuple
import uuid
import tempfile
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from backend.chunk_strategy.strategy import FixedSizeChunkStrategy
from backend.db.models import FileChunk, FileInfo, StorageProvider
from backend.storage_provider.abstract_provider import AbstractStorageProvider
from backend.log.logger import get_logger
from backend.storage_provider.factory import get_provider
from .schemas import FileInfoResponseModel

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")


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


fixed_size_chunk_strategy = FixedSizeChunkStrategy()
metadata_manager_service = MetaDataManagerService()

CHUNK_SIZE = 1024 * 1024 * 5


class FileManagerService:

    async def upload_file(
        self, session: AsyncSession, file: UploadFile, firebase_uid: str
    ):
        try:
            temp_file_path = await self.save_to_temp_file(file)
            # TODO: implement chunk strategy selection here later
            # Get the info of the user's linked storage providers and select a distribution strategy
            chunk_strat = fixed_size_chunk_strategy  # TODO: use Strategy pattern to select chunk strategy

            loop = asyncio.get_event_loop()
            chunk_paths = await loop.run_in_executor(
                None, chunk_strat.split_file, temp_file_path
            )
            uploaded_chunks = []

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

            if len(storage_providers) == 0:
                raise HTTPException(
                    status_code=400, detail="No storage providers linked"
                )
            logger.debug(f"Storage providers: {storage_providers}")

            for idx, chunk_path in enumerate(chunk_paths):
                chunk_name = f"{file.filename}_{int(time.time())}.part{idx+1:03d}"
                # TODO: implement a strategy to select the storage provider
                storage_provider_id, storage_provider = storage_providers[
                    idx % len(storage_providers)
                ]

                chunk_id_in_provider = await asyncio.to_thread(
                    storage_provider.upload_chunk, chunk_path, chunk_name
                )
                uploaded_chunks.append(
                    {
                        "original_filename": file.filename,
                        "chunk_number": idx + 1,
                        "chunk_name": chunk_name,
                        "storage_provider": storage_provider.__class__.__name__,
                        "provider_file_id": chunk_id_in_provider,
                        "provider_id": storage_provider_id,
                        "size": os.path.getsize(chunk_path),
                    }
                )

            file_extension = (
                file.filename.split(".")[-1] if "." in file.filename else "unknown"
            )
            file_ = FileInfo(
                firebase_uid=firebase_uid,
                file_name=file.filename,
                content_type=file.content_type,
                extension=file_extension,
                size=file.size,
            )
            session.add(file_)
            await session.commit()
            await session.refresh(file_)

            for chunk in uploaded_chunks:
                chunk_to_add = FileChunk(
                    file_id=file_.uid,
                    chunk_name=chunk["chunk_name"],
                    chunk_number=chunk["chunk_number"],
                    provider_file_id=chunk["provider_file_id"],
                    provider_id=uuid.UUID(chunk["provider_id"]),
                    size=chunk["size"],
                )
                session.add(chunk_to_add)
            await session.commit()

            # Clean up temporary files
            os.remove(temp_file_path)
            for chunk_path in chunk_paths:
                os.remove(chunk_path)

            return {
                "message": "File uploaded successfully",
                "filename": file.filename,
                "total_chunks": len(chunk_paths),
                "chunks": uploaded_chunks,
            }

        except Exception as e:
            await session.rollback()
            logger.error(f"Error in upload_file: {e}")
            if "temp_file_path" in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if "chunk_paths" in locals():
                for chunk_path in chunk_paths:
                    if os.path.exists(chunk_path):
                        os.remove(chunk_path)
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    async def save_to_temp_file(self, file: UploadFile) -> str:
        logger.debug(dir(file))
        async with aiofiles.tempfile.NamedTemporaryFile(
            "wb", delete=False
        ) as temp_file:
            while True:
                chunk = await file.read(CHUNK_SIZE)
                if not chunk:
                    break
                await temp_file.write(chunk)
            return temp_file.name

    async def delete_file(self, session: AsyncSession, file_id: str, firebase_uid: str):
        """Delete a file uploaded by User"""
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

    async def list_files(self, session: AsyncSession, firebase_uid: str):
        stmt = select(FileInfo).where(FileInfo.firebase_uid == firebase_uid)
        result = await session.exec(stmt)
        return result.all()

    async def download_file(
        self, session: AsyncSession, file_id: str, firebase_uid: str
    ):
        pass

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

    async def get_storage_usage(self, session: AsyncSession, firebase_uid: str) -> Dict:
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
        return usage

    async def sync_storage_stats(self, session: AsyncSession, firebase_uid: str):
        stmt = select(StorageProvider).where(
            StorageProvider.firebase_uid == firebase_uid
        )
        results = await session.exec(stmt)
        storage_providers = []
        for res in results:
            storage_provider = get_provider(
                res.provider_name, credentials=json.loads(res.creds)
            )
            stat_dict = await asyncio.to_thread(storage_provider.get_stats)
            logger.debug(
                f"Stats for {storage_provider.__class__.__name__}: {stat_dict}"
            )
            storage_providers.append((str(res.uid), storage_provider))

    async def add_new_storage_provider(
        self,
        session: AsyncSession,
        provider_name: str,
        credentials: Dict,
        firebase_uid: str,
    ):
        pass
