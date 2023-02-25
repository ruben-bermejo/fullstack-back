"""Programa para generar tokens JWT"""
import uuid
import argparse
import json
import jwt

def generar_token(payload: open, secret: str):
    """ Genera un token JWT """
    print("Ejecutando programa con los siguiente argumentos:")
    print("--payload: " + payload.name)
    print("--secreto: " + secret)

    jwt_id = str(uuid.uuid4())
    token = jwt.encode({"iss": json.load(payload), "jti": jwt_id}, secret, algorithm="HS256")
    print("TOKEN JWT: " + token)

parser = argparse.ArgumentParser(description='Generador de tokens JWT')
parser.add_argument('--payload',
                        type=argparse.FileType('r', encoding='utf-8'),
                        metavar='./payload.json',
                        required=True,
                        help='Ruta a un fichero JSON que contiene el body del token')
parser.add_argument('--secret',
                        type=str,
                        metavar='G3tr0n1c5',
                        required=True,
                        help='Secreto para firmar el token')
args = parser.parse_args()
generar_token(args.payload, args.secret)
 