from fastapi import FastAPI
from app.routes import artists,artworks,catalog,categories

app = FastAPI()

app.include_router(artists.router)
app.include_router(categories.router)
app.include_router(artworks.router)
app.include_router(catalog.router)

