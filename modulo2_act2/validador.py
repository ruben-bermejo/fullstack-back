"""Clase validadora de documentos xml con un esquema xml dado"""
import json
import argparse
import xmlschema

def validar(xml: argparse.FileType('r', encoding='utf-8'),
            xsd: argparse.FileType('r', encoding='utf-8'),
            xpath: str,
            _json: bool):
    """ Valida un archivo xml con un esquema xsd y permite obtener el valor de
        uno de sus elementos y exportarlo a un archivo en formato Json """

    print("Ejecutando programa con los siguiente argumentos:")
    print("--xml: " + xml.name)
    print("--xsd: " + xsd.name)
    print("--xpath: " + str(xpath))
    print("--json: " + str(_json))

    try:
        xmlschema.validate(xml, xsd)
        print("¡El archivo es válido!")

        if xpath:
            esquema = xmlschema.XMLSchema(xsd.name)
            valor = esquema.to_dict(xml.name, xpath)
            print("Valor del elemento " + str(xpath) + " = " + str(valor))

        if _json:
            with open("carta.json", "w", encoding="utf-8") as file:
                file.write(json.dumps(xmlschema.to_dict(xml.name), indent=4))
                file.close()
            print("¡Fichero " + xml.name + " convertido a JSON con éxito!")

    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        print("¡El archivo no es válido! Causa:" + err.reason)

parser = argparse.ArgumentParser(description='Validador de XML.')
parser.add_argument('--xml', type=argparse.FileType('r', encoding='utf-8'), metavar='./carta.xml',
                    required=True, help='Ruta a un fichero XML')
parser.add_argument('--xsd', type=argparse.FileType('r', encoding='utf-8'), metavar='./carta.xsd',
                    required=True, help='Ruta a un fichero XSD')
parser.add_argument('--xpath', type=str, metavar='/carta/remitente/nombre', nargs='?',
                    help='Identifica en formato xpath un elemento del XML')
parser.add_argument('--json', action=argparse.BooleanOptionalAction, metavar='N',
                    help='Indica si transformar o no el XML a un fichero formato JSON')
args = parser.parse_args()

validar(args.xml, args.xsd, args.xpath, args.json)
