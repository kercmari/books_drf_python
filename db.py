from pymongo import MongoClient
import os

# Obtener la URI de MongoDB desde variables de entorno
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/mi_basedatos")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "prueba")
# Inicializar el cliente de MongoDB con la URI que incluye la base de datos predeterminada
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
# Obtener la base de datos predeterminada
