"""Clase para las operaciones con la base de datos del Almacén"""
import sqlite3
import dataclasses
from typing import Optional
from io import StringIO
import dataclasses_json

@dataclasses_json.dataclass_json
@dataclasses.dataclass
class Articulo:
    """Esta clase define los datos de un artículo"""
    nombre: str
    detalle: Optional[str] = None
    stock: Optional[int] = 0
    disponible: Optional[bool] = False
    articulo_id: Optional[int] = None

    def imprimir(self):
        """Imprime por consola el detalle del artículo"""
        detalles = ''
        detalles += f'Id                   : {self.articulo_id}\n'
        detalles += f'Nombre               : {self.nombre}\n'
        detalles += f'Detalle              : {self.detalle}\n'
        detalles += f'Stock                : {self.stock}\n'
        detalles += f'Disponible           : {self.disponible}\n'
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
    '''Obtiene la conexión e inicia la base de datos con la tabla ARTICULO si no existe'''
    conn = sqlite3.connect(db_config['path'])
    try:
        cur = conn.cursor()
        create_table = StringBuilder()
        create_table.append('CREATE TABLE IF NOT EXISTS ARTICULO')
        create_table.append(' (articuloId INTEGER PRIMARY KEY,')
        create_table.append(' nombre TEXT UNIQUE NOT NULL,')
        create_table.append(' detalle TEXT,')
        create_table.append(' stock INTEGER NOT NULL,')
        create_table.append(' disponible BOOLEAN NOT NULL)')
        cur.execute(create_table.to_string())
    except Exception as exc:
        print(f"No pudo crearse la tabla ARTICULO debido a: {exc}")
        raise exc
    finally:
        cur.close()

    return conn

def get_articulos(db_config: dict):
    '''Obtiene todos los elementos de la tabla ARTICULO'''
    articulos = []
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        result = cur.execute("SELECT nombre,detalle,stock,disponible,articuloId FROM ARTICULO")
        for row in result:
            articulo = Articulo(*row)
            articulos.append(articulo.to_dict())
    except Exception as exc:
        print(f"No se pudo recuperar los articulos debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()
    return articulos

def get_articulo(db_config: dict, articulo_id: int):
    '''Obtiene un elemento de la tabla ARTICULO'''
    articulos = {}
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        result = cur.execute('''SELECT nombre,
                                    detalle,
                                    stock,
                                    CASE disponible when 1 then true
                                    else false
                                    end as disponible,
                                    articuloId
                                 FROM ARTICULO 
                                 WHERE articuloId=?''', (articulo_id,))
        row = result.fetchone()
        if row is not None:
            articulo = Articulo(*row)
            articulos.update(articulo.to_dict())
    except Exception as exc:
        print(f"No se pudo recuperar el artículo debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()
    return articulos

def delete_articulo(db_config: dict, articulo_id: int):
    '''Elimina un elemento de la tabla ARTICULO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        cur.execute("DELETE FROM ARTICULO WHERE articuloId=?", (articulo_id,))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError('Operación cancelada. Se encontró más de un registro para eliminar.')
    except Exception as exc:
        print(f"No se pudo eliminar el artículo debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def post_articulo(db_config: dict, data: Articulo):
    '''Crea un nuevo elemento en la tabla ARTICULO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''INSERT INTO ARTICULO
                                 (nombre, detalle, stock, disponible) 
                                 VALUES (?,?,?,?)'''
        cur.execute(sql, (data.nombre, data.detalle, data.stock, data.disponible))
        conn.commit()
        return get_articulo(db_config, cur.lastrowid)
    except Exception as exc:
        print(f"No se pudo crear el artículo debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def put_articulo(db_config: dict, data: Articulo):
    '''Actualiza nombre, detalle y disponibilidad de un elemento de la tabla ARTICULO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''UPDATE ARTICULO
                     SET nombre = ?,
                     detalle = ?,
                     disponible = ?
                 WHERE articuloId = ?'''
        cur.execute(sql, (data.nombre, data.detalle, data.disponible, data.articulo_id))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError('Operación cancelada. Se encontró más de un registro para actualizar.')
        return get_articulo(db_config, data.articulo_id)
    except Exception as exc:
        print(f"No se pudo actualizar el artículo debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()

def put_articulo_stock(db_config: dict, articulo_id: int, cantidad: int):
    '''Actualiza el stock de un elemento de la tabla ARTICULO'''
    try:
        conn = obtener_conexion(db_config)
        cur = conn.cursor()
        sql = '''UPDATE ARTICULO
                     SET stock = ?
                 WHERE articuloId = ?'''
        cur.execute(sql, (cantidad, articulo_id))
        if cur.rowcount <= 1:
            conn.commit()
        else:
            conn.rollback()
            raise ValueError('Operación cancelada. Se encontró más de un registro para actualizar.')
        return get_articulo(db_config, articulo_id)
    except Exception as exc:
        print(f"No se pudo actualizar el artículo debido a {exc}")
        raise exc
    finally:
        cur.close()
        conn.close()
