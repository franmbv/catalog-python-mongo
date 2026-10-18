from typing import Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.domain.repositories.catalog_repository import CatalogRepository


class MongoCatalogRepository(CatalogRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = db["artworks"]

    async def search(
        self,
        genero_id: Optional[int] = None,
        estatus: Optional[str] = None,
        precio_max: Optional[float] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[dict]:
        pipeline = []

        # 1. Dynamic filters ($match)
        match_stage = {}
        if genero_id is not None:
            match_stage["genero_id"] = genero_id
        if estatus is not None:
            match_stage["estatus"] = estatus
        if precio_max is not None:
            match_stage["precio_obra"] = {"$lte": precio_max}

        if match_stage:
            pipeline.append({"$match": match_stage})

        # 2. Join with artists collection ($lookup)
        pipeline.append({
            "$lookup": {
                "from": "artists",
                "localField": "autor_id",
                "foreignField": "id_sql",
                "as": "informacion_artista",
            }
        })

        # 3. Unwind artist information ($unwind)
        pipeline.append({
            "$unwind": {
                "path": "$informacion_artista",
                "preserveNullAndEmptyArrays": True,
            }
        })

        # 4. Projection to exclude internal Mongo ObjectIds
        pipeline.append({
            "$project": {
                "_id": 0,
                "informacion_artista._id": 0,
            }
        })

        # 5. Pagination
        if skip > 0:
            pipeline.append({"$skip": skip})
        pipeline.append({"$limit": limit})

        cursor = self._collection.aggregate(pipeline)
        return await cursor.to_list(length=limit)
