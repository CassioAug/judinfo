import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    ROOT_DIR = Path(__file__).resolve().parent
    load_dotenv(ROOT_DIR / ".env")
except Exception:
    pass

# API pública do DataJud conforme disponibilizado em:
# https://datajud-wiki.cnj.jus.br/api-publica/acesso
# Suporta sobreposição opcional via variável de ambiente DATAJUD_API_KEY no arquivo .env
API_KEY = os.getenv("DATAJUD_API_KEY", "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==")