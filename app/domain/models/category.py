"""Category domain model."""
from pydantic import BaseModel, Field


class Category(BaseModel):
    id_sql: int = Field(..., description="Category ID in the core SQL database")
    detalles: list[str] = Field(..., description="List of mandatory polymorphic detail field names")
