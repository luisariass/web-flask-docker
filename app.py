from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure # Para manejo de errores de conexión


app = Flask(__name__)
DATA_FOLDER = '/app/data'
MESSAGES_FILE = os.path.join(DATA_FOLDER, 'mensajes.txt')

os.makedirs(DATA_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/docker")
def docker():
    return render_template("docker.html")


@app.route("/mensaje", methods=['POST'])
def recibir_mensaje():
    try:
        # Asume que el cuerpo de la petición es JSON con una clave 'mensaje'
        data = request.get_json()
        mensaje = data.get('mensaje')

        if not mensaje:
            return jsonify({"error": "Mensaje no proporcionado"}), 400

        # Guarda el mensaje en el archivo, añadiendo una nueva línea
        with open(MESSAGES_FILE, 'a') as f:
            f.write(mensaje + '\n')

        return jsonify({"status": "Mensaje recibido y guardado"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/mensajes", methods=['GET'])
def ver_mensajes():
    try:
        if not os.path.exists(MESSAGES_FILE):
            return jsonify({"mensajes": []})

        with open(MESSAGES_FILE, 'r') as f:
            mensajes = [line.strip() for line in f.readlines()]
        return jsonify({"mensajes": mensajes})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False) # Desactiva debug para producción en contenedor
# app.py
