"""Clase principal del backend de pizza fullstack"""
from flask import Flask, send_file
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/api/docs'
API_URL = '/services/spec'

@app.route("/services/spec", methods=['GET'])
def swagger_yaml():
    """Recupera el archivo yaml"""
    return send_file('./api_doc.yaml')

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API Swagger JSONPlaceholder"
    }
)

app.register_blueprint(swaggerui_blueprint)

app.run()
