"""Clase principal del backend de pizza fullstack"""
from datetime import datetime
from flask import Flask, request, redirect
from persistencia import guardar_pedido_completo, Pedido, StringBuilder, FIELD_SEPARATOR

app = Flask(__name__)

@app.route("/pizza", methods=['POST'])

def procesar_pedido():
    """Crea fichero con nombre y apellidos desde frontend y redirige a solicita_pedido"""
    nombre = request.form.get("nombre")
    apellidos = request.form.get("apellidos")
    telefono = request.form.get("telefono")
    fecha_nacimiento = request.form.get("nacimiento")
    direccion = request.form.get("direccion")
    tamano_pizza = request.form.get("tamano")
    york = request.form.get("york")
    peppe = request.form.get("peppe")
    champis = request.form.get("champis")
    aceitunas = request.form.get("aceitunas")
    pedido = Pedido()
    pedido.iniciar(nombre, apellidos)
    if telefono:
        pedido.telefono = telefono
    if fecha_nacimiento:
        pedido.nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').strftime('%d/%m/%Y')
    if direccion:
        pedido.direccion = direccion
    if tamano_pizza:
        pedido.tamano = tamanos_pizza.get(tamano_pizza)
    if york:
        pedido.ingredientes.append(ingredientes.get(york))
    if peppe:
        pedido.ingredientes.append(ingredientes.get(peppe))
    if champis:
        pedido.ingredientes.append(ingredientes.get(champis))
    if aceitunas:
        pedido.ingredientes.append(ingredientes.get(aceitunas))
    pedido.imprimir()
    crear_fichero()
    guardar_pedido_completo(pedido)
    return redirect("http://localhost/pizza-fullstack/solicita_pedido.html", code = 302)

def crear_fichero():
    """Crea un fichero "pedidos.txt" vacío."""
    header = StringBuilder()
    header.append("NOMBRE")
    header.append(FIELD_SEPARATOR)
    header.append("APELLIDOS")
    header.append(FIELD_SEPARATOR)
    header.append("TELÉFONO")
    header.append(FIELD_SEPARATOR)
    header.append("FECHA_NACIMIENTO")
    header.append(FIELD_SEPARATOR)
    header.append("DIRECCIÓN")
    header.append(FIELD_SEPARATOR)
    header.append("TAMAÑO_PIZZA")
    header.append(FIELD_SEPARATOR)
    header.append("INGREDIENTES")
    with open("pedidos.txt", "w", encoding="utf-8") as file:
        file.write(header.to_string() + "\n")
        file.close()

tamanos_pizza = {
    "p": "Pequeña",
    "m": "Mediana",
    "g": "Grande",
    "x": "XXL"
}

ingredientes = {
    "p": "Pepperoni",
    "y": "Jamón de York",
    "c": "Champiñones",
    "a": "Aceitunas"
}
