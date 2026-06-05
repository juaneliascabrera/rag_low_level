import os
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = "INFO"

EMBEDDING_PROVIDER = "local"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

LLM_PROVIDER = "ollama"
OLLAMA_MODEL = "gemma4:e4b-it-qat"
OLLAMA_BASE_URL = "http://localhost:11434"

OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY", "")
OPENCODE_MODEL = "kimi-k2.6"

DATA_DIR = "data/curated"
STORAGE_DIR = "storage"
CACHE_DIR = "storage/cache"

TOP_K = 10
SIMILARITY_THRESHOLD = 0.3

RERANK_ENABLED = True
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 3

HYDE_ENABLED = False

CONTEXT_TOKEN_BUDGET = 3000
CHARS_PER_TOKEN = 4

DEBUG_SHOW_CONTEXT = False

SYSTEM_PROMPT = """You are an expert firmware engineer specialized in Intel x86 32-bit Protected Mode.

Verified context from the official manual:
{context}

Respond using only the information in the context. If it is not sufficient, say so explicitly. It is strictly forbidden to hallucinate or invent hardware registers.

Response format:
- If the question is about code, provide NASM examples
- If the question is about data structures, use diagrams or tables
- Cite the specific fragment you used for each main claim using [Fragment N]
"""
