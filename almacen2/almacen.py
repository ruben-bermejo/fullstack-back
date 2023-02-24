import argparse
import yaml
import db_config
import request_handler
from flask import Flask, jsonify, request, send_from_directory
import article_services 
import consumer_services
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument("--servidor", default="localhost")
parser.add_argument("--puerto", default=5000, type=int)
parser.add_argument("--config", required=True)
args = parser.parse_args()

# Load file .yaml
with open(args.config, 'r') as f:
    config = yaml.safe_load(f)

# Initialize database
db_config.init_db(config["basedatos"]["path"])

# Get API Key from config
api_key = config["basedatos"]["consumidor_almacen_key"]

# Configurar la ruta de documentación de API y el archivo de especificaciones
SWAGGER_URL = '/api/docs'
API_DOC_FILE = '/services/spec'

# Inicializar flask_swagger_ui
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_DOC_FILE,
    config={
        'app_name': "Almacén API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# Crear un servicio para servir la información del archivo api_doc.yaml
@app.route('/services/spec')
def api_spec():
    return send_from_directory(app.root_path, "api_doc.yaml")

# Create article
@app.route('/articles', methods=['POST'])
def create_article_route():
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    article_info = request.json['article_info']
    units = request.json['units']
    available = request.json['available']
    
    request_handler.create_article(article_info, units, available)
    
    return jsonify({'message': 'Article created successfully'}), 201

# Read all articles
@app.route('/articles', methods=['GET'])
def read_all_article_route():
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    articles = request_handler.read_all_articles()
    
    result = []
    for article in articles:
        article_dict = {
            "id": article[0],
            "article_info": article[1],
            "units": article[2],
            "available": article[3],
        }
        result.append(article_dict)
    return jsonify(result), 200

# Read article
@app.route('/articles/<int:article_id>', methods=['GET'])
def read_article_route(article_id):
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401
        
    article = request_handler.read_article(article_id)
    
    if article is None:
        return jsonify({'message': 'Article not found'})
    
    result = []
    article_dict = {
        "id": article[0],
        "article_info": article[1],
        "units": article[2],
        "available": article[3],
    }
    result.append(article_dict)
    return jsonify(result), 200

# Update article
@app.route('/articles/<int:article_id>', methods=['PUT'])
def update_article_route(article_id):
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    article_info = request.json['article_info']
    units = request.json['units']
    available = request.json['available']
    
    request_handler.update_article(article_id, article_info, units, available)
    
    return jsonify({'message': 'Article updated successfully'}), 200

# Delete article
@app.route('/articles/<int:article_id>', methods=['DELETE'])
def delete_article_route(article_id):
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    request_handler.delete_article(article_id)
    
    return jsonify({'message': 'Article deleted successfully'}), 200

# Receive article
@app.route('/articles/receive/<int:article_id>', methods=['PUT'])
def receive_article_route(article_id):
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    units_received = request.json['units_received']
    article_services.receive_article(article_id, units_received)
    
    return jsonify({'message': 'Article received successfully'}), 200

# Send article
@app.route('/articles/send/<int:article_id>', methods=['PUT'])
def send_article_route(article_id):
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    units_sent = request.json['cantidad']
    print(units_sent)
    article_services.send_article(article_id, units_sent)
    return jsonify({'message': 'Article sent successfully'}), 200

# Create consumer
@app.route('/consumers', methods=['POST'])
def create_consumer_route():
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401

    username = request.json['username']
    password = request.json['password']

    api_key_consumer = consumer_services.create_consumer(username, password)

    if api_key_consumer is None:
        return jsonify({'message': 'Creation of consumer failed'})

    return jsonify({'message': 'Consumer created successfully', 'api_key': api_key_consumer}), 200

# Authenticate consumer
@app.route('/consumers/authenticate', methods=['POST'])
def authenticate_consumer_route():
    # Check API Key
    if 'Authorization' not in request.headers:
        return jsonify({'message': 'API Key is missing'}), 401
    if request.headers['Authorization'] != api_key:
        return jsonify({'message': 'API Key is invalid'}), 401
        
    username = request.json['username']
    password = request.json['password']

    api_key_consumer = consumer_services.authenticate_consumer(username, password)

    if api_key_consumer is None:
        return jsonify({'message': 'Authentication failed'})

    return jsonify({'message': 'Authentication succeeded', 'api_key': api_key_consumer}), 200

if __name__ == "__main__":
    app.run(host=args.servidor, port=args.puerto)

