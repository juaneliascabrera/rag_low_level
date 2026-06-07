# Project Context: RAG Specialized in Low-Level (Intel x86 32-bit)

> **Date:** 2026-06-07  
> **Goal:** Centralize the context, technical challenges, suggested architecture, and roadmap for developing an open-source RAG system focused on optimizing LLM performance in low-level programming tasks, monolithic kernel development, and embedded systems.

---

## 1. Problem Statement

Commercial and generic LLMs demonstrate poor performance when interacting with hardware or writing Assembler code due to:

- **Scarcity of Training Data:** The volume of modern, public assembler code on platforms like GitHub is astronomically smaller compared to high-level languages (Python, JavaScript, C++).
- **Absence of Physical Context:** The models lack inherent understanding of memory maps, timings, pin states, or the exact distribution of specific control registers.
- **Absolute Architecture Dependence:** Code varies drastically depending on the physical architecture (Intel x86, ARM, RISC-V, AVR). Mixing syntactic conventions or non-existent registers leads to critical system failures (Triple Faults, Kernel Panics).

> In low-level development, precision is binary: a single incorrect bit in a control register voids the viability of the entire operating system or firmware.

---

## 2. Initial Project Scope (MVP)

To guarantee the system's viability and accuracy, the initial scope is strictly limited to:

- **Target Architecture:** Intel x86 32-bit (Classic educational/experimental architecture and monolithic kernel development in Protected Mode).
- **Critical Concepts to Cover:**
  * System initialization and structures: **GDT** (Global Descriptor Table), **IDT** (Interrupt Descriptor Table).
  * Memory Management: **Basic Paging**, Page Directory, Page Tables, control registers (**CR0, CR2, CR3**).
  * System Instruction Set: `lgdt`, `lidt`, `iret`, `cli`, `sti`, `in/out`, **EFLAGS** manipulation.

---

## 3. RAG System Architecture

The system is composed of modular components distributed locally to guarantee the developer's privacy and offline operation:

```
[ Curated Markdown Docs ] --> [ MarkdownChunker ] --> [ Semantic Chunks ]
                                                          |
                                                          v
[ LLM (Ollama/OpenCode) ] <-- [ RAGSystem ] <-- [ VectorStore (numpy) ]
                                   |                      ^
                                   |                      |
                              [ Reranker ]          [ EmbeddingCache ]
                              [ HyDE (optional) ]   [ Embedder (Ollama/Local/OpenAI) ]
```

### 3.A. Chunker Module (`chunker/`)

- **`MarkdownChunker`**: Splits curated Markdown documents into semantic chunks based on headings.
- Separates code blocks from explanatory text into distinct chunks.
- Adds overlap between consecutive chunks of the same type.
- Filters out irrelevant/too-short chunks.
- Supports YAML frontmatter for metadata (architecture, component, mode, tags).

### 3.B. Embedder Module (`embedder/`)

- **Interface**: `Embedder` (abstract base class) with `embed()`, `embed_batch()`, and `dimension()` methods.
- **Implementations**:
  - `LocalEmbedder`: Uses `sentence-transformers` for local embedding.
  - `OllamaEmbedder`: Uses Ollama API (`/api/embeddings` and `/api/embed` batch).
  - `OpenAIEmbedder`: Uses OpenAI-compatible API.
- **`EmbeddingCache`**: Pickle-based disk cache keyed by `model_name:text` SHA-256 hash.

### 3.C. VectorStore (`vectorstore/`)

- **`VectorStore`**: Custom numpy-based vector store with cosine similarity search.
- Pre-normalizes vectors on insertion for efficient dot-product search.
- Supports metadata filtering and similarity threshold.
- Persistence via `vectors.npy`, `texts.json`, `metadata.json`, `config.json`.

### 3.D. LLM Module (`llm/`)

- **Interface**: `LLMClient` (abstract base class) with `generate()` method supporting streaming output.
- **Implementations**:
  - `OllamaClient`: Ollama chat API with streaming and thinking/reasoning support.
  - `OpenCodeClient`: OpenCode API with auto-detection of OpenAI vs Anthropic format.
- Both support `silent` mode for internal use (e.g., HyDE).

### 3.E. Reranker (`reranker/`)

- **`Reranker`**: Cross-encoder based re-ranking using `sentence-transformers`.
- Re-scores retrieval results for improved precision.
- Lazy-loaded to avoid model loading when not needed.

### 3.F. Retrieval Enhancements (`retrieval/`)

- **`HyDETransformer`**: Hypothetical Document Embeddings.
- Generates a hypothetical technical document via LLM, then uses its embedding for search.
- Disabled by default (`HYDE_ENABLED = False`).

---

## 4. Pipeline Flow

### Indexing (`python rag.py index`)
1. Read all `.md` files from `data/curated/`.
2. Split each document into semantic chunks via `MarkdownChunker`.
3. Generate embeddings (with cache) via the configured `Embedder`.
4. Store normalized vectors, texts, and metadata in `VectorStore`.

### Querying (`python rag.py query <question>`)
1. Optionally transform the query via HyDE.
2. Embed the query/hypothetical document.
3. Search VectorStore for top-K similar chunks (with similarity threshold).
4. Re-rank results with cross-encoder (if enabled).
5. Deduplicate fragments.
6. Build context within token budget.
7. Generate response via LLM with system prompt + context injection.

---

## 5. Directory Structure

```
RAGIntelx86/
├── chunker/
│   ├── __init__.py
│   └── markdown.py          # MarkdownChunker
├── embedder/
│   ├── __init__.py
│   ├── base.py              # Embedder (ABC)
│   ├── cache.py             # EmbeddingCache
│   ├── local.py             # LocalEmbedder
│   ├── ollama.py            # OllamaEmbedder
│   └── openai_client.py     # OpenAIEmbedder
├── llm/
│   ├── __init__.py
│   ├── base.py              # LLMClient (ABC)
│   ├── ollama.py            # OllamaClient
│   └── opencode.py          # OpenCodeClient
├── reranker/
│   ├── __init__.py
│   └── reranker.py          # Reranker
├── retrieval/
│   ├── __init__.py
│   └── hyde.py              # HyDETransformer
├── vectorstore/
│   ├── __init__.py
│   └── store.py             # VectorStore
├── storage/                  # Persisted data (gitignored)
│   ├── cache/               # Embedding cache
│   ├── vectors.npy
│   ├── texts.json
│   ├── metadata.json
│   └── config.json
├── data/
│   └── curated/             # Source markdown documents
├── tests/                   # Unit tests
├── config.py                # Centralized configuration
├── logger.py                # Logging setup
├── rag.py                   # Main pipeline & CLI
├── requirements.txt         # Production dependencies
├── requirements-dev.txt     # Dev dependencies (pytest)
└── CONTEXT.md               # This file
```

---

## 6. Configuration

All configuration is centralized in `config.py`:

- **Embedding**: Provider (`local`/`ollama`/`openai`), model name
- **LLM**: Provider (`ollama`/`opencode`), model name, base URL
- **Reranker**: Enable/disable, model, top-K
- **HyDE**: Enable/disable
- **Search**: Top-K, similarity threshold, context token budget
- **Paths**: Data directory, storage directory, cache directory (all absolute)

Secrets are loaded from `.env` file via `python-dotenv`.

---

## 7. Development Roadmap

### Phase 1: Seed Dataset Preparation ✅
- Curated markdown documents for GDT structure.

### Phase 2: Local Vector Pipeline ✅
- Embedding, chunking, vector storage, and search implemented.

### Phase 3: User Interface and Integration ✅
- CLI interface with index and query commands.
- Multiple LLM provider support (Ollama, OpenCode).

### Phase 4: Retrieval Enhancements ✅
- Re-ranking with cross-encoder.
- HyDE (Hypothetical Document Embeddings).

### Phase 5: Expand Knowledge Base (In Progress)
- Add IDT, Paging, and control register documentation.

### Phase 6: Agent with Compilation Loop (Future)
- Connect with `nasm`/`gcc` for real-time syntax error correction.

---

*Document updated to reflect the current implementation.*
