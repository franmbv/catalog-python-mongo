from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any


class ArtistEntity(BaseModel):
    """Modelo físico que representa el documento de Artista en MongoDB."""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[Any] = Field(None, alias="_id")
    id_sql: int
    nombre: str
    apellido: str
    fecha_nac: Optional[str] = None
    fecha_fal: Optional[str] = None
    nacionalidad: Optional[str] = None
    descripcion: Optional[str] = None
    fotografia: Optional[str] = None
    estado: str = "Activo"
