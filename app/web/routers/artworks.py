from fastapi import APIRouter, Depends, Query, status
from app.domain.models.artwork import Artwork
from app.domain.services.artwork_service import ArtworkService
from app.domain.repositories.artwork_repository import ArtworkRepository
from app.web.dependencies import get_artwork_service, get_artwork_repository
from app.web.schemas.artwork_schema import (
    ArtworkCreateDTO,
    ArtworkUpdateDTO,
    ArtworkResponseDTO,
)

router = APIRouter(tags=["Artworks"])


@router.post("/", response_model=ArtworkResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_artwork(
    dto: ArtworkCreateDTO,
    sync: bool = Query(False, description="Si es True, realiza un Upsert idempotente para sincronización"),
    service: ArtworkService = Depends(get_artwork_service),
):
    artwork_model = Artwork(**dto.model_dump())
    return await service.create_artwork(artwork_model, sync_mode=sync)


@router.get("/", response_model=list[ArtworkResponseDTO])
async def list_artworks(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    repo: ArtworkRepository = Depends(get_artwork_repository),
):
    return await repo.get_all(skip=skip, limit=limit)


@router.get("/{id}", response_model=ArtworkResponseDTO)
async def get_artwork(
    id: int,
    service: ArtworkService = Depends(get_artwork_service),
):
    return await service.get_artwork(id)


@router.put("/{id}", response_model=ArtworkResponseDTO)
async def update_artwork(
    id: int,
    dto: ArtworkUpdateDTO,
    service: ArtworkService = Depends(get_artwork_service),
):
    update_data = dto.model_dump(exclude_unset=True)
    return await service.update_artwork(id, update_data)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_artwork(
    id: int,
    service: ArtworkService = Depends(get_artwork_service),
):
    await service.delete_artwork(id)
    return {"msg": "Obra borrada del catálogo", "id_sql": id}
