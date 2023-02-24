"""Clase para las operaciones con la base de datos de la tienda"""
import sqlite3
import dataclasses
from typing import Optional
from io import StringIO
import dataclasses_json

OPERACION_CANCELADA = 'Operación cancelada. Se encontró más de un registro para actualizar.'

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Producto:
    """Esta clase define los datos de un producto"""
    nombre: str
    articulo_id: int
    precio: Optional[int] = 0
    disponibles: Optional[int] = 0
    vendidas: Optional[int] = 0
    producto_id: Optional[int] = None

    def imprimir(self):
        """Imprime por consola el detalle del PRODUCTO"""
        detalles = ''
        detalles += f'Id                   : {self.producto_id}\n'
        detalles += f'Nombre               : {self.nombre}\n'
        detalles += f'Articulo Id          : {self.articulo_id}\n'
        detalles += f'Disponibles          : {self.disponibles}\n'
        detalles += f'Vendidas             : {self.vendidas}\n'
        detalles += f'Precio               : {self.precio}\n'
        print(detalles)

class StringBuilder:
    """Clase para constuir strings"""
    _file_str = None

    def __init__(self):
        self._file_str = StringIO()

    def append(self, texto: str):
        """Función para concatenar un string al final de otro"""
        self._file_str.write(texto)

    def to_string(self):
        """Función para convertir el StringBuilder a string"""
        return self._file_str.getvalue()

def obtener_conexion(db_config: dict):
    '''Obtiene la conexión e inicia la base de datos con la tabla PRODUCTO si no existe'''
    conn = sqlite3.connect(db_config['path'])
    try:
        cur = conn.cursor()
        create_table = StringBuilder()
        create_table.append('CREATE TABLE IF NOT EXISTS PRODUCTO')
        create_table.append(' (productoId INTEGER PRIMARY KEY,')
        create_table.append(' nombre TEXT UNIQUE NOT NULL,')
        create_table.append(' precio REAL NOT NULL DEFAULT 0,')
        create_table.append(' disponibles INTEGER,')
        create_table.append(' vendidas INTEGER DEFAULT 0,')
        create_table.append(' articuloId INTEGER UNIQUE NOT NULL)')
        cur.execute(create_table.to_string())
    except Exception as exc:
        print(f"No pudo crearse la tabla PRODUCTO debido a: {exc}")
        raise exc
    finally:
        cur.close()

    return conn

def get_productos(db_config: dict):
    '''Obtiene todos los elementos de la tabla PRODUCTO'''
    productos = []
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        result = cur.execute('''SELECT nombre,
                                    articuloId,
                                    precio,
                                    disponibles,
                                    vendidas,
                                    productoId FROM PRODUCTO''')
        for row in result:
            producto = Producto(*row)
            productos.append(producto.to_dict())
    except Exception as exc:
        print(f"No se pudo recuperar los productos debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()
    return productos

def get_producto(db_config: dict, producto_id: int):
    '''Obtiene un elemento de la tabla PRODUCTO'''
    productos = {}
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        result = cur.execute('''SELECT nombre,
                                    articuloId,
                                    precio,
                                    disponibles,
                                    vendidas,
                                    productoId
                                 FROM PRODUCTO 
                                 WHERE productoId=?''', (producto_id,))
        row = result.fetchone()
        if row is not None:
            producto = Producto(*row)
            productos.update(producto.to_dict())
    except Exception as exc:
        print(f"No se pudo recuperar el producto debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()
    return productos

def delete_producto(db_config: dict, producto_id: int):
    '''Elimina un elemento de la tabla PRODUCTO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        cur.execute("DELETE FROM PRODUCTO WHERE productoId=?", (producto_id,))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError('Operación cancelada. Se encontró más de un registro para eliminar.')
    except Exception as exc:
        print(f"No se pudo eliminar el producto debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def put_cambiar_precio(db_config: dict, producto_id: int, precio: float):
    '''Actualiza el precio de un PRODUCTO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''UPDATE PRODUCTO
                     SET precio = ?
                 WHERE productoId = ?'''
        cur.execute(sql, (precio, producto_id))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError(OPERACION_CANCELADA)
        return get_producto(db_config, producto_id)
    except Exception as exc:
        print(f"No se pudo actualizar el producto debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def put_vender_producto(db_config: dict, producto_id: int):
    '''Representa la venta de un PRODUCTO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''UPDATE PRODUCTO
                     SET disponibles = disponibles - 1,
                        vendidas = vendidas + 1
                 WHERE productoId = ?'''
        cur.execute(sql, (producto_id))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError(OPERACION_CANCELADA)
        return get_producto(db_config, producto_id)
    except Exception as exc:
        print(f"No se pudo actualizar el producto debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def put_recibir_producto(db_config: dict, producto_id: int, cantidad: int):
    '''Representa la recepción de una cantidad de unidades del PRODUCTO al ALMACÉN'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''UPDATE PRODUCTO
                     SET disponibles = disponibles + ?
                 WHERE productoId = ?'''
        cur.execute(sql, (cantidad, producto_id))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError(OPERACION_CANCELADA)
        return get_producto(db_config, producto_id)
    except Exception as exc:
        print(f"No se pudo actualizar el producto debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def put_crear_producto(db_config: dict, disponibles: int, nombre: str, articulo_id: int):
    '''Representa la recepción de un nuevo PRODUCTO desde el ALMACÉN'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''INSERT INTO PRODUCTO
                                 (nombre, articuloId, disponibles) 
                                 VALUES (?,?,?)'''
        cur.execute(sql, (nombre, articulo_id, disponibles))
        conn.commit()
        return get_producto(db_config, cur.lastrowid)
    except Exception as exc:
        print(f"No se pudo crear el producto debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()
