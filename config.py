EMBEDDING_PROVIDER = "local"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

OPENAI_API_KEY = ""

LLM_PROVIDER = "ollama"
LLM_MODEL = "gemma4:e4b-it-qat"
OLLAMA_BASE_URL = "http://localhost:11434"

OPENCODE_MODEL = "qwen3.7-max"

DATA_DIR = "data/curated"
STORAGE_DIR = "storage"

TOP_K = 3
SIMILARITY_THRESHOLD = 0.3

SYSTEM_PROMPT = """Actuás como un ingeniero de firmware experto en Intel x86 de 32 bits en Modo Protegido.

Contexto verificado del manual oficial:
{context}

Respondé usando únicamente la información del contexto. Si no es suficiente, decilo explícitamente. Está terminantemente prohibido alucinar o inventar registros de hardware."""
