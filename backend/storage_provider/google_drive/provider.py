from backend.storage_provider.abstract_provider import AbstractStorageProvider


class GoogleDriveProvider(AbstractStorageProvider):

    def authenticate(self, credentials):
        pass

    def upload_chunk(self, file_path, file_name):
        pass

    def download_chunk(self, file_path):
        pass

    def delete_chunk(self, file_path):
        pass

    def get_stats(self):
        pass
