from abc import ABC, abstractmethod


class StorageAdapter(ABC):
    @abstractmethod
    async def upload(self, content: bytes, key: str, content_type: str) -> str:
        """Загружает файл и возвращает URL"""
        ...