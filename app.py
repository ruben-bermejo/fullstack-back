from datetime import datetime
from flask import Flask, request, redirect
from persistencia import guardar_pedido_completo, Pedido

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
    pedido = Pedido(nombre, apellidos)
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
    print(pedido)
    crear_fichero()
    guardar_pedido_completo(pedido)
    return redirect("http://localhost/pizza-fullstack/solicita_pedido.html", code = 302)
    
def crear_fichero():
    """ Crea un fichero "pedidos.txt" vacío. """
    with open("pedidos.txt", "w", encoding="utf-8") as file:
        file.write("NOMBRE|APELLIDOS|TELÉFONO|FECHA_NACIMIENTO|DIRECCIÓN|TAMAÑO_PIZZA|INGREDIENTES\n")
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