from pydantic import BaseModel, Field
from typing import Optional


class CategoryBaseDTO(BaseModel):
    detalles: list[str] = Field(..., description="List of required dynamic field names")


class CategoryCreateDTO(CategoryBaseDTO):
    id_sql: int = Field(..., description="Category ID in core SQL database")


class CategoryUpdateDTO(BaseModel):
    detalles: Optional[list[str]] = None


class CategoryResponseDTO(CategoryBaseDTO):
    id_sql: int
