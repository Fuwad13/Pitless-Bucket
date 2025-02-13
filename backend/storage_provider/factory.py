from abc import ABC, abstractmethod
from backend.storage_provider.google_drive.provider import GoogleDriveProvider
from backend.storage_provider.onedrive.provider import OneDriveProvider
from backend.storage_provider.dropbox.provider import DropBoxProvider


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


FACTORY_REGISTRY = {
    "google_drive": GoogleDriveProviderFactory(),
    "onedrive": OneDriveProviderFactory(),
    "dropbox": DropBoxProviderFactory(),
}


def get_provider_factory(provider_name: str):
    provider_factory = FACTORY_REGISTRY.get(provider_name)
    if not provider_factory:
        raise ValueError(f"Invalid provider name: {provider_name}")
    return provider_factory
