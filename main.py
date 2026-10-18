import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.persistence.config.database import (
    get_database,
    close_mongo_client,
)
from app.persistence.indexes import init_indexes
from app.web.error_handlers import register_error_handlers
from app.web.routers import (
    artists_router,
    categories_router,
    artworks_router,
    catalog_router,
    health_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to database and initialize indexes
    db = get_database()
    app.state.db = db
    try:
        await init_indexes(db)
    except Exception as e:
        print(f"Warning: Could not automatically initialize indexes: {e}")
    yield
    # Shutdown: Cleanly close database connections
    close_mongo_client()


app = FastAPI(
    title="Atrium Catalog API (Microservice)",
    description="NoSQL catalog and polymorphic query microservice for Atrium",
    version="1.0.0",
    lifespan=lifespan,
)

# ---- Global Error Handlers (Domain -> HTTP) ----
register_error_handlers(app)

# ---- CORS Configuration ----
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000,http://localhost:5000")
origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

# If wildcard '*' is included, allow_credentials cannot be True per browser specification
allow_creds = "*" not in origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=allow_creds,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Mount Routers ----
# 1. Health check for orchestrators and gateways
app.include_router(health_router)

# 2. Standard plural REST routes
app.include_router(artists_router, prefix="/artists")
app.include_router(categories_router, prefix="/categories")
app.include_router(artworks_router, prefix="/artworks")
app.include_router(catalog_router, prefix="/catalog")

# 3. Backward compatibility (singular routes)
app.include_router(artists_router, prefix="/artist", include_in_schema=False)
app.include_router(categories_router, prefix="/category", include_in_schema=False)
app.include_router(artworks_router, prefix="/artwork", include_in_schema=False)
