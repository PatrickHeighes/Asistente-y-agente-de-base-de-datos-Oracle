import os
import json
import requests
from dotenv import load_dotenv
import oracledb
from config.settings_model.config_model import model_settings
from prompt.system import SYSTEM_PROMPT 
from chat_with_AI.response_agent_mode import ASK_RESPONSE_STRUCTURE, AGENT_RESPONSE_STRUCTURE

load_dotenv()

class ModelAI:
    def __init__(self):
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.dsn = os.getenv("DB_DSN")
        self.model_name = model_settings.MODEL_NAME
        self.api_key = os.getenv("OLLAMA_KEY")
        
        print(f"Configurando modelo en la nube ({self.model_name})...")

    def ejecutar_consulta_sql(self, query_sql: str):
        """Ejecuta la consulta SQL directamente en Oracle usando oracledb"""
        try:
            connection = oracledb.connect(
                user=self.user, 
                password=self.password, 
                dsn=self.dsn
            )
            cursor = connection.cursor()
            cursor.execute(query_sql)
            
            sql_upper = query_sql.strip().upper()
            if sql_upper.startswith("SELECT") or sql_upper.startswith("WITH"):
                resultados = cursor.fetchall()
                columnas = [col[0] for col in cursor.description] if cursor.description else []
                cursor.close()
                connection.close()
                return {"tipo": "select", "columns": columnas, "rows": resultados}
            
            connection.commit()
            cursor.close()
            connection.close()
            return {"tipo": "mutacion", "status": "success", "message": "Consulta o mutación ejecutada correctamente."}
            
        except Exception as e:
            return {"error": str(e)}

    def modo_ask(self, pregunta_usuario: str):
        """Responde preguntas generales usando la estructura de ASK_RESPONSE_STRUCTURE"""
        url = "https://api.ollama.com/api/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        prompt_completo = f"""
        {SYSTEM_PROMPT}
        
        Pregunta del usuario: "{pregunta_usuario}"
        
        {ASK_RESPONSE_STRUCTURE}
        """
        
        payload = {
            "model": self.model_name,
            "prompt": prompt_completo,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", data.get("content", ""))
            else:
                return f"Error de API ({response.status_code}): {response.text}"
        except Exception as e:
            return f"Error de conexión: {str(e)}"

    def modo_agent_analisis(self, pregunta_usuario: str):
        """Pide al modelo que analice la solicitud, determine gravedad, SQL e impacto"""
        prompt_completo = f"""
        {SYSTEM_PROMPT}
        
        Esquema conocido de la base de datos Chinook:
        - ARTIST (ArtistId, Name)
        - ALBUM (AlbumId, Title, ArtistId)
        - TRACK (TrackId, Name, AlbumId, MediaTypeId, GenreId, Composer, Milliseconds, Bytes, UnitPrice)
        - CUSTOMER (CustomerId, FirstName, LastName, Company, Address, City, State, Country, PostalCode, Phone, Fax, Email, SupportRepId)
        - INVOICE (InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total)
        
        Petición o instrucción del usuario: "{pregunta_usuario}"
        
        {AGENT_RESPONSE_STRUCTURE}
        
        Devuelve tu respuesta en formato JSON estricto con las llaves: "entendimiento", "gravedad", "sql", "explicacion_impacto", "estilo".
        """
        
        url = "https://api.ollama.com/api/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model_name,
            "prompt": prompt_completo,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                texto_generado = data.get("response", data.get("content", ""))
                
                # Intentar limpiar bloques markdown si el modelo los incluye
                texto_limpio = texto_generado.replace("```json", "").replace("```", "").strip()
                
                try:
                    parsed_json = json.loads(texto_limpio)
                    return parsed_json
                except json.JSONDecodeError:
                    # Fallback si no devuelve JSON puro
                    return {
                        "entendimiento": texto_generado,
                        "gravedad": "desconocida",
                        "sql": "",
                        "explicacion_impacto": "No se pudo estructurar el impacto automáticamente.",
                        "estilo": "estándar"
                    }
            else:
                return {"error": f"Error de API ({response.status_code}): {response.text}"}
        except Exception as e:
            return {"error": f"Error de conexión: {str(e)}"}