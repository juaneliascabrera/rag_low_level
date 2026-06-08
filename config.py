import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# --- Embedding ---
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "ollama")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "qwen3-embedding:0.6b")

# --- LLM ---
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "opencode")

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma4:e4b-it-qat")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

OPENCODE_MODEL = os.getenv("OPENCODE_MODEL", "kimi-k2.6")
OPENCODE_API_TYPE = os.getenv("OPENCODE_API_TYPE", None)

CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")

# --- API Keys ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENCODE_API_KEY = os.getenv("OPENCODE_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# --- Paths ---
DATA_DIR = str(BASE_DIR / "data" / "curated")
STORAGE_DIR = str(BASE_DIR / "storage")
CACHE_DIR = str(BASE_DIR / "storage" / "cache")

# --- Retrieval ---
TOP_K = int(os.getenv("TOP_K", "10"))
SIMILARITY_THRESHOLD = float(os.getenv("SIMILARITY_THRESHOLD", "0.3"))

RERANK_ENABLED = os.getenv("RERANK_ENABLED", "true").lower() == "true"
RERANK_MODEL = os.getenv("RERANK_MODEL", "cross-encoder/ms-marco-MiniLM-L-6-v2")
RERANK_TOP_K = int(os.getenv("RERANK_TOP_K", "3"))

HYDE_ENABLED = os.getenv("HYDE_ENABLED", "false").lower() == "true"

# --- Context ---
CONTEXT_TOKEN_BUDGET = int(os.getenv("CONTEXT_TOKEN_BUDGET", "3000"))
CHARS_PER_TOKEN = int(os.getenv("CHARS_PER_TOKEN", "4"))

DEBUG_SHOW_CONTEXT = os.getenv("DEBUG_SHOW_CONTEXT", "false").lower() == "true"

# --- System Prompt ---
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", """You are an expert firmware engineer specialized in Intel x86 32-bit Protected Mode.

Verified context from the official manual:
{context}

Respond using only the information in the context. If it is not sufficient, say so explicitly. It is strictly forbidden to hallucinate or invent hardware registers.

Response format:
- If the question is about code, provide NASM examples
- If the question is about data structures, use diagrams or tables
- Cite the specific fragment you used for each main claim using [Fragment N]
""")
