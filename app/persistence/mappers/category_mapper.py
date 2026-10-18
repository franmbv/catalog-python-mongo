from typing import Any
from app.persistence.entities.category_entity import CategoryEntity
from app.domain.models.category import Category


class CategoryMapper:
    @staticmethod
    def to_domain(entity: CategoryEntity) -> Category:
        """Converts a persistence entity into a category domain model."""
        return Category(
            id_sql=entity.id_sql,
            detalles=entity.detalles,
        )

    @staticmethod
    def to_entity(domain: Category) -> CategoryEntity:
        """Converts a domain model into a persistence entity."""
        return CategoryEntity(
            id_sql=domain.id_sql,
            detalles=domain.detalles,
        )

    @staticmethod
    def to_document(domain: Category) -> dict[str, Any]:
        """Generates a clean BSON dictionary for MongoDB insertion/update."""
        entity = CategoryMapper.to_entity(domain)
        return entity.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
