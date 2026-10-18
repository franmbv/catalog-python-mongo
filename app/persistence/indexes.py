"""Index initialization for MongoDB collections."""
from motor.motor_asyncio import AsyncIOMotorDatabase


async def init_indexes(db: AsyncIOMotorDatabase) -> None:
    """Crea los índices necesarios para garantizar unicidad y optimizar búsquedas."""
    # 1. Artistas: id_sql único
    await db.artists.create_index("id_sql", unique=True)

    # 2. Categorías: id_sql único
    await db.categories.create_index("id_sql", unique=True)

    # 3. Obras: id_sql único, autor_id indexado para validaciones y lookups
    await db.artworks.create_index("id_sql", unique=True)
    await db.artworks.create_index("autor_id")
    await db.artworks.create_index("genero_id")

    # 4. Índice compuesto para la búsqueda y filtrado del catálogo
    await db.artworks.create_index([
        ("genero_id", 1),
        ("estatus", 1),
        ("precio_obra", 1),
    ])
