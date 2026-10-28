import os
import oracledb
from dotenv import load_dotenv

load_dotenv()

def get_oracle_connection():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    dsn = os.getenv("DB_DSN")

    try:
        # Habilitar modo delgado o grueso según necesidad (por defecto el modo delgado no requiere Oracle Client pesado)
        connection = oracledb.connect(user=user, password=password, dsn=dsn)
        print("¡Conexión exitosa a la base de datos Oracle!")
        return connection
    except Exception as e:
        print(f"Error al conectar a Oracle: {e}")
        return None

if __name__ == "__main__":
    get_oracle_connection()