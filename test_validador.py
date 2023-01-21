"""Módulo con funciones de test para el validador de xml"""
from validador import validar

print("1. Validando documento con un esquema XML dado")
validar("carta.xml", "carta.xsd")

print("2. Verificar que podemos sacar el nombre del remitente")
validar("carta.xml", "carta.xsd", "/carta/remitente/nombre")

print("3. Transformar el fichero XML en JSON")
validar("carta.xml", "carta.xsd", "", True)
