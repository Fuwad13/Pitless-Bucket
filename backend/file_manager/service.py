import asyncio
import json
import os
from typing import Dict, List, Tuple
import uuid
import tempfile

import aiofiles
from fastapi import HTTPException, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from backend.chunk_strategy.strategy import FixedSizeChunkStrategy
from backend.db.models import FileChunk, FileInfo, StorageProvider
from backend.storage_provider.abstract_provider import AbstractStorageProvider
from backend.log.logger import get_logger
from backend.storage_provider.factory import get_provider

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


class FileManagerService:

    def upload_file(self, session: AsyncSession, file: UploadFile, user_id: str):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                content = file.file.read()
                temp_file_path = temp_file.name

            # TODO : implement chunk strategy selection here later
            # get the info of the user's linked storage providers
            # select a chunk distribution strategy based on the user's avaiable storage or filetype etc.

            chunk_strat = fixed_size_chunk_strategy  # TODO :  use Strategy pattern to select chunk strategy
            chunk_paths = chunk_strat.split_file(temp_file_path)
            uploaded_chunks = []
            stmt = select(StorageProvider).where(
                StorageProvider.user_id == uuid.UUID(user_id)
            )
            results = asyncio.run(session.exec(stmt))
            storage_providers: List[Tuple[str, AbstractStorageProvider]] = []
            for res in results:
                storage_provider = get_provider(
                    res.provider_name, credentials=json.loads(res.creds)
                )
                storage_providers.append((str(res.uid), storage_provider))

            for idx, chunk_path in enumerate(chunk_paths):

                chunk_name = f"{file.filename}.part{idx+1:03d}"
                file_metadata = {"name": chunk_name}
                # TODO : implement a strategy to select the storage provider
                storage_provider_id, storage_provider = storage_providers[
                    idx % len(storage_providers)
                ]  # round robin

                storage_provider.upload_chunk(chunk_path, file_metadata)
                uploaded_chunks.append(
                    {
                        "original_filename": file.filename,
                        "chunk_number": idx + 1,
                        "chunk_name": chunk_name,
                        "storage_provider": storage_provider.__class__.__name__,
                        "prodiver_file_id": "TODO",
                        "provider_id": storage_provider_id,
                        "size": os.path.getsize(chunk_path),
                    }
                )

            file_extension = (
                file.filename.split(".")[-1] if "." in file.filename else "unknown"
            )
            file_ = FileInfo(
                user_id=uuid.UUID(user_id),
                file_name=file.filename,
                content_type=file.content_type,
                extension=file_extension,
                size=file.size,
            )
            session.add(file_)
            asyncio.run(session.commit())
            asyncio.run(session.refresh(file_))
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
            asyncio.run(session.commit())

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
            logger.error(f"Error in upload_file: {e}")
            if "temp_file_path" in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if "chunk_paths" in locals():
                for chunk_path in chunk_paths:
                    if os.path.exists(chunk_path):
                        os.remove(chunk_path)
            raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    async def download_file(self, session: AsyncSession, file_id: str, user_id: str):
        pass

    async def delete_file(self, session: AsyncSession, file_id: str, user_id: str):
        pass

    async def rename_file(
        self, session: AsyncSession, file_id: str, user_id: str, new_name: str
    ):
        pass

    async def list_files(self, session: AsyncSession, user_id: str):
        pass

    async def create_folder(
        self, session: AsyncSession, folder_name: str, user_id: str
    ):
        pass

    async def delete_folder(self, session: AsyncSession, folder_id: str, user_id: str):
        pass

    async def rename_folder(
        self, session: AsyncSession, folder_id: str, user_id: str, new_name: str
    ):
        pass

    async def move_file(
        self, session: AsyncSession, file_id: str, user_id: str, new_folder_id: str
    ):
        pass

    async def move_folder(
        self, session: AsyncSession, folder_id: str, user_id: str, new_folder_id: str
    ):
        pass
