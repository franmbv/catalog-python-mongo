import pytest
from unittest.mock import AsyncMock
from app.domain.models import Artist, Category, Artwork
from app.domain.services import ArtistService, CategoryService, ArtworkService, CatalogService
from app.domain.exceptions import (
    EntityNotFoundError,
    InvalidPolymorphicDetailsError,
    BusinessRuleConflictError,
)


@pytest.fixture
def mock_repos():
    artist_repo = AsyncMock()
    category_repo = AsyncMock()
    artwork_repo = AsyncMock()
    catalog_repo = AsyncMock()
    return artist_repo, category_repo, artwork_repo, catalog_repo


@pytest.mark.asyncio
async def test_create_artwork_valid_polymorphic(mock_repos):
    artist_repo, category_repo, artwork_repo, _ = mock_repos
    service = ArtworkService(artwork_repo, artist_repo, category_repo)

    # Setup mocks
    artist_repo.get_by_id_sql.return_value = Artist(id_sql=1, nombre="Carlos", apellido="Mendoza")
    category_repo.get_by_id_sql.return_value = Category(id_sql=1, detalles=["tecnica", "soporte"])
    artwork_repo.get_by_id_sql.return_value = None
    artwork_repo.create.side_effect = lambda art: art

    artwork = Artwork(
        id_sql=100,
        genero_id=1,
        autor_id=1,
        nombre="El Sol",
        precio_obra=5000.0,
        detalles={"tecnica": "óleo", "soporte": "lienzo"},
    )

    result = await service.create_artwork(artwork)
    assert result.nombre == "El Sol"
    artwork_repo.create.assert_awaited_once_with(artwork)


@pytest.mark.asyncio
async def test_create_artwork_fails_missing_polymorphic_detail(mock_repos):
    artist_repo, category_repo, artwork_repo, _ = mock_repos
    service = ArtworkService(artwork_repo, artist_repo, category_repo)

    artist_repo.get_by_id_sql.return_value = Artist(id_sql=1, nombre="Carlos", apellido="Mendoza")
    category_repo.get_by_id_sql.return_value = Category(id_sql=1, detalles=["tecnica", "soporte"])
    artwork_repo.get_by_id_sql.return_value = None

    # Missing 'soporte'
    artwork = Artwork(
        id_sql=101,
        genero_id=1,
        autor_id=1,
        nombre="Incompleta",
        precio_obra=3000.0,
        detalles={"tecnica": "óleo"},
    )

    with pytest.raises(InvalidPolymorphicDetailsError):
        await service.create_artwork(artwork)


@pytest.mark.asyncio
async def test_delete_artist_with_artworks_fails(mock_repos):
    artist_repo, _, _, _ = mock_repos
    service = ArtistService(artist_repo)

    artist_repo.get_by_id_sql.return_value = Artist(id_sql=5, nombre="Diego", apellido="Torres")
    artist_repo.has_artworks.return_value = True

    with pytest.raises(BusinessRuleConflictError):
        await service.delete_artist(5)
