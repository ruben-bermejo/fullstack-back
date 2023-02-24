"""Aplicación de tienda para vender productos de un almacén"""
import argparse
import json
from flask import Flask, request, Response, send_file
from flask_swagger_ui import get_swaggerui_blueprint
import yaml
from yaml.loader import SafeLoader
from requests import get, put
import persist_tienda

app = Flask(__name__)

MIME_TYPE='application/json'
UNAUTHORIZED='Acción no permitida: No autenticado.'

SWAGGER_URL = '/api/docs'
API_URL = '/services/spec'

parser = argparse.ArgumentParser(description='Aplicación de Tienda del Equipo 3')
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
                    metavar='5001',
                    default=5001,
                    const=5001,
                    help='Puerto donde se expondrá el API')
parser.add_argument('--config',
                    type=str,
                    metavar='./config.yaml',
                    required=True,
                    help='Ruta y nombre del fichero de configuración de la aplicación')
parser.add_argument('--key',
                    type=str,
                    metavar='api_key',
                    required=True,
                    help='Valor del API KEY para consumir servicios del Almacén')

args = parser.parse_args()

#Leemos el archivo de configuración
with open(args.config, "r", encoding="utf-8") as f:
    config_data = yaml.load(f, Loader=SafeLoader)
    f.close()

@app.route("/services/spec", methods=['GET'])
def swagger_yaml():
    """Recupera el archivo yaml"""
    return send_file('./api_doc.yaml')

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API Swagger Tienda"
    }
)

@app.before_first_request
def init_database():
    '''Si no hay productos invoca los servicios de Almacén para traspasar un
        máximo de 2 unidades de cada artículo'''
    print('Iniciando aplicación tienda')
    productos = persist_tienda.get_productos(config_data['basedatos'])
    if not productos:
        print('No hay productos. Cargando desde el almacén')
        url_articulo = config_data['almacen']['base_url'] + '/articles'
        response_data = get(url = url_articulo,
                        timeout = 60,
                        headers = config_data['almacen']['api_key'])
        print(response_data)              
        articulos = response_data.json()
        for articulo in articulos:
            if articulo['available'] == 1 and articulo['units'] > 0:
                solicitadas = min(articulo['units'], 2)
                put(url = url_articulo
                            + '/send/'
                            + str(articulo['id']),
                        timeout = 60,
                        headers = config_data['almacen']['api_key'],
                        json = {'cantidad': solicitadas})
                persist_tienda.put_crear_producto(config_data['basedatos'],
                                    solicitadas,
                                    articulo['article_info'],
                                    articulo['id'])

@app.route("/producto", methods=['GET'])
def obtener_productos():
    '''Busca todos los productos en la tienda'''
    productos = persist_tienda.get_productos(config_data['basedatos'])
    return Response(json.dumps(productos, indent=4),
                    200,
                    {'Access-Control-Allow-Origin':'*'},
                    mimetype=MIME_TYPE)

@app.route("/producto/<id_producto>", methods=['GET'])
def obtener_producto(id_producto):
    '''Busca en la tienda un producto por su identificador único'''
    producto = persist_tienda.get_producto(config_data['basedatos'], id_producto)
    if not producto:
        return error_response(f'Producto {id_producto} no encontrado', 404)
    return Response(json.dumps(producto, indent=4),
                    200,
                    {'Access-Control-Allow-Origin':'*'},
                    mimetype=MIME_TYPE)

@app.route("/producto/<id_producto>", methods=['DELETE'])
def borrar_producto(id_producto):
    '''Servicio para eliminar un producto'''
    persist_tienda.delete_producto(config_data['basedatos'], id_producto)
    return Response('¡Producto eliminado correctamente!',
                    200,
                    {'Access-Control-Allow-Origin':'*'},
                    mimetype=MIME_TYPE)

@app.route("/producto/<id_producto>/vender", methods=['PUT'])
def vender_producto(id_producto):
    '''Servicio para vender un producto
        Verifica que hay unidades disponibles
        Verifica que tiene precio
        Decrementa disponibles e incrementa vendidas'''
    producto = persist_tienda.get_producto(config_data['basedatos'], id_producto)
    if not producto:
        return error_response(f'Producto {id_producto} no encontrado', 404)
    if producto['disponibles'] > 0 and producto['precio'] > 0:
        modificado = persist_tienda.put_vender_producto(config_data['basedatos'], id_producto)
        return Response(json.dumps(modificado, indent=4),
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        mimetype=MIME_TYPE)
    return error_response(f'Producto {id_producto} no disponible sin precio asignado', 400)

@app.route("/producto/<id_producto>/cambiar_precio", methods=['PUT'])
def cambiar_precio_producto(id_producto):
    '''Servicio para cambiar el precio de un producto'''
    precio = request.args.get("precio", default=0, type=float)
    if precio > 0:
        producto = persist_tienda.get_producto(config_data['basedatos'], id_producto)
        if not producto:
            return error_response(f'Producto {id_producto} no encontrado', 404)
        modificado = persist_tienda.put_cambiar_precio(config_data['basedatos'],
            id_producto, precio)
        return Response(json.dumps(modificado, indent=4),
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        mimetype=MIME_TYPE)
    return error_response('Debe indicar un precio mayor que 0', 400)

@app.route("/producto/<id_producto>/solicitar", methods=['PUT'])
def solicitar_producto(id_producto):
    '''Servicio para solicitar una cantidad de un producto al almacén
        Invoca al API del Almacén para saber el stock disponible
        Si hay stock solicita su traspaso a la tienda
        Actualiza el producto con la nueva cantidad disponible'''
    cantidad = request.args.get("cantidad", default=0, type=int)
    if cantidad > 0:
        producto = persist_tienda.get_producto(config_data['basedatos'], id_producto)
        if not producto:
            return error_response(f'Producto {id_producto} no encontrado', 404)
        art_id = str(producto['articulo_id'])
        url_articulo = config_data['almacen']['base_url'] + '/articles/'
        response_data = None
        url_get = url_articulo + art_id
        response_data = get(url = url_get,
                        timeout = 60,
                        headers = config_data['almacen']['api_key'])
        if not response_data:
            return error_response(f'Articulo {art_id} no encontrado', 404)
        articulo = response_data.json()
        if articulo[0]['units'] < cantidad:
            return error_response('No hay suficiente stock', 400)
        put(url = url_articulo + '/send/' + art_id,
                timeout = 60,
                json = {'cantidad': cantidad},
                headers = config_data['almacen']['api_key'])
        modificado = persist_tienda.put_recibir_producto(config_data['basedatos'],
                        id_producto, cantidad)
        return Response(json.dumps(modificado, indent=4),
                        200,
                        {'Access-Control-Allow-Origin':'*'},
                        mimetype=MIME_TYPE)
    return error_response('Debe indicar una cantidad mayor que 0', 400)

def error_response(message: str, code: int):
    '''Respuesta de error'''
    return Response(message,
            code,
            {'Access-Control-Allow-Origin':'*'},
            MIME_TYPE)

app.register_blueprint(swaggerui_blueprint)
app.run(host=args.servidor, port=args.puerto)
