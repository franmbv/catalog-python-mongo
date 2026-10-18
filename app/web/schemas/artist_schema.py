from pydantic import BaseModel, Field
from typing import Optional


class ArtistBaseDTO(BaseModel):
    nombre: str = Field(..., max_length=100)
    apellido: str = Field(..., max_length=100)
    fecha_nac: Optional[str] = None
    fecha_fal: Optional[str] = None
    nacionalidad: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    fotografia: Optional[str] = Field(None, max_length=255)
    estado: str = Field("Activo", description="Activo o Inactivo")


class ArtistCreateDTO(ArtistBaseDTO):
    id_sql: int = Field(..., description="ID del artista en el núcleo SQL")


class ArtistUpdateDTO(BaseModel):
    nombre: Optional[str] = Field(None, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    fecha_nac: Optional[str] = None
    fecha_fal: Optional[str] = None
    nacionalidad: Optional[str] = Field(None, max_length=50)
    descripcion: Optional[str] = None
    fotografia: Optional[str] = Field(None, max_length=255)
    estado: Optional[str] = None


class ArtistResponseDTO(ArtistBaseDTO):
    id_sql: int
