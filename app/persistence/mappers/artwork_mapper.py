from typing import Any
from app.persistence.entities.artwork_entity import ArtworkEntity
from app.domain.models.artwork import Artwork


class ArtworkMapper:
    @staticmethod
    def to_domain(entity: ArtworkEntity) -> Artwork:
        """Converts a persistence entity into an artwork domain model."""
        return Artwork(
            id_sql=entity.id_sql,
            genero_id=entity.genero_id,
            autor_id=entity.autor_id,
            nombre=entity.nombre,
            fecha_creacion=entity.fecha_creacion,
            precio_obra=entity.precio_obra,
            porcentaje_ganancia=entity.porcentaje_ganancia,
            estatus=entity.estatus,
            foto=entity.foto,
            detalles=entity.detalles,
        )

    @staticmethod
    def to_entity(domain: Artwork) -> ArtworkEntity:
        """Converts a domain model into a persistence entity."""
        return ArtworkEntity(
            id_sql=domain.id_sql,
            genero_id=domain.genero_id,
            autor_id=domain.autor_id,
            nombre=domain.nombre,
            fecha_creacion=domain.fecha_creacion,
            precio_obra=domain.precio_obra,
            porcentaje_ganancia=domain.porcentaje_ganancia,
            estatus=domain.estatus,
            foto=domain.foto,
            detalles=domain.detalles,
        )

    @staticmethod
    def to_document(domain: Artwork) -> dict[str, Any]:
        """Generates a clean BSON dictionary for MongoDB insertion/update."""
        entity = ArtworkMapper.to_entity(domain)
        return entity.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
