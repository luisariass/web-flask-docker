from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient # Importar MongoClient
from pymongo.errors import ConnectionFailure # Para manejo de errores de conexión

app = Flask(__name__)

# --- Configuración de MongoDB desde variables de entorno ---
# Usar 'mongo-db' como default si no se provee, ya que ese será el nombre del servicio/contenedor de mongo
MONGO_HOST = os.environ.get('MONGO_HOST', 'mongo-db')
MONGO_PORT = int(os.environ.get('MONGO_PORT', 27017))
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'mensajes_db')
MONGO_COLLECTION_NAME = os.environ.get('MONGO_COLLECTION_NAME', 'mensajes')

# --- Conexión a MongoDB ---
try:
    # Construir la URI de conexión
    MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"
    client = MongoClient(MONGO_URI)
    # La siguiente línea fuerza una conexión para verificarla al inicio
    client.admin.command('ping')
    db = client[MONGO_DB_NAME]
    mensajes_collection = db[MONGO_COLLECTION_NAME]
    print(f"Conexión exitosa a MongoDB en {MONGO_URI}")
except ConnectionFailure as e:
    print(f"Error al conectar a MongoDB: {e}")
    # Podrías decidir terminar la aplicación si la DB no está disponible
    # O manejarlo en las rutas específicas
    client = None # Marcar cliente como None si falla la conexión
    mensajes_collection = None

# --- Rutas existentes (home, about, docker) ---
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/docker")
def docker():
    # Asegúrate de tener docker.html o modifica esta ruta
    return render_template("docker.html")

# --- Ruta para recibir y guardar mensajes en MongoDB ---
@app.route("/mensaje", methods=['POST'])
def recibir_mensaje():
    # Cambia esta línea
    if mensajes_collection is None:
         return jsonify({"error": "Conexión a base de datos no disponible"}), 503 # Service Unavailable
    try:
        data = request.get_json()
        mensaje_texto = data.get('mensaje')

        if not mensaje_texto:
            return jsonify({"error": "Mensaje no proporcionado"}), 400

        # Crear documento para MongoDB
        mensaje_doc = {"mensaje": mensaje_texto}
        # Insertar en la colección
        result = mensajes_collection.insert_one(mensaje_doc)

        return jsonify({
            "status": "Mensaje recibido y guardado en DB",
            "id": str(result.inserted_id) # Devolver el ID del documento insertado
            }), 201

    except Exception as e:
        print(f"Error en /mensaje: {e}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

# --- Ruta para ver mensajes desde MongoDB ---
@app.route("/mensajes", methods=['GET'])
def ver_mensajes():
    if mensajes_collection is None:
         return jsonify({"error": "Conexión a base de datos no disponible"}), 503

    try:
        # Buscar todos los documentos, excluyendo el campo _id
        mensajes_cursor = mensajes_collection.find({}, {'_id': 0})
        # Convertir cursor a lista de diccionarios
        lista_mensajes = list(mensajes_cursor)
        return jsonify({"mensajes": lista_mensajes})
    except Exception as e:
        print(f"Error en /mensajes: {e}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500

if __name__ == "__main__":
    # Flask se ejecutará usando las variables de entorno definidas en el Dockerfile o docker run
    # No es necesario especificar host/port aquí si se usa 'flask run'
    # app.run(host='0.0.0.0', port=5000, debug=False)
    # Sin embargo, si ejecutas 'python app.py' directamente, Flask usará sus defaults (localhost:5000)
    # Para consistencia con Docker, podrías leer las ENV aquí también, pero 'flask run' ya lo hace.
    pass # El comando CMD ["flask", "run"] se encargará de iniciar
