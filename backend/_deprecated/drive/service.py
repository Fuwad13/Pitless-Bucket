import json
import uuid
import asyncio
import aiofiles
from pathlib import Path
from typing import List, Tuple
from googleapiclient.discovery import build, Resource
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from backend.db.models import FileInfo, FileChunk, StorageProvider, User
from backend.drive.schemas import FileInfoModel, FileChunkModel, GoogleDriveModel
from backend.auth.schemas import UserModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from backend.log.logger import get_logger

logger = get_logger(__name__, Path(__file__).parent.parent / "log" / "app.log")


class DriveService:
    async def get_files_by_user_id(
        self, session: AsyncSession, user_id: str
    ) -> List[FileInfoModel]:
        stmt = select(FileInfo).where(FileInfo.user_id == uuid.UUID(user_id))
        result = await session.exec(stmt)
        return result.all()

    async def async_split_file(
        self, input_file_path: str, chunk_size: int = 100 * 1024 * 1024
    ) -> List[str]:
        """
        Split a file into chunks of specified size (default: 100MB).
        Returns a list of chunk file paths.
        """
        chunk_paths = []
        part_num = 1

        async with aiofiles.open(input_file_path, "rb") as f:
            while True:
                chunk = await f.read(chunk_size)
                if not chunk:
                    break

                chunk_name = f"{input_file_path}.part{part_num}"
                async with aiofiles.open(chunk_name, "wb") as chunk_file:
                    await chunk_file.write(chunk)

                chunk_paths.append(chunk_name)
                part_num += 1

        return chunk_paths

    def get_api_service(
        self, api: str, version: str, credentials: str
    ) -> Tuple[Resource, Credentials]:
        creds = Credentials.from_authorized_user_info(json.loads(credentials))
        # logger.debug(f"Credentials: {creds}")
        # logger.debug(f"{creds.token}")
        return build(api, version, credentials=creds), creds

    async def async_get_api_service(
        self, api: str, version: str, credentials: str
    ) -> Tuple[Resource, Credentials]:
        return await asyncio.to_thread(self.get_api_service, api, version, credentials)

    async def async_get_api_service_by_email(
        self, session: AsyncSession, api: str, version: str, email: str
    ) -> Tuple[Resource, Credentials]:
        stmt = select(GoogleDrive).where(GoogleDrive.email == email)
        result = await session.exec(stmt)
        gdrive = result.first()
        return await self.async_get_api_service("drive", "v3", gdrive.creds)

    def upload_file(
        self, gdrive_service: Resource, media: MediaFileUpload, fields: str, **kwargs
    ):
        return (
            gdrive_service.files()
            .create(media_body=media, fields=fields, **kwargs)
            .execute()
        )

    async def async_upload_file(
        self, gdrive_service: Resource, media: MediaFileUpload, fields: str, **kwargs
    ):
        return await asyncio.to_thread(
            self.upload_file, gdrive_service, media, fields, **kwargs
        )

    def delete_file(self, gdrive_service: Resource, file_id: str):
        return gdrive_service.files().delete(fileId=file_id).execute()

    async def async_delete_file(self, gdrive_service: Resource, file_id: str):
        return await asyncio.to_thread(self.delete_file, gdrive_service, file_id)

    async def get_creds_by_gmail(self, session: AsyncSession, email: str) -> str:
        stmt = select(GoogleDrive).where(GoogleDrive.email == email)
        result = await session.exec(stmt)
        gdrive = result.first()
        return gdrive.creds
