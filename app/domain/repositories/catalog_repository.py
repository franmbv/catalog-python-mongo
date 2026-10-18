from abc import ABC, abstractmethod
from typing import Optional


class CatalogRepository(ABC):
    @abstractmethod
    async def search(
        self,
        genero_id: Optional[int] = None,
        estatus: Optional[str] = None,
        precio_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[dict]:
        pass
