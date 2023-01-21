"""Programa para decodificar tokens JWT"""
import argparse
import jwt

def decode_token(token: str, secret: str, field: str):
    """ Decodifica un token JWT """

    print("Ejecutando programa con los siguiente argumentos:")
    print("--token: " + token)
    print("--secreto: " + secret)

    try:
        decoded = jwt.decode(token, secret, algorithms="HS256")
        if field:
            valor = str(decoded[field]) if field in decoded.keys() else 'No encontrado'
            print('Campo ' + field + ': ' + valor)
        else:
            print('Body del token: ' + str(decoded))
    except jwt.exceptions.InvalidSignatureError:
        print('¡¡Firma incorrecta!!')

parser = argparse.ArgumentParser(description='Decodificador de tokens JWT')
parser.add_argument('--token',
                        type=str,
                        metavar='eyJhbGciOiJIUzI1NiIsI...',
                        required=True,
                        help='Token JWT a decodificar')
parser.add_argument('--secret',
                        type=str,
                        metavar='G3tr0n1c5',
                        required=True,
                        help='Secreto de la firma del token')
parser.add_argument('--field',
                        type=str,
                        metavar='jti',
                        nargs='?',
                        help='Campo del body del token a mostrar')
args = parser.parse_args()

decode_token(args.token, args.secret, args.field)
