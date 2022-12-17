from io import StringIO

def guardar_pedido(nombre, apellidos):
    """ Escribe una línea con el formato "nombre apellidos " en el fichero "pedidos.txt" 
    
        Atributos:
            nombre: El nombre de la persona que hace el pedido
            apellidos: Los apellidos de la persona que hace el pedido
    """
    with open("pedidos.txt", "a", encoding="utf-8") as file:
        file.write(nombre + " " + apellidos + "\n")
        file.close()

def guardar_pedido_completo(pedido: object):
    """ Escribe una línea con el formato "nombre|apellidos|...|ingredientes " en el fichero "pedidos.txt" 
    
        Atributos:
            pedido: Objeto de la clase Pedido que contiene todos los datos del pedido
    """
    field_separator = "|"
    sb = StringBuilder()
    sb.append(pedido.nombre)
    sb.append(field_separator)
    sb.append(pedido.apellidos)
    sb.append(field_separator)
    sb.append(pedido.telefono)
    sb.append(field_separator)
    sb.append(pedido.nacimiento)
    sb.append(field_separator)
    sb.append(pedido.direccion)
    sb.append(field_separator)
    sb.append(pedido.tamano)
    sb.append(field_separator)
    sb.append(str(pedido.ingredientes))
    
    with open("pedidos.txt", "a", encoding="utf-8") as file:
        file.write(str(sb))
        file.close()

class StringBuilder:
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def append(self, str):
        self._file_str.write(str)

    def __str__(self):
        return self._file_str.getvalue()

class Pedido:
    """Esta clae define los datos de un pedido"""

    def __init__(self, nombre, apellidos):
        self.nombre = nombre
        self.apellidos = apellidos
        self.telefono = None;
        self.nacimiento = None;
        self.direccion = None;
        self.tamano = None;
        self.ingredientes = [];

    def __str__(self):
        detalles = ''
        detalles += f'Nombre               : {self.nombre}\n'
        detalles += f'Apellidos            : {self.apellidos}\n'
        detalles += f'Teléfono             : {self.telefono}\n'
        detalles += f'Fecha nacimiento     : {self.nacimiento}\n'
        detalles += f'Dirección            : {self.direccion}\n'
        detalles += f'Tamaño pizza         : {self.tamano}\n'
        detalles += f'Ingredientes         : {self.ingredientes}\n'
        return detalles
