from pydantic import BaseModel, Field
from typing import Optional


class ArtworkBaseDTO(BaseModel):
    genero_id: int = Field(..., description="ID del género/categoría")
    autor_id: int = Field(..., description="ID del artista/autor")
    nombre: str = Field(..., max_length=150)
    fecha_creacion: Optional[str] = None
    precio_obra: float = Field(..., gt=0)
    porcentaje_ganancia: Optional[float] = Field(None, ge=0)
    estatus: str = Field("Disponible", description="Disponible, Reservada, Vendida")
    foto: Optional[str] = None
    detalles: dict[str, str] = Field(default_factory=dict, description="Campos polimórficos de la obra")


class ArtworkCreateDTO(ArtworkBaseDTO):
    id_sql: int = Field(..., description="ID de la obra en el núcleo SQL")


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
