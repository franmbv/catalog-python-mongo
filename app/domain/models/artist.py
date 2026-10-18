"""Domain models for Atrium Catalog."""
from pydantic import BaseModel, Field
from typing import Optional


class Artist(BaseModel):
    id_sql: int = Field(..., description="ID del artista en el núcleo SQL")
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    fecha_nac: Optional[str] = None
    fecha_fal: Optional[str] = None
    nacionalidad: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    fotografia: Optional[str] = Field(None, max_length=255)
    estado: str = Field("Activo", description="Activo o Inactivo")
