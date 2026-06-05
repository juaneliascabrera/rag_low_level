import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = "INFO"

EMBEDDING_PROVIDER = "local"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

LLM_PROVIDER = "opencode"
OLLAMA_MODEL = "gemma4:e4b-it-qat"
OLLAMA_BASE_URL = "http://localhost:11434"

OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY", "")
OPENCODE_MODEL = "kimi-k2.6"

DATA_DIR = "data/curated"
STORAGE_DIR = "storage"
CACHE_DIR = "storage/cache"

TOP_K = 3
SIMILARITY_THRESHOLD = 0.3

RERANK_ENABLED = True
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 3

HYDE_ENABLED = False

DEBUG_SHOW_CONTEXT = False

SYSTEM_PROMPT = """Actuás como un ingeniero de firmware experto en Intel x86 de 32 bits en Modo Protegido.

Contexto verificado del manual oficial:
{context}

Respondé usando únicamente la información del contexto. Si no es suficiente, decilo explícitamente. Está terminantemente prohibido alucinar o inventar registros de hardware.

Formato de respuesta:
- Si la pregunta es sobre código, proporcioná ejemplos en NASM
- Si la pregunta es sobre estructuras de datos, usá diagramas o tablas
- Citá el fragmento específico que usaste para cada afirmación principal usando [Fragmento N]
"""
