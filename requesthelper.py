"""Clase de utilidad para las peticiones http"""
from requests import get, put, post, delete, Response
from jsonhelper import read_json

def do_request(_url: str, method: str, input_file: str, tout: int):
    """Realiza una llamada http con los datos proporcionados y devuelve la respuesta"""
    match method:
        case 'GET':
            response_data = get(url = _url, timeout = tout)
        case 'DELETE':
            response_data = delete(url = _url, timeout = tout)
        case 'POST':
            #Recuperamos los datos enviar para crear el recurso
            post_data=read_json(input_file)
            response_data = post(url = _url, timeout = tout, json = post_data)
        case 'PUT':
            #Recuperamos los datos enviar para modificar el recurso
            put_data=read_json(input_file)
            response_data = put(url = _url, timeout = tout, json = put_data)
    return response_data

def parse_response(response: Response, _url: str, method: str):
    """Construye un dict con los datos que necesitamos para grabar la respuesta"""
    parsed_response = {}
    parsed_response['method'] = method
    parsed_response['url'] = _url
    parsed_response['status'] = response.status_code
    parsed_response['content-type'] = response.headers['Content-Type']
    parsed_response['encoding'] = response.encoding
    return parsed_response
