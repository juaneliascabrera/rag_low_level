# RAG Intel x86 32-bit

RAG (Retrieval-Augmented Generation) system specialized in low-level programming for Intel x86 32-bit in Protected Mode. It optimizes LLM performance on monolithic kernel development and embedded systems tasks, eliminating critical hardware hallucinations through verified context retrieval.

## Features

- **Interchangeable embeddings:** Local (sentence-transformers), Ollama, OpenAI
- **Interchangeable LLMs:** Local Ollama, OpenCode GO (OpenAI-compatible + Anthropic-compatible)
- **Semantic chunking:** Markdown parser with YAML frontmatter, code block separation, configurable overlap
- **Cross-encoder re-ranking:** Improves retrieval precision
- **HyDE (optional):** Query transformation with hypothetical documents
- **Metadata filtering:** Filter by component, architecture, mode, type
- **Context budget:** Automatic truncation to prevent LLM overflow
- **Embedding cache:** Persistence with SHA256 hash per model
- **Unit tests:** Coverage for cache, vectorstore, chunker, reranker, hyde

## Table of contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Project structure](#project-structure)
5. [Preparing documents](#preparing-documents)
6. [Usage](#usage)
7. [Detailed configuration per provider](#detailed-configuration-per-provider)
8. [Troubleshooting](#troubleshooting)
9. [Tests](#tests)
10. [Concepts covered](#concepts-covered)

---

## Prerequisites

- **Python 3.10+**
- **pip** (package manager)
- At least one embedding provider:
  - `sentence-transformers` (local, no external services)
  - Ollama running locally
  - OpenAI API key
- At least one LLM provider:
  - Ollama running locally with a downloaded model
  - OpenCode GO API key (or OpenAI/Anthropic if you adapt the code)

---

## Installation

### 1. Clone the repository

```bash
git clone <repo-url>
cd RAGIntelx86
```

### 2. Create a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or on Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

For development (includes pytest):

```bash
pip install -r requirements-dev.txt
```

---

## Configuration

### 1. Environment variables (API keys)

Copy the example file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys:

```bash
# OpenAI (optional, only if you use OpenAIEmbedder or the OpenAI LLM)
OPENAI_API_KEY=sk-...

# OpenCode GO (optional, if you use OpenCode models)
OPENCODE_API_KEY=your-api-key-here
```

⚠️ **Important:** The `.env` file is in `.gitignore` and **is not uploaded to the repository**. Each user must create their own.

### 2. Model configuration (`config.py`)

Edit `config.py` to choose:

#### Embedding

```python
EMBEDDING_PROVIDER = "local"  # "local" | "ollama" | "openai"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

| Provider | Recommended models | Requirements |
|----------|---------------------|------------|
| `local` | `all-MiniLM-L6-v2` (384d, fast), `all-mpnet-base-v2` (768d, better quality) | None (auto-download) |
| `ollama` | `nomic-embed-text`, `mxbai-embed-large` | Ollama running locally |
| `openai` | `text-embedding-3-small` (1536d), `text-embedding-3-large` (3072d) | `OPENAI_API_KEY` in `.env` |

#### LLM

```python
LLM_PROVIDER = "opencode"  # "ollama" | "opencode"
OLLAMA_MODEL = "gemma4:e4b-it-qat"
OLLAMA_BASE_URL = "http://localhost:11434"
OPENCODE_MODEL = "kimi-k2.6"
```

| Provider | Example models | Requirements |
|----------|----------------|------------|
| `ollama` | `gemma4:e4b-it-qat`, `qwen2.5-coder:7b`, `deepseek-coder` | Ollama running locally |
| `opencode` | `kimi-k2.6`, `glm-5.1`, `qwen3.7-max` | `OPENCODE_API_KEY` in `.env` |

#### Retrieval parameters

```python
TOP_K = 10                      # Candidates for the reranker
SIMILARITY_THRESHOLD = 0.3      # Minimum cosine similarity threshold
RERANK_ENABLED = True            # Use cross-encoder for re-ranking
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 3                # Final results after re-rank
HYDE_ENABLED = False             # Query transformation with HyDE
CONTEXT_TOKEN_BUDGET = 3000      # Maximum context tokens
```

---

## Project structure

```
RAGIntelx86/
├── rag.py                    # Main CLI and orchestrator
├── config.py                 # Central configuration
├── logger.py                 # Logging system
├── .env.example              # Environment variables template
├── .gitignore
├── requirements.txt          # Runtime dependencies
├── requirements-dev.txt      # Development dependencies
├── README.md                 # This file
├── CONTEXT.md                # Detailed project context
├── data/
│   └── curated/              # Curated .md documents (YAML frontmatter)
├── embedder/
│   ├── base.py               # Embedder abstract interface
│   ├── local.py              # sentence-transformers local
│   ├── ollama.py             # Ollama API
│   ├── openai_client.py      # OpenAI API
│   ├── cache.py              # Embedding cache (pickle)
│   └── __init__.py
├── vectorstore/
│   ├── store.py              # VectorStore (NumPy + JSON)
│   └── __init__.py
├── chunker/
│   ├── markdown.py           # Semantic parser with YAML + code split
│   └── __init__.py
├── llm/
│   ├── base.py               # LLMClient abstract interface
│   ├── ollama.py             # Ollama client (streaming + thinking)
│   ├── opencode.py           # OpenCode GO client
│   └── __init__.py
├── reranker/
│   ├── reranker.py           # Cross-encoder re-ranking
│   └── __init__.py
├── retrieval/
│   ├── hyde.py               # HyDE query transformation
│   └── __init__.py
├── tests/                    # Unit tests
│   ├── test_cache.py
│   ├── test_chunker.py
│   ├── test_hyde.py
│   ├── test_reranker.py
│   ├── test_vectorstore.py
│   └── __init__.py
└── storage/                  # Auto-generated
    ├── vectors.npy
    ├── texts.json
    ├── metadata.json
    ├── config.json
    └── cache/
        └── embedding_cache.pkl
```

---

## Preparing documents

### Format of `.md` files

Documents go in `data/curated/` and must have **YAML frontmatter** with metadata:

```markdown
---
architecture: x86_32
component: GDT
mode: protected
tags: [segmentation, memory, descriptors]
---

# Document title

Brief introduction...

## Section 1

Explanatory content with long text...

```nasm
; Example code
mov eax, cr0
or eax, 1
mov cr0, eax
```

## Section 2

Another section...
```

### Frontmatter

| Field | Description | Default |
|-------|-------------|---------|
| `architecture` | Target architecture | `x86_32` |
| `component` | Component (GDT, IDT, paging, etc.) | Filename |
| `mode` | Operation mode | `protected` |
| `tags` | List of tags for filtering | (none) |

### Code blocks

Code blocks are automatically split into independent chunks with `type: "code"` in the metadata. This allows retrieval to find relevant code even though the embedding does not understand assembler inside natural text.

### Overlap

The chunker adds overlap (default 3 lines) between chunks **of the same type** (code with code, explanation with explanation) to maintain contextual continuity without contaminating embeddings of one type with the other.

---

## Usage

### 1. Index documents

Indexing generates embeddings for all `.md` files in `data/curated/` and persists them in `storage/`.

```bash
python rag.py index
```

**Expected output:**

```
[INFO] embedder.local: Loading local embedding model: all-MiniLM-L6-v2
[INFO] embedder.local: Model loaded. Dimension: 384
[INFO] Indexing 1 files...
[INFO]   Processing: GDT.md
[INFO] chunker.markdown:   GDT.md: 19 chunks generated
[INFO]   Generating embeddings for 19 chunks...
[INFO]   Generating 19 new embeddings...
[INFO] Indexing complete: 19 chunks stored
```

⚠️ **When to re-index:**

- First time
- You add or modify documents in `data/curated/`
- You change `EMBEDDING_PROVIDER` or `EMBEDDING_MODEL`
- You change `CHARS_PER_TOKEN` or chunker parameters

⚠️ **If you change the embedding model, the vector dimension changes and the system detects the inconsistency.** You will see an error asking to re-index.

### 2. Make queries

```bash
python rag.py query "How do I configure a segment descriptor in the GDT?"
```

**Expected output:**

```
================================================================================
ANSWER:
================================================================================
[Thinking]
The user is asking about the GDT...

[Response]
According to the provided context, a GDT segment descriptor is configured...
```

### 3. Debug: see the retrieved context

Enable `DEBUG_SHOW_CONTEXT = True` in `config.py` to see which fragments were retrieved and their similarity/re-ranking scores.

---

## Detailed configuration per provider

### Option 1: Local with sentence-transformers (recommended to start)

**Advantages:** No external services, no API keys, works offline.

```python
# config.py
EMBEDDING_PROVIDER = "local"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

**Installation:** Already in `requirements.txt` (`sentence-transformers`).

**First time:** Downloads the model (~80MB) automatically.

### Option 2: Ollama (local with Ollama)

**Advantages:** Full control, multiple models available.

```python
# config.py
EMBEDDING_PROVIDER = "ollama"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"
```

**Requirements:**
1. Install Ollama: https://ollama.com/download
2. Download the embedding model:
   ```bash
   ollama pull nomic-embed-text
   ```
3. (Optional) Download the LLM model:
   ```bash
   ollama pull gemma4:e4b-it-qat
   ```

**Usage:**
```python
LLM_PROVIDER = "ollama"
OLLAMA_MODEL = "gemma4:e4b-it-qat"
```

### Option 3: OpenAI (embeddings and/or LLM)

**Advantages:** High quality models.

```python
# config.py
EMBEDDING_PROVIDER = "openai"
EMBEDDING_MODEL = "text-embedding-3-small"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # In .env
```

⚠️ **Note:** The current code has `OpenAIEmbedder` but the OpenAI LLM client is not implemented. Only OpenCode and Ollama are supported as LLM. If you want to use OpenAI as the LLM, you need to adapt `llm/opencode.py` or create `llm/openai.py`.

### Option 4: OpenCode GO (OpenCode models)

**Advantages:** Access to models like Kimi, GLM, Qwen, etc. without infrastructure.

```python
# config.py
LLM_PROVIDER = "opencode"
OPENCODE_MODEL = "kimi-k2.6"
```

**Requirements:**
1. OpenCode GO API key in `.env`:
   ```
   OPENCODE_API_KEY=your-api-key
   ```

**Available models:**

| Model | API type |
|-------|----------|
| `kimi-k2.6`, `kimi-k2.5`, `glm-5.1`, `glm-5`, `deepseek-v4-pro`, `deepseek-v4-flash`, `mimo-v2.5`, `mimo-v2.5-pro` | OpenAI-compatible |
| `qwen3.7-max`, `qwen3.7-plus`, `qwen3.6-plus`, `minimax-m3`, `minimax-m2.7`, `minimax-m2.5` | Anthropic-compatible |

The client automatically detects which format to use based on the model.

---

## Troubleshooting

### Error: "Stored vector dimension does not match"

**Cause:** You changed the embedding model without re-indexing.

**Solution:**
```bash
python rag.py index
```

### Error: "Could not connect to Ollama"

**Cause:** Ollama is not running.

**Solution:**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve
```

### Error: "Invalid OpenCode API key"

**Cause:** `OPENCODE_API_KEY` is not configured or is incorrect.

**Solution:**
1. Verify that `.env` exists and contains the key
2. Verify that the key is valid
3. Reload the environment: `source venv/bin/activate`

### The query takes a long time to start responding

**Cause:** The model is "thinking". Models with reasoning like `qwen3.7-max` generate thinking tokens before the response.

**Solution:** Wait. The stderr output shows the thinking in real time.

### Results are not relevant

**Possible causes:**
1. **Embedding model too basic:** `all-MiniLM-L6-v2` is general-purpose. Try a larger or multilingual model.
2. **Threshold too high/low:** Adjust `SIMILARITY_THRESHOLD` in `config.py`.
3. **Poorly curated documents:** Verify that the `.md` files have correct frontmatter and clear technical content.
4. **Re-ranking disabled:** Enable `RERANK_ENABLED = True` to improve precision.

### The context exceeds the LLM budget

**Cause:** The chunks are too long or there are too many.

**Solution:**
- Reduce `TOP_K` (fewer candidates)
- Reduce `RERANK_TOP_K` (fewer final results)
- Adjust `CONTEXT_TOKEN_BUDGET` according to the model

---

## Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/

# With verbose
pytest tests/ -v

# Specific test
pytest tests/test_chunker.py -v
```

**Current coverage:**
- `test_cache.py`: Embedding cache (4 tests)
- `test_chunker.py`: Markdown parser (5 tests)
- `test_hyde.py`: HyDE transformer (2 tests)
- `test_reranker.py`: Cross-encoder reranker (3 tests, mocked)
- `test_vectorstore.py`: VectorStore (5 tests)

**19/19 tests pass.**

---

## Concepts covered

- **Architecture:** Intel x86 32-bit, Protected Mode
- **Structures:** GDT (Global Descriptor Table), IDT (Interrupt Descriptor Table)
- **Memory management:** Paging, Page Directory, Page Tables
- **Control registers:** CR0, CR2, CR3
- **System instructions:** `lgdt`, `lidt`, `iret`, `cli`, `sti`, `in/out`, EFLAGS manipulation

---

## License

Open Source
