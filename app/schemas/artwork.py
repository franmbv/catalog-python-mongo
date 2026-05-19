from pydantic import BaseModel,Field
#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

#ArtworkBase
#Lo que se definira aqui es: 
# id_sql - Tipo entero 
# id_category - Tipo entero
# detalles - Tipo lista dict/diccionarios

#ArtworkCreate
#Este 'scheme' heredara simplemente de 'ArtworkBase'

#ArtworkResponse
#Este 'scheme' heredara simplemente de 'ArtworkBase'


class ArtworkBase(BaseModel):
    """
    Schema base que define la estructura común para las obras de arte.
    Cruza los datos del Core en Node.js con los detalles dinámicos en Mongo.
    """
    id_sql: int = Field(
        ..., 
        description="Identificador único correlativo proveniente de la base de datos relacional de Node.js"
    )
    id_category: int = Field(
        ..., 
        description="ID SQL de la categoría a la que pertenece esta obra"
    )
    detalles: dict[str, str] = Field(
        ..., 
        description="Lista de strings que almacena las características y detalles dinámicos de la obra"
    )

class ArtworkCreate(ArtworkBase):
    """
    Schema utilizado para la creación de nuevas obras en el microservicio.
    Hereda directamente de ArtworkBase sin campos adicionales por ahora.
    """
    pass

class ArtworkResponse(ArtworkBase):
    """
    Schema utilizado para estructurar las respuestas HTTP enviadas al cliente.
    Hereda directamente de ArtworkBase sin campos adicionales por ahora.
    """
    pass