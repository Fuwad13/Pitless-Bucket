from abc import ABC, abstractmethod
from storage_provider.google_drive.provider import GoogleDriveProvider
from storage_provider.onedrive.provider import OneDriveProvider
from storage_provider.dropbox.provider import DropBoxProvider


class StorageProviderFactory(ABC):
    @abstractmethod
    def create_provider(self, provider_name: str):
        pass


class GoogleDriveProviderFactory(StorageProviderFactory):
    def create_provider(self):
        return GoogleDriveProvider()


class OneDriveProviderFactory(StorageProviderFactory):
    def create_provider(self):
        return OneDriveProvider()


class DropBoxProviderFactory(StorageProviderFactory):
    def create_provider(self):
        return DropBoxProvider()
