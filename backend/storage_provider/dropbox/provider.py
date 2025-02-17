from typing import Dict
import dropbox
from backend.storage_provider.abstract_provider import AbstractStorageProvider
from .utils import get_valid_dropbox_token


class DropBoxProvider(AbstractStorageProvider):

    def __init__(self, credentials):
        super().__init__(credentials)
        self.access_token = get_valid_dropbox_token(credentials)

    def authenticate(self, credentials: dict):
        self.access_token = get_valid_dropbox_token(credentials)

    def upload_chunk(self, file_path, file_name):
        dbx = dropbox.Dropbox(self.access_token)
        with open(file_path, "rb") as f:
            data = f.read()
        result = dbx.files_upload(data, f"/{file_name}")
        return str(result.id)

    def download_chunk(self) -> str:
        pass

    def delete_chunk(self):
        pass

    def get_stats(self) -> Dict:
        pass
