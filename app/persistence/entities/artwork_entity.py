from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any


class ArtworkEntity(BaseModel):
    """Modelo físico que representa el documento de Obra en MongoDB."""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[Any] = Field(None, alias="_id")
    id_sql: int
    genero_id: int
    autor_id: int
    nombre: str
    fecha_creacion: Optional[str] = None
    precio_obra: float
    porcentaje_ganancia: Optional[float] = None
    estatus: str = "Disponible"
    foto: Optional[str] = None
    detalles: dict[str, str] = Field(default_factory=dict)
