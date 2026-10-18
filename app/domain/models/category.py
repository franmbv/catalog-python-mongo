"""Category domain model."""
from pydantic import BaseModel, Field


class Category(BaseModel):
    id_sql: int = Field(..., description="ID de la categoría en el núcleo SQL")
    detalles: list[str] = Field(..., description="Lista de nombres de campos polimórficos obligatorios")
