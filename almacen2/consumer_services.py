import hashlib
import uuid
import sqlite3
from flask import Flask

app = Flask(__name__)

def generate_api_key(username):
    api_key = hashlib.sha256((username + str(uuid.uuid4())).encode()).hexdigest()
    return api_key

def create_consumer(username, password):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    api_key = generate_api_key(username)
    password = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO consumers (username, password, api_key) VALUES (?, ?, ?)",
                   (username, password, api_key))
    conn.commit()
    return api_key

def authenticate_consumer(username, password):
    conn = sqlite3.connect('almacen.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consumers WHERE username=?", (username,))
    consumer = cursor.fetchone()
    if consumer is None:
        return None
    if hashlib.sha256(password.encode()).hexdigest() != consumer[3]:
        return None
    return consumer[3]
    