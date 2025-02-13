from abc import ABC, abstractmethod


class StorageProviderBase(ABC):
    @abstractmethod
    def upload_chunk(self, file_path: str, file_name: str) -> str:
        pass

    @abstractmethod
    def download_file(self, file_path: str) -> str:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass

    @abstractmethod
    def list_files(self, folder_path: str) -> list:
        pass

    @abstractmethod
    def create_folder(self, folder_path: str) -> None:
        pass

    @abstractmethod
    def delete_folder(self, folder_path: str) -> None:
        pass
