"""Herramientas principales para trabajar con streams"""
import dataclasses
from io import StringIO

FIELD_SEPARATOR="|"

def guardar_pedido(nombre, apellidos):
    """Escribe una línea con el formato "nombre apellidos " en el fichero "pedidos.txt"
        Atributos:
            nombre: El nombre de la persona que hace el pedido
            apellidos: Los apellidos de la persona que hace el pedido
    """
    with open("pedidos.txt", "a", encoding="utf-8") as file:
        file.write(nombre + " " + apellidos + "\n")
        file.close()

def guardar_pedido_completo(pedido: object):
    """Escribe una línea con el formato "nombre|apellidos|..." en el fichero "pedidos.txt"
        Atributos:
            pedido: Objeto de la clase Pedido que contiene todos los datos del pedido
    """
    linea_pedido = StringBuilder()
    linea_pedido.append(pedido.nombre)
    linea_pedido.append(FIELD_SEPARATOR)
    linea_pedido.append(pedido.apellidos)
    linea_pedido.append(FIELD_SEPARATOR)
    linea_pedido.append(pedido.telefono)
    linea_pedido.append(FIELD_SEPARATOR)
    linea_pedido.append(pedido.nacimiento)
    linea_pedido.append(FIELD_SEPARATOR)
    linea_pedido.append(pedido.direccion)
    linea_pedido.append(FIELD_SEPARATOR)
    linea_pedido.append(pedido.tamano)
    linea_pedido.append(FIELD_SEPARATOR)
    linea_pedido.append(str(pedido.ingredientes))
    with open("pedidos.txt", "a", encoding="utf-8") as file:
        file.write(linea_pedido.to_string())
        file.close()

class StringBuilder:
    """Clase para constuir strings"""
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def append(self, str):
        """Función para concatenar un string al final de otro"""
        self._file_str.write(str)

    def to_string(self):
        """Función para convertir el StringBuilder a string"""
        return self._file_str.getvalue()

@dataclasses.dataclass
class Pedido:
    """Esta clase define los datos de un pedido"""
    nombre = str
    apellidos = str
    telefono = int
    nacimiento = str
    direccion = str
    tamano = str
    ingredientes = set

    def iniciar(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = None
        self.nacimiento = None
        self.direccion = None
        self.tamano = None
        self.ingredientes = []

    def imprimir(self):
        detalles = ''
        detalles += f'Nombre               : {self.nombre}\n'
        detalles += f'Apellidos            : {self.apellidos}\n'
        detalles += f'Teléfono             : {self.telefono}\n'
        detalles += f'Fecha nacimiento     : {self.nacimiento}\n'
        detalles += f'Dirección            : {self.direccion}\n'
        detalles += f'Tamaño pizza         : {self.tamano}\n'
        detalles += f'Ingredientes         : {self.ingredientes}\n'
        print(detalles)
