import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("ERROR: La variable de entorno MONGO_URI no está configurada en el archivo .env")

# 1. Inicializar el cliente de Motor de forma global (pero sin conectar aún)
client: AsyncIOMotorClient = None
db = None

async def init_db():
    """
    Inicializa la conexión asíncrona con MongoDB Atlas.
    Se ejecuta automáticamente al arrancar el servidor FastAPI (lifespan).
    """
    global client, db
    try:
        # 2. Crear la instancia del cliente asíncrono
        client = AsyncIOMotorClient(MONGO_URI)
        
        # 3. Seleccionar la base de datos (Motor la extrae automáticamente de la URI o usa 'atrium_db')
        db = client.get_default_database()
        
        # 4. Forzar una consulta rápida para verificar que las credenciales y el internet estén bien
        await client.admin.command('ping')
        print("🚀 [DATABASE] Conexión asíncrona a MongoDB Atlas establecida con éxito.")
        
    except Exception as e:
        print(f"❌ [DATABASE] Error crítico al conectar a MongoDB Atlas: {e}")
        raise e

def get_db():
    """
    Función utilitaria para obtener la instancia de la base de datos
    en otros archivos o rutas (como en tu catalog.py).
    """
    if db is None:
        raise RuntimeError("La base de datos no ha sido inicializada. Llama a init_db() primero.")
    return db