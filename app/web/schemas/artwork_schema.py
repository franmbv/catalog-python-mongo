from pydantic import BaseModel, Field
from typing import Optional


class ArtworkBaseDTO(BaseModel):
    genero_id: int = Field(..., description="Category/genre ID")
    autor_id: int = Field(..., description="Artist/author ID")
    nombre: str = Field(..., max_length=150)
    fecha_creacion: Optional[str] = None
    precio_obra: float = Field(..., gt=0)
    porcentaje_ganancia: Optional[float] = Field(None, ge=0)
    estatus: str = Field("Disponible", description="Status: Disponible, Reservada, Vendida")
    foto: Optional[str] = None
    detalles: dict[str, str] = Field(default_factory=dict, description="Polymorphic dynamic fields of the artwork")


class ArtworkCreateDTO(ArtworkBaseDTO):
    id_sql: int = Field(..., description="Artwork ID in core SQL database")


class ArtworkUpdateDTO(BaseModel):
    genero_id: Optional[int] = None
    autor_id: Optional[int] = None
    nombre: Optional[str] = Field(None, max_length=150)
    fecha_creacion: Optional[str] = None
    precio_obra: Optional[float] = Field(None, gt=0)
    porcentaje_ganancia: Optional[float] = Field(None, ge=0)
    estatus: Optional[str] = None
    foto: Optional[str] = None
    detalles: Optional[dict[str, str]] = None


class ArtworkResponseDTO(ArtworkBaseDTO):
    id_sql: int
