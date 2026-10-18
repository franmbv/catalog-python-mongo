"""Domain service for Artwork operations and polymorphic validation."""
from app.domain.models.artwork import Artwork
from app.domain.models.category import Category
from app.domain.repositories.artwork_repository import ArtworkRepository
from app.domain.repositories.artist_repository import ArtistRepository
from app.domain.repositories.category_repository import CategoryRepository
from app.domain.exceptions.domain_exceptions import (
    EntityNotFoundError,
    EntityAlreadyExistsError,
    InvalidPolymorphicDetailsError,
)


class ArtworkService:
    def __init__(
        self,
        artwork_repo: ArtworkRepository,
        artist_repo: ArtistRepository,
        category_repo: CategoryRepository,
    ):
        self.artwork_repo = artwork_repo
        self.artist_repo = artist_repo
        self.category_repo = category_repo

    def validate_polymorphic_details(self, category: Category, detalles: dict[str, str]) -> None:
        """Verifies that all required fields for the category are present in details."""
        for campo in category.detalles:
            if campo not in detalles or detalles[campo] is None:
                raise InvalidPolymorphicDetailsError(
                    f"Polymorphic schema validation failed: the field '{campo}' is required for category {category.id_sql}."
                )

    async def create_artwork(self, artwork: Artwork, sync_mode: bool = False) -> Artwork:
        existing = await self.artwork_repo.get_by_id_sql(artwork.id_sql)
        if existing and not sync_mode:
            raise EntityAlreadyExistsError(f"Artwork with ID {artwork.id_sql} is already registered.")

        # Validate artist existence
        artist = await self.artist_repo.get_by_id_sql(artwork.autor_id)
        if not artist:
            raise EntityNotFoundError(f"Artist with ID {artwork.autor_id} does not exist.")

        # Validate category existence
        category = await self.category_repo.get_by_id_sql(artwork.genero_id)
        if not category:
            raise EntityNotFoundError(f"Category with ID {artwork.genero_id} does not exist.")

        # Validate polymorphic rule
        self.validate_polymorphic_details(category, artwork.detalles)

        if sync_mode:
            return await self.artwork_repo.upsert(artwork)
        return await self.artwork_repo.create(artwork)

    async def get_artwork(self, id_sql: int) -> Artwork:
        artwork = await self.artwork_repo.get_by_id_sql(id_sql)
        if not artwork:
            raise EntityNotFoundError(f"Artwork with ID {id_sql} not found.")
        return artwork

    async def update_artwork(self, id_sql: int, data: dict) -> Artwork:
        current = await self.get_artwork(id_sql)

        target_autor_id = data.get("autor_id", current.autor_id)
        target_genero_id = data.get("genero_id", current.genero_id)
        target_detalles = data.get("detalles", current.detalles)

        # Validate author and category if modified
        artist = await self.artist_repo.get_by_id_sql(target_autor_id)
        if not artist:
            raise EntityNotFoundError(f"Artist with ID {target_autor_id} does not exist.")

        category = await self.category_repo.get_by_id_sql(target_genero_id)
        if not category:
            raise EntityNotFoundError(f"Category with ID {target_genero_id} does not exist.")

        # Re-validate polymorphic details
        self.validate_polymorphic_details(category, target_detalles)

        return await self.artwork_repo.update(id_sql, data)

    async def delete_artwork(self, id_sql: int) -> bool:
        await self.get_artwork(id_sql)
        return await self.artwork_repo.delete(id_sql)
