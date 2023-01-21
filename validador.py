"""Clase validadora de documentos xml con un esquema xml dado"""
import json
import os
import xmlschema

def validar(xml: str, xsd: str, xpath = "", _json = False):
    """ Valida un archivo xml con un esquema xsd """
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    xml_ruta = os.path.join(__location__, xml)
    xsd_ruta = os.path.join(__location__, xsd)

    try:
        xmlschema.validate(xml_ruta, xsd_ruta)
        print("¡El archivo es válido!")
    except xmlschema.validators.exceptions.XMLSchemaValidationError as err:
        print("¡El archivo no es válido! Causa:" + err.reason)

    if xpath:
        esquema = xmlschema.XMLSchema(xsd_ruta)
        valor = esquema.to_dict(xml_ruta, xpath)
        print("Valor del elemento " + xpath + " = " + valor)

    if _json:
        with open("carta.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(xmlschema.to_dict(xml_ruta), indent=4))
            file.close()
        print("¡Fichero " + xml_ruta + " convertido a JSON con éxito!")
