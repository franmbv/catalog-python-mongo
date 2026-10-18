from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.domain.models.artwork import Artwork
from app.domain.repositories.artwork_repository import ArtworkRepository
from app.persistence.entities.artwork_entity import ArtworkEntity
from app.persistence.mappers.artwork_mapper import ArtworkMapper


class MongoArtworkRepository(ArtworkRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db["artworks"]

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Artwork]:
        cursor = self._collection.find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        entities = [ArtworkEntity(**doc) for doc in docs]
        return [ArtworkMapper.to_domain(entity) for entity in entities]

    async def get_by_id_sql(self, id_sql: int) -> Optional[Artwork]:
        doc = await self._collection.find_one({"id_sql": id_sql})
        if not doc:
            return None
        entity = ArtworkEntity(**doc)
        return ArtworkMapper.to_domain(entity)

    async def create(self, artwork: Artwork) -> Artwork:
        doc = ArtworkMapper.to_document(artwork)
        await self._collection.insert_one(doc)
        return artwork

    async def upsert(self, artwork: Artwork) -> Artwork:
        doc = ArtworkMapper.to_document(artwork)
        await self._collection.update_one(
            {"id_sql": artwork.id_sql},
            {"$set": doc},
            upsert=True,
        )
        return artwork

    async def update(self, id_sql: int, artwork_data: dict) -> Optional[Artwork]:
        update_data = {k: v for k, v in artwork_data.items() if k not in ("id_sql", "_id")}
        await self._collection.update_one(
            {"id_sql": id_sql},
            {"$set": update_data},
        )
        return await self.get_by_id_sql(id_sql)

    async def delete(self, id_sql: int) -> bool:
        result = await self._collection.delete_one({"id_sql": id_sql})
        return result.deleted_count > 0
