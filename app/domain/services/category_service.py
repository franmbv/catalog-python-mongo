"""Domain service for Category operations and business rules."""
from app.domain.models.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
    BusinessRuleConflictError,
)


class CategoryService:
    def __init__(self, category_repo: CategoryRepository):
        self.category_repo = category_repo

    async def create_category(self, category: Category, sync_mode: bool = False) -> Category:
        existing = await self.category_repo.get_by_id_sql(category.id_sql)
        if existing and not sync_mode:
            raise EntityAlreadyExistsError(f"La categoría con ID {category.id_sql} ya existe.")
        if sync_mode:
            return await self.category_repo.upsert(category)
        return await self.category_repo.create(category)

    async def get_category(self, id_sql: int) -> Category:
        category = await self.category_repo.get_by_id_sql(id_sql)
        if not category:
            raise EntityNotFoundError(f"Categoría con ID {id_sql} no encontrada.")
        return category

    async def update_category(self, id_sql: int, data: dict) -> Category:
        await self.get_category(id_sql)
        return await self.category_repo.update(id_sql, data)

    async def delete_category(self, id_sql: int) -> bool:
        await self.get_category(id_sql)
        has_works = await self.category_repo.has_artworks(id_sql)
        if has_works:
            raise BusinessRuleConflictError(
                f"No se puede borrar la categoría con ID {id_sql} porque tiene obras asociadas."
            )
        return await self.category_repo.delete(id_sql)
