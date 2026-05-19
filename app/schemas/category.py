from pydantic import BaseModel,Field
#Importante utilizar solo esas importaciones para realizar los Schemas
#De aqui para abajo, se deben realizar los 'Schemas'
#Para cosas opcionales utilizar el operador: '|' que significa 'O'

#CategoryBase
#Lo que se definira aqui es: 
# id_sql - Tipo entero 
# detalles - Tipo lista de string (list[str])

#CategoryCreate
#Este 'scheme' heredara simplemente de 'CategoryBase'

#CategoryResponse
#Este 'scheme' heredara simplemente de 'CategoryBase'


