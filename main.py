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
    # Startup: Conectar a la base de datos e inicializar índices
    db = get_database()
    app.state.db = db
    try:
        await init_indexes(db)
    except Exception as e:
        print(f"Advertencia: No se pudieron inicializar los índices automáticamente: {e}")
    yield
    # Shutdown: Cerrar conexiones limpiamente
    close_mongo_client()


app = FastAPI(
    title="Atrium Catalog API (Microservice)",
    description="Microservicio NoSQL de catálogo y motor polimórfico para Atrium",
    version="1.0.0",
    lifespan=lifespan,
)

# ---- Manejadores Globales de Errores (Dominio -> HTTP) ----
register_error_handlers(app)

# ---- Configuración de CORS ----
cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost,http://localhost:3000,http://localhost:5000")
origins = [origin.strip() for origin in cors_origins_env.split(",") if origin.strip()]

# Si contiene '*', allow_credentials no puede ser True según la especificación del navegador
allow_creds = "*" not in origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=allow_creds,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Montaje de Routers ----
# 1. Health check para orquestadores y gateway
app.include_router(health_router)

# 2. Rutas estándar en plural
app.include_router(artists_router, prefix="/artists")
app.include_router(categories_router, prefix="/categories")
app.include_router(artworks_router, prefix="/artworks")
app.include_router(catalog_router, prefix="/catalog")

# 3. Compatibilidad hacia atrás (rutas en singular)
app.include_router(artists_router, prefix="/artist", include_in_schema=False)
app.include_router(categories_router, prefix="/category", include_in_schema=False)
app.include_router(artworks_router, prefix="/artwork", include_in_schema=False)
