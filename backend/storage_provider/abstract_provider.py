from abc import ABC, abstractmethod
from typing import Dict


class AbstractStorageProvider(ABC):

    def __init__(self, credentials: Dict):
        self.credentials = credentials

    @abstractmethod
    def authenticate(self, credentials: Dict):
        pass

    @abstractmethod
    def upload_chunk(self):
        pass

    @abstractmethod
    def download_chunk(self) -> str:
        pass

    @abstractmethod
    def delete_chunk(self):
        pass

    @abstractmethod
    def get_stats(self) -> Dict:
        pass
