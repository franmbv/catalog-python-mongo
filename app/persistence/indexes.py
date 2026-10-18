"""Index initialization for MongoDB collections."""
from motor.motor_asyncio import AsyncIOMotorDatabase


async def init_indexes(db: AsyncIOMotorDatabase) -> None:
    """Creates required indexes to enforce uniqueness and optimize queries."""
    # 1. Artists: unique id_sql index
    await db.artists.create_index("id_sql", unique=True)

    # 2. Categories: unique id_sql index
    await db.categories.create_index("id_sql", unique=True)

    # 3. Artworks: unique id_sql, indexed autor_id and genero_id for lookups
    await db.artworks.create_index("id_sql", unique=True)
    await db.artworks.create_index("autor_id")
    await db.artworks.create_index("genero_id")

    # 4. Compound index for catalog searching and filtering
    await db.artworks.create_index([
        ("genero_id", 1),
        ("estatus", 1),
        ("precio_obra", 1),
    ])
