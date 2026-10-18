from fastapi import APIRouter, Depends, Query, status
from app.domain.models.category import Category
from app.domain.services.category_service import CategoryService
from app.domain.repositories.category_repository import CategoryRepository
from app.web.dependencies import get_category_service, get_category_repository
from app.web.schemas.category_schema import (
    CategoryCreateDTO,
    CategoryUpdateDTO,
    CategoryResponseDTO,
)

router = APIRouter(tags=["Categories"])


@router.post("/", response_model=CategoryResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_category(
    dto: CategoryCreateDTO,
    sync: bool = Query(False, description="Si es True, realiza un Upsert idempotente para sincronización"),
    service: CategoryService = Depends(get_category_service),
):
    category_model = Category(**dto.model_dump())
    return await service.create_category(category_model, sync_mode=sync)


@router.get("/", response_model=list[CategoryResponseDTO])
async def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    repo: CategoryRepository = Depends(get_category_repository),
):
    return await repo.get_all(skip=skip, limit=limit)


@router.get("/{id}", response_model=CategoryResponseDTO)
async def get_category(
    id: int,
    service: CategoryService = Depends(get_category_service),
):
    return await service.get_category(id)


@router.put("/{id}", response_model=CategoryResponseDTO)
async def update_category(
    id: int,
    dto: CategoryUpdateDTO,
    service: CategoryService = Depends(get_category_service),
):
    update_data = dto.model_dump(exclude_unset=True)
    return await service.update_category(id, update_data)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_category(
    id: int,
    service: CategoryService = Depends(get_category_service),
):
    await service.delete_category(id)
    return {"msg": "Categoría borrada", "id_sql": id}
