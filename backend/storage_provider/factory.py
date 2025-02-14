from abc import ABC, abstractmethod
from typing import Dict
from backend.storage_provider.abstract_provider import AbstractStorageProvider
from backend.storage_provider.google_drive.provider import GoogleDriveProvider
from backend.storage_provider.onedrive.provider import OneDriveProvider
from backend.storage_provider.dropbox.provider import DropBoxProvider


class StorageProviderFactory(ABC):
    @abstractmethod
    def create_provider(self, credentials: Dict) -> AbstractStorageProvider:
        pass


class GoogleDriveProviderFactory(StorageProviderFactory):
    def create_provider(self, credentials: Dict) -> GoogleDriveProvider:
        return GoogleDriveProvider(credentials=credentials)


class OneDriveProviderFactory(StorageProviderFactory):
    def create_provider(self, credentials: Dict) -> OneDriveProvider:
        return OneDriveProvider(credentials=credentials)


class DropBoxProviderFactory(StorageProviderFactory):
    def create_provider(self, credentials: Dict) -> DropBoxProvider:
        return DropBoxProvider(credentials=credentials)


FACTORY_REGISTRY = {
    "google_drive": GoogleDriveProviderFactory(),
    "onedrive": OneDriveProviderFactory(),
    "dropbox": DropBoxProviderFactory(),
}


def get_provider_factory(provider_name: str) -> StorageProviderFactory:
    provider_factory = FACTORY_REGISTRY.get(provider_name)
    if not provider_factory:
        raise ValueError(f"Invalid provider name: {provider_name}")
    return provider_factory


def get_provider(provider_name: str, credentials: Dict) -> AbstractStorageProvider:
    provider_factory = get_provider_factory(provider_name)
    return provider_factory.create_provider(credentials)
