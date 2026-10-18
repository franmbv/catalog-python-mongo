"""Domain service for Catalog search and aggregations."""
from typing import Optional
from app.domain.repositories.catalog_repository import CatalogRepository


class CatalogService:
    def __init__(self, catalog_repo: CatalogRepository):
        self.catalog_repo = catalog_repo

    async def search_catalog(
        self,
        genero_id: Optional[int] = None,
        estatus: Optional[str] = None,
        precio_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[dict]:
        return await self.catalog_repo.search(
            genero_id=genero_id,
            estatus=estatus,
            precio_max=precio_max,
            skip=skip,
            limit=limit,
        )
