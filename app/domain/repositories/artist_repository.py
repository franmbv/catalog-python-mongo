from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.artist import Artist


class ArtistRepository(ABC):
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Artist]:
        pass

    @abstractmethod
    async def get_by_id_sql(self, id_sql: int) -> Optional[Artist]:
        pass

    @abstractmethod
    async def create(self, artist: Artist) -> Artist:
        pass

    @abstractmethod
    async def upsert(self, artist: Artist) -> Artist:
        pass

    @abstractmethod
    async def update(self, id_sql: int, artist_data: dict) -> Optional[Artist]:
        pass

    @abstractmethod
    async def delete(self, id_sql: int) -> bool:
        pass

    @abstractmethod
    async def has_artworks(self, id_sql: int) -> bool:
        pass
