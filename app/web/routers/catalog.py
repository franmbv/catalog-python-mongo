from fastapi import APIRouter, Depends, Query
from typing import Optional
from app.domain.services.catalog_service import CatalogService
from app.web.dependencies import get_catalog_service
from app.web.schemas.catalog_schema import CatalogArtworkSearchResponseDTO

router = APIRouter(tags=["Catalog"])


@router.get("/search", response_model=list[CatalogArtworkSearchResponseDTO])
async def search_catalog(
    genero_id: Optional[int] = Query(None, description="Filtrar por ID de género"),
    estatus: Optional[str] = Query(None, description="Filtrar por estatus: Disponible, Reservada, Vendida"),
    precio_max: Optional[float] = Query(None, description="Precio máximo de la obra"),
    skip: int = Query(0, ge=0, description="Cantidad de registros a omitir para paginación"),
    limit: int = Query(100, ge=1, le=500, description="Límite de registros a retornar"),
    service: CatalogService = Depends(get_catalog_service),
):
    return await service.search_catalog(
        genero_id=genero_id,
        estatus=estatus,
        precio_max=precio_max,
        skip=skip,
        limit=limit,
    )
