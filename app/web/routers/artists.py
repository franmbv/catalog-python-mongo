from fastapi import APIRouter, Depends, Query, status
from app.domain.models.artist import Artist
from app.domain.services.artist_service import ArtistService
from app.domain.repositories.artist_repository import ArtistRepository
from app.web.dependencies import get_artist_service, get_artist_repository
from app.web.schemas.artist_schema import (
    ArtistCreateDTO,
    ArtistUpdateDTO,
    ArtistResponseDTO,
)

router = APIRouter(tags=["Artists"])


@router.post("/", response_model=ArtistResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_artist(
    dto: ArtistCreateDTO,
    sync: bool = Query(False, description="If True, performs an idempotent Upsert for synchronization"),
    service: ArtistService = Depends(get_artist_service),
):
    artist_model = Artist(**dto.model_dump())
    created = await service.create_artist(artist_model, sync_mode=sync)
    return created


@router.get("/", response_model=list[ArtistResponseDTO])
async def list_artists(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    repo: ArtistRepository = Depends(get_artist_repository),
):
    return await repo.get_all(skip=skip, limit=limit)


@router.get("/{id}", response_model=ArtistResponseDTO)
async def get_artist(
    id: int,
    service: ArtistService = Depends(get_artist_service),
):
    return await service.get_artist(id)


@router.put("/{id}", response_model=ArtistResponseDTO)
async def update_artist(
    id: int,
    dto: ArtistUpdateDTO,
    service: ArtistService = Depends(get_artist_service),
):
    update_data = dto.model_dump(exclude_unset=True)
    return await service.update_artist(id, update_data)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_artist(
    id: int,
    service: ArtistService = Depends(get_artist_service),
):
    await service.delete_artist(id)
    return {"msg": "Artist deleted from NoSQL catalog", "id_sql": id}
