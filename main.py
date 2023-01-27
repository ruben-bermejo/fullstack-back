"""Clase para invocar los métodos de un API REST"""
import argparse
import jsonhelper
from requesthelper import do_request, parse_response
from constantes import FICHERO_CONFIG, FICHERO_POSTS, FICHERO_COMMENTS, POSTS, COMMENTS

parser = argparse.ArgumentParser(description='Programa para invocar API REST')
parser.add_argument('--method',
                    type=str,
                    metavar='[GET,PUT,POST,DELETE]',
                    required=True,
                    choices=['GET','PUT','POST','DELETE'],
                    help='Método usado para llamar al API')
parser.add_argument('--resource',
                    type=str,
                    metavar='[comments,posts]',
                    required=True,
                    choices=[COMMENTS,POSTS],
                    help='Recurso sobre el que realizar la operación')
parser.add_argument('--resource_id',
                    type=int,
                    metavar='1',
                    nargs='?',
                    help='Identificador único del recurso. Obligatorio para DELETE/PUT')
args = parser.parse_args()

#Validamos resource_id obligatorio
if args.method in ['PUT', 'DELETE'] and not args.resource_id:
    parser.error('El argumento --resource_id es obligatorio cuando --method es PUT o DELETE')

#Recuperamos la información del fichero de configuración
config = jsonhelper.read_json(FICHERO_CONFIG)
baseurl = config['url']
tout = config['request_time_out']
response_data_file = config['response_data']
response_status_file = config['response_status']

#Construimos la URL
_url = baseurl + args.resource
if args.method != 'POST' and args.resource_id:
    _url = _url + '/' + str(args.resource_id)

#Invocamos al API
response_data = do_request(_url,
                            args.method,
                            FICHERO_POSTS if args.resource==POSTS else FICHERO_COMMENTS,
                            tout)

#Escribimos el fichero con la información de estado de la respuesta
jsonhelper.write_json(response_status_file,
                        parse_response(response_data, _url, args.method),
                        response_data.encoding)

#Escribimos el fichero json con los datos del recurso devueltos en la respuesta
jsonhelper.write_json(response_data_file,
                    jsonhelper.parse_jsonapi(response_data.json(), _url),
                    response_data.encoding)
