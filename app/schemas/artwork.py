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
