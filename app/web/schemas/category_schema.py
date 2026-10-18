from pydantic import BaseModel, Field
from typing import Optional


class CategoryBaseDTO(BaseModel):
    detalles: list[str] = Field(..., description="Lista de nombres de campos requeridos")


class CategoryCreateDTO(CategoryBaseDTO):
    id_sql: int = Field(..., description="ID de la categoría en el núcleo SQL")


class CategoryUpdateDTO(BaseModel):
    detalles: Optional[list[str]] = None


class CategoryResponseDTO(CategoryBaseDTO):
    id_sql: int
