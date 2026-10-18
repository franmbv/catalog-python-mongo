from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any


class CategoryEntity(BaseModel):
    """Modelo físico que representa el documento de Categoría en MongoDB."""
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    id: Optional[Any] = Field(None, alias="_id")
    id_sql: int
    detalles: list[str]
