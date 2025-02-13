from abc import ABC, abstractmethod
from typing import List


class ChunkStrategyBase(ABC):
    @abstractmethod
    def split_file(self, input_file_path: str, chunk_size: int) -> List[str]:
        pass

    @abstractmethod
    def merge_chunks(self, file_id: str) -> str:
        pass


class FixedSizeChunkStrategy(ChunkStrategyBase):
    def split_file(
        self, input_file_path: str, chunk_size: int = 100 * 1024 * 1024
    ) -> List[str]:
        """
        Split a file into chunks of specified size (default: 100MB).
        Returns a list of chunk file paths.
        """
        chunk_paths = []
        part_num = 1

        with open(input_file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                chunk_name = f"{input_file_path}.part{part_num}"
                with open(chunk_name, "wb") as chunk_file:
                    chunk_file.write(chunk)

                chunk_paths.append(chunk_name)
                part_num += 1

        return chunk_paths

    def merge_chunks(self, file_id: str) -> str:
        return "to be implemented"
