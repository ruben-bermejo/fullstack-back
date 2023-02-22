"""Aplicación de almacén para solicitar artículos, su detalle y modificar su cantidad"""
import argparse
import json
from sqlite3 import Error
import yaml
from yaml.loader import SafeLoader
from flask import Flask, request, Response, jsonify, send_file
from flask_swagger_ui import get_swaggerui_blueprint
from marshmallow import ValidationError, INCLUDE
import persistencia
from validator import ArticuloSchema, check_authorization

app = Flask(__name__)

MIME_TYPE='application/json'
UNAUTHORIZED='Acción no permitida: No autenticado.'

SWAGGER_URL = '/api/docs'
API_URL = '/services/spec'

parser = argparse.ArgumentParser(description='Aplicación de Almacén del Equipo 3')
parser.add_argument('--servidor',
                    type=str,
                    metavar='localhost',
                    nargs='?',
                    const='localhost',
                    default='localhost',
                    help='IP o nombre del servidor donde se inicia la aplicación')
parser.add_argument('--puerto',
                    type=int,
                    nargs='?',
                    metavar='5000',
                    default=5000,
                    const=5000,
                    help='Puerto donde se expondrá el API')
parser.add_argument('--config',
                    type=str,
                    metavar='./config.yaml',
                    required=True,
                    help='Ruta y nombre del fichero de configuración de la aplicación')

args = parser.parse_args()

#Leemos el archivo de configuración
with open(args.config, "r", encoding="utf-8") as f:
    config_data = yaml.load(f, Loader=SafeLoader)
    f.close()

def convertir_articulo(body: any):
    '''Transforma un body request en JSON a Artículo'''
    # Recuperamos y validamos el body de la request como JSON
    result = ArticuloSchema(unknown=INCLUDE).load(body)

    # Convertimos el JSON a la clase Articulo
    return persistencia.Articulo.from_json(json.dumps(result, indent=4))

@app.route("/services/spec", methods=['GET'])
def swagger_yaml():
    """Recupera el archivo yaml"""
    return send_file('./api_doc.yaml')

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API Swagger Almacén"
    }
)

@app.route("/articulo", methods=['GET'])
def obtener_articulos():
    '''Busca todos los artículos en el almacén'''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        articulos = persistencia.get_articulos(config_data['basedatos'])
        return Response(json.dumps(articulos, indent=4),
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        mimetype=MIME_TYPE)
    return error_response(UNAUTHORIZED,401)

@app.route("/articulo/<id_articulo>", methods=['GET'])
def obtener_articulo(id_articulo):
    '''Busca en el almacén un artículo por su identificador único'''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        articulo = persistencia.get_articulo(config_data['basedatos'], id_articulo)
        if not articulo:
            return error_response(f'Artículo {id_articulo} no encontrado', 404)
        return Response(json.dumps(articulo, indent=4),
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        mimetype=MIME_TYPE)
    return error_response(UNAUTHORIZED,401)

@app.route("/articulo", methods=['POST'])
def crear_articulo():
    '''Servicio para crear un nuevo artículo
        - Campos obligatorios: nombre
        - Campos opcionales: articulo_id, detalle, stock, disponible
            - stock 0 por defecto
            - disponible False por defecto
    '''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        # Convertimos el JSON a la clase Articulo
        try:
            articulo = convertir_articulo(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400

        # Damos de alta el nuevo artículo si pasa las validaciones
        try:
            creado = persistencia.post_articulo(config_data['basedatos'], articulo)
            return Response(json.dumps(creado, indent=4),
                            201,
                            {'Access-Control-Allow-Origin':'*'},
                            mimetype=MIME_TYPE)
        except Error as sqlite_err:
            message = {"código": sqlite_err.sqlite_errorcode,
                        "error": sqlite_err.sqlite_errorname,
                        "mensaje": sqlite_err.args[0]}
            return Response(json.dumps(message, indent=4),
                                        400,
                                        {'Access-Control-Allow-Origin':'*'},
                                        mimetype=MIME_TYPE)
    return error_response(UNAUTHORIZED,401)

@app.route("/articulo/<id_articulo>", methods=['DELETE'])
def borrar_articulo(id_articulo):
    '''Servicio para eliminar un artículo'''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        persistencia.delete_articulo(config_data['basedatos'], id_articulo)
        return Response('¡Articulo eliminado correctamente!',
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        mimetype=MIME_TYPE)
    return error_response(UNAUTHORIZED,401)

@app.route("/articulo/<id_articulo>", methods=['PUT'])
def actualizar_articulo(id_articulo):
    '''Servicio para actualizar un artículo'''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        # Convertimos el JSON a la clase Articulo
        try:
            articulo = convertir_articulo(request.get_json())
        except ValidationError as err:
            return jsonify(err.messages), 400
        articulo.articulo_id = id_articulo
        modified = persistencia.put_articulo(config_data['basedatos'], articulo)
        return Response(json.dumps(modified, indent=4),
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        MIME_TYPE)
    return error_response(UNAUTHORIZED,401)

@app.route("/articulo/<id_articulo>/entrada_stock", methods=['PUT'])
def aumentar_stock_articulo(id_articulo):
    '''Servicio para aumentar el stock de un artículo'''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        cantidad = request.args.get("cantidad", default=0, type=int)
        if cantidad > 0:
            articulo = persistencia.get_articulo(config_data['basedatos'],id_articulo)
            if articulo:
                cantidad = cantidad + articulo['stock']
                mod = persistencia.put_articulo_stock(config_data['basedatos'],
                                id_articulo,
                                cantidad)
                return Response(json.dumps(mod, indent=4),
                                200,
                                {'Access-Control-Allow-Origin':'*'},
                                MIME_TYPE)
            return error_response('Artículo no encontrado',404)
        return error_response('La cantidad debe ser mayor que cero',400)
    return error_response(UNAUTHORIZED,401)

@app.route("/articulo/<id_articulo>/salida_stock", methods=['PUT'])
def disminuir_stock_articulo(id_articulo):
    '''Servicio para disminuir el stock de un artículo'''
    if check_authorization(request, config_data['basedatos']['consumidor_almacen_key']):
        cantidad = request.args.get("cantidad", default=0, type=int)
        if cantidad > 0:
            articulo = persistencia.get_articulo(config_data['basedatos'],id_articulo)
            if articulo:
                disponible = articulo['disponible']
                if disponible == 1:
                    cantidad = articulo['stock'] - cantidad
                    if cantidad >= 0:
                        mod = persistencia.put_articulo_stock(config_data['basedatos'],
                                        id_articulo,
                                        cantidad)
                        return Response(json.dumps(mod, indent=4),
                                        200,
                                        {'Access-Control-Allow-Origin':'*'},
                                        MIME_TYPE)
                    return error_response('No hay suficiente stock del artículo seleccionado',400)
                return error_response('El artículo no está disponible actualmente',400)
            return error_response('Artículo no encontrado',404)
        return error_response('La cantidad debe ser mayor que cero',400)
    return error_response(UNAUTHORIZED,401)

def error_response(message: str, code: int):
    '''Respuesta de error'''
    return Response(message,
            code,
            {'Access-Control-Allow-Origin':'*'},
            MIME_TYPE)

app.register_blueprint(swaggerui_blueprint)
app.run(host=args.servidor, port=args.puerto)
