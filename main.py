from fastapi import FastAPI
from app.routes import artworks,catalog,categories

app = FastAPI()

app.include_router(artworks.router)
app.include_router(catalog.router)
app.include_router(categories.router)

