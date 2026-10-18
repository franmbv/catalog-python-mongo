from app.domain.models import Artist, Category, Artwork
from app.persistence.entities import ArtistEntity, CategoryEntity, ArtworkEntity
from app.persistence.mappers import ArtistMapper, CategoryMapper, ArtworkMapper


def test_artist_mapper_bidirectional():
    domain_artist = Artist(
        id_sql=10,
        nombre="Pablo",
        apellido="Picasso",
        nacionalidad="Española",
        estado="Inactivo",
    )

    # Domain -> Entity
    entity = ArtistMapper.to_entity(domain_artist)
    assert isinstance(entity, ArtistEntity)
    assert entity.id_sql == 10
    assert entity.nombre == "Pablo"

    # Entity -> Domain
    reconstructed = ArtistMapper.to_domain(entity)
    assert isinstance(reconstructed, Artist)
    assert reconstructed.id_sql == 10
    assert reconstructed.nombre == "Pablo"

    # Domain -> BSON Document for MongoDB
    doc = ArtistMapper.to_document(domain_artist)
    assert "_id" not in doc
    assert doc["id_sql"] == 10


def test_category_mapper_bidirectional():
    domain_cat = Category(id_sql=3, detalles=["tecnica", "material"])
    entity = CategoryMapper.to_entity(domain_cat)
    assert isinstance(entity, CategoryEntity)
    assert entity.detalles == ["tecnica", "material"]

    reconstructed = CategoryMapper.to_domain(entity)
    assert reconstructed.id_sql == 3
    assert reconstructed.detalles == ["tecnica", "material"]


def test_artwork_mapper_bidirectional():
    domain_art = Artwork(
        id_sql=50,
        genero_id=2,
        autor_id=1,
        nombre="Guernica",
        precio_obra=100000.0,
        detalles={"tecnica": "óleo", "soporte": "lienzo"},
    )
    entity = ArtworkMapper.to_entity(domain_art)
    assert isinstance(entity, ArtworkEntity)
    assert entity.nombre == "Guernica"

    reconstructed = ArtworkMapper.to_domain(entity)
    assert reconstructed.detalles["tecnica"] == "óleo"
