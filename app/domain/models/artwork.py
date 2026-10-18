"""Artwork domain model."""
from pydantic import BaseModel, Field
from typing import Optional


class Artwork(BaseModel):
    id_sql: int = Field(..., description="ID de la obra en el núcleo SQL")
    genero_id: int = Field(..., description="ID de la categoría / género")
    autor_id: int = Field(..., description="ID del artista")
    nombre: str = Field(..., max_length=150)
    fecha_creacion: Optional[str] = None
    precio_obra: float = Field(..., gt=0)
    porcentaje_ganancia: Optional[float] = Field(None, ge=0)
    estatus: str = Field("Disponible")
    foto: Optional[str] = None
    detalles: dict[str, str] = Field(default_factory=dict, description="Detalles polimórficos de la obra")
