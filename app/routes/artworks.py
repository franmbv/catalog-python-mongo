from fastapi import APIRouter
from app.config.database import db

#Idea de como quedarian las exportaciones una vez realizados los 'Schemas'
#from app.schemas.artwork import ArtworkCreate, ArtworkResponse

router = APIRouter(prefix="/artwork",tags=["Artworks"])

#Coloca de aqui para abajo todos los endpoints pero con 'router' en vez de 'app'
#Hacer CRUD de enpoints para 'Artworks' verificar correspondencia con  los schemas expuestos en 'Schemas/artwork.py'

#Enpoint - Create (Verificar que la 'Category' a la que se esta haciendo referencia exista)

#Enpoint - Update

#Enpoint - Get

#Enpoint - Delete

