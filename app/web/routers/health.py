from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.web.dependencies import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", summary="Verifica el estado del microservicio y la conexión a MongoDB")
async def health_check(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        await db.command("ping")
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Fallo en la conexión a la base de datos: {str(exc)}",
        )
