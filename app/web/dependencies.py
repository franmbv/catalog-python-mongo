from fastapi import Depends, Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.persistence.config.database import get_database
from app.domain.repositories import (
    ArtistRepository,
    CategoryRepository,
    ArtworkRepository,
    CatalogRepository,
)
from app.persistence.repositories import (
    MongoArtistRepository,
    MongoCategoryRepository,
    MongoArtworkRepository,
    MongoCatalogRepository,
)
from app.domain.services import (
    ArtistService,
    CategoryService,
    ArtworkService,
    CatalogService,
)


def get_db(request: Request) -> AsyncIOMotorDatabase:
    """Obtiene la instancia de la base de datos desde app.state o fallback a get_database()."""
    if hasattr(request.app.state, "db") and request.app.state.db is not None:
        return request.app.state.db
    return get_database()


# ── Repositorios ──────────────────────────────────────────────────
def get_artist_repository(db: AsyncIOMotorDatabase = Depends(get_db)) -> ArtistRepository:
    return MongoArtistRepository(db)


def get_category_repository(db: AsyncIOMotorDatabase = Depends(get_db)) -> CategoryRepository:
    return MongoCategoryRepository(db)


def get_artwork_repository(db: AsyncIOMotorDatabase = Depends(get_db)) -> ArtworkRepository:
    return MongoArtworkRepository(db)


def get_catalog_repository(db: AsyncIOMotorDatabase = Depends(get_db)) -> CatalogRepository:
    return MongoCatalogRepository(db)


# ── Servicios de Dominio ──────────────────────────────────────────
def get_artist_service(
    artist_repo: ArtistRepository = Depends(get_artist_repository),
) -> ArtistService:
    return ArtistService(artist_repo=artist_repo)


def get_category_service(
    category_repo: CategoryRepository = Depends(get_category_repository),
) -> CategoryService:
    return CategoryService(category_repo=category_repo)


def get_artwork_service(
    artwork_repo: ArtworkRepository = Depends(get_artwork_repository),
    artist_repo: ArtistRepository = Depends(get_artist_repository),
    category_repo: CategoryRepository = Depends(get_category_repository),
) -> ArtworkService:
    return ArtworkService(
        artwork_repo=artwork_repo,
        artist_repo=artist_repo,
        category_repo=category_repo,
    )


def get_catalog_service(
    catalog_repo: CatalogRepository = Depends(get_catalog_repository),
) -> CatalogService:
    return CatalogService(catalog_repo=catalog_repo)
