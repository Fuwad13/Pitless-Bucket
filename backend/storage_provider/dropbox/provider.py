import tempfile
from pathlib import Path
from typing import Dict

import dropbox

from backend.log.logger import get_logger
from backend.storage_provider.abstract_provider import AbstractStorageProvider

from .utils import get_valid_dropbox_token

logger = get_logger(__name__, Path(__file__).parent.parent.parent / "log" / "app.log")


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
        logger.debug(f"Uploaded chunk: {file_name} -> dropbox id: {result.id}")
        return str(result.id)

    def download_chunk(self, file_id) -> str:
        dbx = dropbox.Dropbox(self.access_token)
        metadata = dbx.files_get_metadata(file_id)
        file_path = metadata.path_lower
        with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
            dbx.files_download_to_file(tmp.name, file_path)
            return tmp.name

    def delete_chunk(self, file_id):
        dbx = dropbox.Dropbox(self.access_token)
        metadata = dbx.files_get_metadata(file_id)
        dbx.files_delete_v2(metadata.path_lower)

    def get_stats(self) -> Dict:
        dbx = dropbox.Dropbox(self.access_token)
        space_usage = dbx.users_get_space_usage()
        used = space_usage.used
        total = space_usage.allocation.get_individual().allocated
        available = total - used
        return {"used": used, "available": available, "total": total}
