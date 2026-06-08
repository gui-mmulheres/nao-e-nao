import os
from dotenv import load_dotenv


def inicializa_env():
    load_dotenv()

    env = {
        'model_docx': os.getenv("MODEL_DOCX"),
        'output_dir': os.getenv("OUTPUT_DIR"),
        'client_id': os.getenv("CLIENT_ID"),
        'tenant_id': os.getenv("TENANT_ID"),
        'cache_key': os.getenv("CACHE_KEY"),
        'url_validador': os.getenv("URL_VALIDADOR")
    }

    return env
