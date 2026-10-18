from typing import Any
from app.persistence.entities.category_entity import CategoryEntity
from app.domain.models.category import Category


class CategoryMapper:
    @staticmethod
    def to_domain(entity: CategoryEntity) -> Category:
        """Convierte una entidad de persistencia en un modelo de dominio de categoría."""
        return Category(
            id_sql=entity.id_sql,
            detalles=entity.detalles,
        )

    @staticmethod
    def to_entity(domain: Category) -> CategoryEntity:
        """Convierte un modelo de dominio en una entidad de persistencia."""
        return CategoryEntity(
            id_sql=domain.id_sql,
            detalles=domain.detalles,
        )

    @staticmethod
    def to_document(domain: Category) -> dict[str, Any]:
        """Genera el diccionario BSON para guardar en MongoDB."""
        entity = CategoryMapper.to_entity(domain)
        return entity.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
