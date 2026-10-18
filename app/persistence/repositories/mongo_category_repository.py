from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.domain.models.category import Category
from app.domain.repositories.category_repository import CategoryRepository
from app.persistence.entities.category_entity import CategoryEntity
from app.persistence.mappers.category_mapper import CategoryMapper


class MongoCategoryRepository(CategoryRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db["categories"]
        self._artworks_collection = db["artworks"]

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Category]:
        cursor = self._collection.find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        entities = [CategoryEntity(**doc) for doc in docs]
        return [CategoryMapper.to_domain(entity) for entity in entities]

    async def get_by_id_sql(self, id_sql: int) -> Optional[Category]:
        doc = await self._collection.find_one({"id_sql": id_sql})
        if not doc:
            return None
        entity = CategoryEntity(**doc)
        return CategoryMapper.to_domain(entity)

    async def create(self, category: Category) -> Category:
        doc = CategoryMapper.to_document(category)
        await self._collection.insert_one(doc)
        return category

    async def upsert(self, category: Category) -> Category:
        doc = CategoryMapper.to_document(category)
        await self._collection.update_one(
            {"id_sql": category.id_sql},
            {"$set": doc},
            upsert=True,
        )
        return category

    async def update(self, id_sql: int, category_data: dict) -> Optional[Category]:
        update_data = {k: v for k, v in category_data.items() if k not in ("id_sql", "_id")}
        await self._collection.update_one(
            {"id_sql": id_sql},
            {"$set": update_data},
        )
        return await self.get_by_id_sql(id_sql)

    async def delete(self, id_sql: int) -> bool:
        result = await self._collection.delete_one({"id_sql": id_sql})
        return result.deleted_count > 0

    async def has_artworks(self, id_sql: int) -> bool:
        artwork = await self._artworks_collection.find_one({"genero_id": id_sql})
        return artwork is not None
