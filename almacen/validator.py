'''Clase para validaciones de las operaciones en la aplicación Almacén'''
from marshmallow import Schema, fields, ValidationError, validates
from flask import request

class ArticuloSchema(Schema):
    '''Esquema de validación para los datos del Articulo'''
    articulo_id = fields.Integer()
    nombre = fields.String(required = True)
    detalle = fields.String()
    stock = fields.Integer()
    disponible = fields.Boolean()

    @validates("nombre")
    def validate_nombre(self, value):
        '''Validador para el campo nombre'''
        if not value.strip():
            raise ValidationError("El nombre no puede estar vacío.")

    @validates("stock")
    def validate_stock(self, value):
        '''Validador para el campo stock'''
        if value < 0:
            raise ValidationError("El stock debe ser igual o mayor a cero.")

    @validates("articulo_id")
    def validate_id(self, value):
        '''Validador para el campo articulo_id'''
        if value <= 0:
            raise ValidationError("El articulo_id no existe: " + str(value))

def check_authorization(req: request, pwd: str):
    '''Comprueba si es una consulta autenticada al API'''
    autenticado = False
    key = req.headers.get('api-key-warehouse')
    if key == pwd:
        autenticado = True
    return autenticado
