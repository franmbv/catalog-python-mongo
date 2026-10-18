from abc import ABC, abstractmethod
from typing import Optional
from app.domain.models.category import Category


class CategoryRepository(ABC):
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Category]:
        pass

    @abstractmethod
    async def get_by_id_sql(self, id_sql: int) -> Optional[Category]:
        pass

    @abstractmethod
    async def create(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def upsert(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def update(self, id_sql: int, category_data: dict) -> Optional[Category]:
        pass

    @abstractmethod
    async def delete(self, id_sql: int) -> bool:
        pass

    @abstractmethod
    async def has_artworks(self, id_sql: int) -> bool:
        pass
