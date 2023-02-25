"""Contiene funciones de utilidad para trabajar con formato json"""
import json
from constantes import UTF8

def read_json(json_file: str) -> dict[str,str]:
    """Abre el archivo json recibido como argumento y retorna un dict con el contenido"""
    with open(json_file, "r", encoding=UTF8) as fichero:
        datos = json.load(fichero)
        fichero.close()
        return datos

def write_json(json_file: str, json_data: dict, _encoding: str):
    """Vuelca los contenidos de json_data en el fichero json_file"""
    with open(json_file, "w", encoding=_encoding) as fichero:
        json.dump(json_data, fichero, indent=4)

def parse_jsonapi(json_data: any, request_url: str):
    """Adecua los datos json devueltos por una request a la especificación jsonapi"""
    json_data_openapi = {"jsonapi": {"version": 1.1},
                        "links": {"self": request_url},
                        "meta": {"copyright": "(C)2023 Master Fullstack Developer"
                                    ,"authors": ["Rubén Bermejo"]},
                        "data": json_data}
    return json_data_openapi
