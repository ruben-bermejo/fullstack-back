"""Módulo persistencia con funciones para procesar pedidos"""
from persistencia import guardar_pedido

#Lista de pedidos con dos atributos: Nombre y Apellidos
pedidos = [ {"nombre": "José Rubén", "apellidos": "Bermejo Sanz"},
            {"nombre": "Michael", "apellidos": "Scott"}]

def crear_fichero():
    """Crea un fichero "pedidos.txt" vacío."""
    with open("pedidos.txt", "w", encoding="utf-8") as file:
        file.write("")
        file.close()

def escribir_fichero():
    """Invoca a la función `persistencia.guardar_pedido()` por cada elemento
    en la lista de pedidos."""
    for person in pedidos:
        guardar_pedido(person["nombre"], person["apellidos"])

def test_guardar_pedido():
    """Prueba básica"""
    crear_fichero()
    escribir_fichero()
    with open("pedidos.txt", "r", encoding="utf-8") as file:
        firstline = file.readline()
        secondline = file.readline()
        file.close()
    assert firstline == "José Rubén Bermejo Sanz\n"
    assert secondline == "Michael Scott\n"
