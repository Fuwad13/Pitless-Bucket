from pathlib import Path
import tempfile
from backend.storage_provider.abstract_provider import AbstractStorageProvider
from googleapiclient.discovery import build, Resource
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload
from backend.log.logger import get_logger
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request


logger = get_logger(__name__, Path(__file__).parent.parent.parent / "log" / "app.log")


class GoogleDriveProvider(AbstractStorageProvider):

    def __init__(self, credentials):
        super().__init__(credentials)
        self.drive_service: Resource = self.authenticate(credentials)

    def authenticate(self, credentials) -> Resource:
        creds = Credentials.from_authorized_user_info(credentials)
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise ValueError("Invalid credentials")

        return build("drive", "v3", credentials=creds)

    def upload_chunk(self, file_path, file_name):
        media = MediaFileUpload(file_path, mimetype="application/octet-stream")
        drive_file = (
            self.drive_service.files()
            .create(media_body=media, fields="id", body={"name": file_name})
            .execute()
        )
        logger.debug(f"Uploaded chunk: {file_name} -> drive id: {drive_file['id']}")
        return drive_file["id"]

    def download_chunk(self, file_id):
        request = self.drive_service.files().get_media(fileId=file_id)
        with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
            downloader = MediaIoBaseDownload(tmp, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            return tmp.name

    def delete_chunk(self, file_id):
        self.drive_service.files().delete(fileId=file_id).execute()

    def get_stats(self):
        about = self.drive_service.about().get(fields="storageQuota").execute()
        used = int(about["storageQuota"]["usageInDrive"]) + int(
            about["storageQuota"]["usageInDriveTrash"]
        )
        total = int(about["storageQuota"]["limit"])
        available = total - used
        return {"used": used, "available": available, "total": total}
