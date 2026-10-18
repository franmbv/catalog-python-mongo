from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.domain.models.artist import Artist
from app.domain.repositories.artist_repository import ArtistRepository
from app.persistence.entities.artist_entity import ArtistEntity
from app.persistence.mappers.artist_mapper import ArtistMapper


class MongoArtistRepository(ArtistRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db["artists"]
        self._artworks_collection = db["artworks"]

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[Artist]:
        cursor = self._collection.find().skip(skip).limit(limit)
        docs = await cursor.to_list(length=limit)
        entities = [ArtistEntity(**doc) for doc in docs]
        return [ArtistMapper.to_domain(entity) for entity in entities]

    async def get_by_id_sql(self, id_sql: int) -> Optional[Artist]:
        doc = await self._collection.find_one({"id_sql": id_sql})
        if not doc:
            return None
        entity = ArtistEntity(**doc)
        return ArtistMapper.to_domain(entity)

    async def create(self, artist: Artist) -> Artist:
        doc = ArtistMapper.to_document(artist)
        await self._collection.insert_one(doc)
        return artist

    async def upsert(self, artist: Artist) -> Artist:
        doc = ArtistMapper.to_document(artist)
        await self._collection.update_one(
            {"id_sql": artist.id_sql},
            {"$set": doc},
            upsert=True,
        )
        return artist

    async def update(self, id_sql: int, artist_data: dict) -> Optional[Artist]:
        update_data = {k: v for k, v in artist_data.items() if k not in ("id_sql", "_id")}
        await self._collection.update_one(
            {"id_sql": id_sql},
            {"$set": update_data},
        )
        return await self.get_by_id_sql(id_sql)

    async def delete(self, id_sql: int) -> bool:
        result = await self._collection.delete_one({"id_sql": id_sql})
        return result.deleted_count > 0

    async def has_artworks(self, id_sql: int) -> bool:
        artwork = await self._artworks_collection.find_one({"autor_id": id_sql})
        return artwork is not None
