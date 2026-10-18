from typing import Any
from app.persistence.entities.artist_entity import ArtistEntity
from app.domain.models.artist import Artist


class ArtistMapper:
    @staticmethod
    def to_domain(entity: ArtistEntity) -> Artist:
        """Converts a persistence entity into a pure domain model."""
        return Artist(
            id_sql=entity.id_sql,
            nombre=entity.nombre,
            apellido=entity.apellido,
            fecha_nac=entity.fecha_nac,
            fecha_fal=entity.fecha_fal,
            nacionalidad=entity.nacionalidad,
            descripcion=entity.descripcion,
            fotografia=entity.fotografia,
            estado=entity.estado,
        )

    @staticmethod
    def to_entity(domain: Artist) -> ArtistEntity:
        """Converts a domain model into a persistence entity."""
        return ArtistEntity(
            id_sql=domain.id_sql,
            nombre=domain.nombre,
            apellido=domain.apellido,
            fecha_nac=domain.fecha_nac,
            fecha_fal=domain.fecha_fal,
            nacionalidad=domain.nacionalidad,
            descripcion=domain.descripcion,
            fotografia=domain.fotografia,
            estado=domain.estado,
        )

    @staticmethod
    def to_document(domain: Artist) -> dict[str, Any]:
        """Generates a clean BSON dictionary for MongoDB insertion/update."""
        entity = ArtistMapper.to_entity(domain)
        return entity.model_dump(by_alias=True, exclude_none=True, exclude={"id"})
