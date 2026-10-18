"""Domain service for Artist operations and business rules."""
from app.domain.models.artist import Artist
from app.domain.repositories.artist_repository import ArtistRepository
from app.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
    BusinessRuleConflictError,
)


class ArtistService:
    def __init__(self, artist_repo: ArtistRepository):
        self.artist_repo = artist_repo

    async def create_artist(self, artist: Artist, sync_mode: bool = False) -> Artist:
        existing = await self.artist_repo.get_by_id_sql(artist.id_sql)
        if existing and not sync_mode:
            raise EntityAlreadyExistsError(f"Artist with ID {artist.id_sql} is already registered.")
        if sync_mode:
            return await self.artist_repo.upsert(artist)
        return await self.artist_repo.create(artist)

    async def get_artist(self, id_sql: int) -> Artist:
        artist = await self.artist_repo.get_by_id_sql(id_sql)
        if not artist:
            raise EntityNotFoundError(f"Artist with ID {id_sql} not found.")
        return artist

    async def update_artist(self, id_sql: int, data: dict) -> Artist:
        await self.get_artist(id_sql)
        updated = await self.artist_repo.update(id_sql, data)
        return updated

    async def delete_artist(self, id_sql: int) -> bool:
        await self.get_artist(id_sql)
        has_works = await self.artist_repo.has_artworks(id_sql)
        if has_works:
            raise BusinessRuleConflictError(
                f"Cannot delete artist with ID {id_sql} because they have artworks registered in the catalog."
            )
        return await self.artist_repo.delete(id_sql)
