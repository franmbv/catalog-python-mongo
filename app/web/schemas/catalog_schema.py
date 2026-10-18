from pydantic import BaseModel
from typing import Optional
from app.web.schemas.artist_schema import ArtistResponseDTO


class CatalogArtworkSearchResponseDTO(BaseModel):
    id_sql: int
    genero_id: int
    autor_id: int
    nombre: str
    fecha_creacion: Optional[str] = None
    precio_obra: float
    porcentaje_ganancia: Optional[float] = None
    estatus: str
    foto: Optional[str] = None
    detalles: dict[str, str]
    informacion_artista: Optional[ArtistResponseDTO] = None
