"""Configuración de la conexión a la base de datos MongoDB."""
import os
import sys
import logging
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from pymongo.collection import Collection

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de base de datos leída desde el .env
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

try:
    # Se inicializa el cliente de MongoDB (síncrono)
    cliente = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # Ping para forzar una verificación de la conexión
    cliente.admin.command('ping')
    logger.info("Conexión exitosa a MongoDB Atlas.")
    
except ConnectionFailure as e:
    logger.error(f"Error Crítico: No se pudo conectar a la base de datos. {e}")
    sys.exit(1)

# Instancias de la DB y Colección
db = cliente[DB_NAME]
coleccion_sensores = db[COLLECTION_NAME]

def get_collection() -> Collection:
    """
    Devuelve la instancia de la colección de sensores.
    
    Returns:
        Collection: Objeto colección de PyMongo para realizar operaciones CRUD.
    """
    return coleccion_sensores
