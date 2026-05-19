from fastapi import APIRouter
from app.config.database import db

#Idea de como quedarian las exportaciones una vez realizados los 'Schemas'
#from app.schemas.category import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/category",tags=["Categories"])

#Coloca de aqui para abajo todos los endpoints pero con 'router' en vez de 'app'
#Hacer CRUD de enpoints para 'Categories' verificar correspondencia con  los schemas expuestos en 'Schemas/artwork.py'

#Enpoint - Create

#Enpoint - Update

#Enpoint - Get

#Enpoint - Delete