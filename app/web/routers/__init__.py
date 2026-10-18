from app.web.routers.artists import router as artists_router
from app.web.routers.categories import router as categories_router
from app.web.routers.artworks import router as artworks_router
from app.web.routers.catalog import router as catalog_router
from app.web.routers.health import router as health_router

__all__ = [
    "artists_router",
    "categories_router",
    "artworks_router",
    "catalog_router",
    "health_router",
]
