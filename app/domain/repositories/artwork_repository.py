from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.artwork import Artwork


class ArtworkRepository(ABC):
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Artwork]:
        pass

    @abstractmethod
    async def get_by_id_sql(self, id_sql: int) -> Optional[Artwork]:
        pass

    @abstractmethod
    async def create(self, artwork: Artwork) -> Artwork:
        pass

    @abstractmethod
    async def upsert(self, artwork: Artwork) -> Artwork:
        pass

    @abstractmethod
    async def update(self, id_sql: int, artwork_data: dict) -> Optional[Artwork]:
        pass

    @abstractmethod
    async def delete(self, id_sql: int) -> bool:
        pass
