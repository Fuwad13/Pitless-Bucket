import asyncio
import os
from typing import List
import uuid
import tempfile

import aiofiles
from fastapi import UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from backend.chunk_strategy.fixed_size_chunk_strategy import FixedSizeChunkStrategy
from backend.db.models import StorageProvider


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

            chunk_strat = fixed_size_chunk_strategy  # TODO :  use Abstract Factory pattern to select chunk strategy
            chunk_paths = chunk_strat.split_file(temp_file_path)
            uploaded_chunks = []
            stmt = select(StorageProvider).where(
                StorageProvider.user_id == uuid.UUID(user_id)
            )
            result = asyncio.run(session.exec(stmt))
            accounts = []
            for storage_provider in result:
                #  get the storage provider service
                storage_provider_service, _ = await drive_service.async_get_api_service(
                    "drive", "v3", drive.creds
                )
                accounts.append(
                    {
                        "account": mail_addr,
                        "creds": drive.creds,
                        "drive_service": gdrive_service,
                    }
                )

            current_account_idx = 0
            for idx, chunk_path in enumerate(chunk_paths):
                account = accounts[current_account_idx % len(accounts)]
                # TODO : handle this in a better way
                # Refresh token if needed
                # if not creds.valid:
                #     creds.refresh(Request())

                # Upload chunk
                chunk_name = f"{file.filename}.part{idx+1:03d}"
                file_metadata = {"name": chunk_name}
                media = MediaFileUpload(chunk_path, mimetype="application/octet-stream")

                drive_file = await drive_service.async_upload_file(
                    account["drive_service"], media, "id, size", body=file_metadata
                )
                uploaded_chunks.append(
                    {
                        "original_filename": file.filename,
                        "chunk_number": idx + 1,
                        "chunk_name": chunk_name,
                        "drive_account": account["account"],
                        "drive_file_id": drive_file["id"],
                        "size": int(drive_file["size"]),
                    }
                )
                media._fd.close()
                current_account_idx += 1

            # TODO : currently hardcoded user_id
            file_extension = (
                file.filename.split(".")[-1] if "." in file.filename else "unknown"
            )
            file_ = FileInfo(
                user_id=test_user_id,
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
                    drive_file_id=chunk["drive_file_id"],
                    drive_account=chunk["drive_account"],
                    size=chunk["size"],
                )
                session.add(chunk_to_add)
            await session.commit()

            await asyncio.to_thread(os.remove, temp_file_path)
            for chunk_path in chunk_paths:
                await asyncio.to_thread(os.remove, chunk_path)

            return {
                "message": "File uploaded successfully",
                "filename": file.filename,
                "total_chunks": len(chunk_paths),
                "chunks": uploaded_chunks,
            }

        except Exception as e:
            logger.error(f"Error in upload_file: {e}")
            if "temp_file_path" in locals() and os.path.exists(temp_file_path):
                await asyncio.to_thread(os.remove, temp_file_path)
            if "chunk_paths" in locals():
                for chunk_path in chunk_paths:
                    if os.path.exists(chunk_path):
                        await asyncio.to_thread(os.remove, chunk_path)
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
