from fastapi import APIRouter

router = APIRouter(prefix="/artwork",tags=["Artworks"])

#Coloca de aqui para abajo todos los endpoints pero con 'router' en vez de 'app'
#Hacer CRUD de enpoints para 'Artworks' verificar correspondencia con  los schemas expuestos en 'Schemas/artwork.py'

#Enpoint - Create

#Enpoint - Update

#Enpoint - Get

#Enpoint - Delete

#=================
from app.config.database import db
from app.schemas.artwork import ArtworkCreate, ArtworkResponse

router = APIRouter(prefix="/artwork", tags=["Artworks"])

# Endpoint - Create
@router.post("/", response_model=ArtworkResponse)
async def create_artwork(artwork: ArtworkCreate):
    # 1. Buscar la categoría en MongoDB usando el categoria_id de la obra
    categoria = await db.categories.find_one({"id_sql": artwork.categoria_id})
    
    # Si la categoría no existe, frenamos
    if not categoria:
        return {"error": f"La categoría con ID {artwork.categoria_id} no existe. No se puede crear la obra."}
    
    # 2. Extraer la plantilla de requisitos (que es una lista de strings en la categoría)
    requisitos = categoria.get("detalles", [])
    
    # 3. Validar que cada campo de la plantilla exista en los detalles de la obra
    for campo_obligatorio in requisitos:
        if campo_obligatorio not in artwork.detalles:
            return {
                "error": "Validación de plantilla fallida",
                "detalle": f"Falta el campo obligatorio '{campo_obligatorio}' requerido para la categoría {categoria['id_sql']}"
            }
            
    # 4. Si pasó la validación, se guarda con éxito en MongoDB Atlas
    await db.artworks.insert_one(artwork.model_dump())
    return artwork

# Endpoint - Get All (Listar todas las obras)
@router.get("/", response_model=list[ArtworkResponse])
async def read_artwork_all():
    cursor = db.artworks.find()
    # Convierte el cursor asíncrono de Motor a una lista de Python
    artworks_db = await cursor.to_list(length=100)
    return artworks_db

# Endpoint - Get por ID (Buscar una obra específica)
@router.get("/{id}")
async def read_artwork_id(id: int):
    # Busca en MongoDB usando el id_sql que conecta con Node.js
    artwork = await db.artworks.find_one({"id_sql": id})
    
    if artwork:
        artwork["_id"] = str(artwork["_id"])  # Limpieza del ObjectId de BSON
    return artwork

# Endpoint - Update
@router.put("/{id}")
async def update_artwork_id(id: int, artwork: ArtworkCreate):
    # Modifica los datos de la obra usando el id_sql
    await db.artworks.update_one({"id_sql": id}, {"$set": artwork.model_dump()})
    return {"msg": "Obra actualizada", "id_sql": id}

# Endpoint - Delete
@router.delete("/{id}")
async def delete_artwork_id(id: int):
    # Borra el documento polimórfico de la colección
    await db.artworks.delete_one({"id_sql": id})
    return {"msg": "Obra borrada", "id_sql": id}