import os
from dotenv import load_dotenv

load_dotenv()

class ModelSettings:
    MODEL_NAME = os.getenv("MODEL_NAME") # O usar gpt-oss:120b si las consultas tiene mucha robustes de analisis
    temperature = float(os.getenv("TEMPERATURE", 0.7))
    max_tokens = int(os.getenv("MAX_TOKENS", 1024))
    log_level = os.getenv("LOG_LEVEL", "INFO")
    top_p = float(os.getenv("TOP_P", 0.9))
    top_k = int(os.getenv("TOP_K", 40))
    frequency_penalty = float(os.getenv("FREQUENCY_PENALTY", 0.0))
    presence_penalty = float(os.getenv("PRESENCE_PENALTY", 0.0))
    timeout = int(os.getenv("TIMEOUT", 30))


    # Aquí puedes agregar parámetros adicionales de temperatura o límites de tokens si lo requieres

model_settings = ModelSettings()