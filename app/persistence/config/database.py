import os
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "atrium_db_ej")

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        if not MONGO_URI:
            raise ValueError("ERROR: La variable de entorno MONGO_URI no está configurada")
        _client = AsyncIOMotorClient(MONGO_URI)
    return _client


def get_database() -> AsyncIOMotorDatabase:
    client = get_mongo_client()
    return client[MONGO_DB_NAME]


def close_mongo_client():
    global _client
    if _client is not None:
        _client.close()
        _client = None
