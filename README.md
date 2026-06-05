# RAG Intel x86 32-bit

Sistema RAG (Retrieval-Augmented Generation) especializado en programación de bajo nivel para Intel x86 de 32 bits en Modo Protegido. Optimiza el rendimiento de LLMs en tareas de desarrollo de kernels monolíticos y sistemas embebidos, eliminando alucinaciones críticas de hardware mediante recuperación de contexto verificado.

## Características

- **Embeddings intercambiables:** Local (sentence-transformers), Ollama, OpenAI
- **LLMs intercambiables:** Ollama local, OpenCode GO (OpenAI-compatible + Anthropic-compatible)
- **Chunking semántico:** Parser de Markdown con YAML frontmatter, separación de bloques de código, overlap configurable
- **Re-ranking con cross-encoder:** Mejora la precisión del retrieval
- **HyDE (opcional):** Query transformation con documentos hipotéticos
- **Metadata filtering:** Filtros por componente, arquitectura, modo, tipo
- **Context budget:** Truncamiento automático para evitar overflow del LLM
- **Caché de embeddings:** Persistencia con hash SHA256 por modelo
- **Tests unitarios:** Cobertura de cache, vectorstore, chunker, reranker, hyde

## Tabla de contenidos

1. [Requisitos previos](#requisitos-previos)
2. [Instalación](#instalación)
3. [Configuración](#configuración)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Preparar documentos](#preparar-documentos)
6. [Uso](#uso)
7. [Configuración detallada por proveedor](#configuración-detallada-por-proveedor)
8. [Troubleshooting](#troubleshooting)
9. [Tests](#tests)
10. [Conceptos cubiertos](#conceptos-cubiertos)

---

## Requisitos previos

- **Python 3.10+**
- **pip** (gestor de paquetes)
- Proveedor de embeddings (al menos uno):
  - `sentence-transformers` (local, sin servicios externos)
  - Ollama corriendo localmente
  - API key de OpenAI
- Proveedor de LLM (al menos uno):
  - Ollama corriendo localmente con un modelo descargado
  - API key de OpenCode GO (o de OpenAI/Anthropic si adaptas el código)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd RAGIntelx86
```

### 2. Crear entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# o en Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Para desarrollo (incluye pytest):

```bash
pip install -r requirements-dev.txt
```

---

## Configuración

### 1. Variables de entorno (APIs keys)

Copiá el archivo de ejemplo:

```bash
cp .env.example .env
```

Editá `.env` con tus API keys:

```bash
# OpenAI (opcional, solo si usás OpenAIEmbedder o el LLM de OpenAI)
OPENAI_API_KEY=sk-...

# OpenCode GO (opcional, si usás modelos de OpenCode)
OPENCODE_API_KEY=tu-api-key-aquí
```

⚠️ **Importante:** El archivo `.env` está en `.gitignore` y **no se sube al repositorio**. Cada usuario debe crear el suyo.

### 2. Configuración del modelo (`config.py`)

Editá `config.py` para elegir:

#### Embedding

```python
EMBEDDING_PROVIDER = "local"  # "local" | "ollama" | "openai"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

| Provider | Modelos recomendados | Requisitos |
|----------|---------------------|------------|
| `local` | `all-MiniLM-L6-v2` (384d, rápido), `all-mpnet-base-v2` (768d, mejor calidad) | Ninguno (descarga automática) |
| `ollama` | `nomic-embed-text`, `mxbai-embed-large` | Ollama corriendo local |
| `openai` | `text-embedding-3-small` (1536d), `text-embedding-3-large` (3072d) | `OPENAI_API_KEY` en `.env` |

#### LLM

```python
LLM_PROVIDER = "opencode"  # "ollama" | "opencode"
OLLAMA_MODEL = "gemma4:e4b-it-qat"
OLLAMA_BASE_URL = "http://localhost:11434"
OPENCODE_MODEL = "kimi-k2.6"
```

| Provider | Modelos ejemplo | Requisitos |
|----------|----------------|------------|
| `ollama` | `gemma4:e4b-it-qat`, `qwen2.5-coder:7b`, `deepseek-coder` | Ollama corriendo local |
| `opencode` | `kimi-k2.6`, `glm-5.1`, `qwen3.7-max` | `OPENCODE_API_KEY` en `.env` |

#### Parámetros de retrieval

```python
TOP_K = 10                      # Candidatos para el reranker
SIMILARITY_THRESHOLD = 0.3      # Umbral mínimo de similitud coseno
RERANK_ENABLED = True            # Usar cross-encoder para re-ranking
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
RERANK_TOP_K = 3                # Resultados finales después de re-rank
HYDE_ENABLED = False             # Query transformation con HyDE
CONTEXT_TOKEN_BUDGET = 3000      # Tokens máximos de contexto
```

---

## Estructura del proyecto

```
RAGIntelx86/
├── rag.py                    # CLI principal y orquestador
├── config.py                 # Configuración central
├── logger.py                 # Sistema de logging
├── .env.example              # Plantilla de variables de entorno
├── .gitignore
├── requirements.txt          # Dependencias de runtime
├── requirements-dev.txt      # Dependencias de desarrollo
├── README.md                 # Este archivo
├── CONTEXT.md                # Contexto detallado del proyecto
├── data/
│   └── curated/              # Documentos .md curados (frontmatter YAML)
├── embedder/
│   ├── base.py               # Interfaz abstracta Embedder
│   ├── local.py              # sentence-transformers local
│   ├── ollama.py             # Ollama API
│   ├── openai_client.py      # OpenAI API
│   ├── cache.py              # Caché de embeddings (pickle)
│   └── __init__.py
├── vectorstore/
│   ├── store.py              # VectorStore (NumPy + JSON)
│   └── __init__.py
├── chunker/
│   ├── markdown.py           # Parser semántico con YAML + code split
│   └── __init__.py
├── llm/
│   ├── base.py               # Interfaz abstracta LLMClient
│   ├── ollama.py             # Cliente Ollama (streaming + thinking)
│   ├── opencode.py           # Cliente OpenCode GO
│   └── __init__.py
├── reranker/
│   ├── reranker.py           # Cross-encoder re-ranking
│   └── __init__.py
├── retrieval/
│   ├── hyde.py               # HyDE query transformation
│   └── __init__.py
├── tests/                    # Tests unitarios
│   ├── test_cache.py
│   ├── test_chunker.py
│   ├── test_hyde.py
│   ├── test_reranker.py
│   ├── test_vectorstore.py
│   └── __init__.py
└── storage/                  # Generado automáticamente
    ├── vectors.npy
    ├── texts.json
    ├── metadata.json
    ├── config.json
    └── cache/
        └── embedding_cache.pkl
```

---

## Preparar documentos

### Formato de los archivos `.md`

Los documentos van en `data/curated/` y deben tener **YAML frontmatter** con metadatos:

```markdown
---
architecture: x86_32
component: GDT
mode: protected
tags: [segmentation, memory, descriptors]
---

# Título del documento

Introducción breve...

## Sección 1

Contenido explicativo con texto largo...

```nasm
; Código de ejemplo
mov eax, cr0
or eax, 1
mov cr0, eax
```

## Sección 2

Otra sección...
```

### Frontmatter

| Campo | Descripción | Default |
|-------|-------------|---------|
| `architecture` | Arquitectura objetivo | `x86_32` |
| `component` | Componente (GDT, IDT, paging, etc.) | Nombre del archivo |
| `mode` | Modo de operación | `protected` |
| `tags` | Lista de tags para filtrado | (ninguno) |

### Bloques de código

Los bloques de código se separan automáticamente como chunks independientes con `type: "code"` en los metadatos. Esto permite que el retrieval encuentre código relevante aunque el embedding no entienda assembler dentro de texto natural.

### Overlap

El chunker agrega overlap (default 3 líneas) entre chunks **del mismo tipo** (código con código, explicación con explicación) para mantener continuidad contextual sin contaminar embeddings de un tipo con el otro.

---

## Uso

### 1. Indexar documentos

La indexación genera embeddings de todos los `.md` en `data/curated/` y los persiste en `storage/`.

```bash
python rag.py index
```

**Output esperado:**

```
[INFO] embedder.local: Cargando modelo de embedding local: all-MiniLM-L6-v2
[INFO] embedder.local: Modelo cargado. Dimensión: 384
[INFO] Indexando 1 archivos...
[INFO]   Procesando: GDT.md
[INFO] chunker.markdown:   GDT.md: 19 chunks generados
[INFO]   Generando embeddings para 19 chunks...
[INFO]   Generando 19 embeddings nuevos...
[INFO] Indexación completa: 19 chunks almacenados
```

⚠️ **Cuándo re-indexar:**

- Primera vez
- Agregás o modificás documentos en `data/curated/`
- Cambiás `EMBEDDING_PROVIDER` o `EMBEDDING_MODEL`
- Cambiás `CHARS_PER_TOKEN` o parámetros del chunker

⚠️ **Si cambiás el modelo de embedding, la dimensión de los vectores cambia y el sistema detecta la inconsistencia.** Vas a ver un error pidiendo re-indexar.

### 2. Hacer consultas

```bash
python rag.py query "¿Cómo configuro un descriptor de segmento en la GDT?"
```

**Output esperado:**

```
================================================================================
RESPUESTA:
================================================================================
[Thinking]
El usuario pregunta sobre la GDT...

[Respuesta]
Según el contexto proporcionado, un descriptor de segmento de la GDT se configura...
```

### 3. Debug: ver el contexto recuperado

Activá `DEBUG_SHOW_CONTEXT = True` en `config.py` para ver qué fragmentos se recuperaron y sus scores de similitud/re-ranking.

---

## Configuración detallada por proveedor

### Opción 1: Local con sentence-transformers (recomendado para empezar)

**Ventajas:** Sin servicios externos, sin API keys, funciona offline.

```python
# config.py
EMBEDDING_PROVIDER = "local"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```

**Instalación:** Ya está en `requirements.txt` (`sentence-transformers`).

**Primera vez:** Descarga el modelo (~80MB) automáticamente.

### Opción 2: Ollama (local con Ollama)

**Ventajas:** Control total, múltiples modelos disponibles.

```python
# config.py
EMBEDDING_PROVIDER = "ollama"
EMBEDDING_MODEL = "nomic-embed-text"
OLLAMA_BASE_URL = "http://localhost:11434"
```

**Requisitos:**
1. Instalar Ollama: https://ollama.com/download
2. Descargar el modelo de embedding:
   ```bash
   ollama pull nomic-embed-text
   ```
3. (Opcional) Descargar el modelo de LLM:
   ```bash
   ollama pull gemma4:e4b-it-qat
   ```

**Uso:**
```python
LLM_PROVIDER = "ollama"
OLLAMA_MODEL = "gemma4:e4b-it-qat"
```

### Opción 3: OpenAI (embeddings y/o LLM)

**Ventajas:** Modelos de alta calidad.

```python
# config.py
EMBEDDING_PROVIDER = "openai"
EMBEDDING_MODEL = "text-embedding-3-small"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")  # En .env
```

⚠️ **Nota:** El código actual tiene `OpenAIEmbedder` pero el LLM client de OpenAI no está implementado. Solo OpenCode y Ollama están soportados como LLM. Si querés usar OpenAI como LLM, necesitás adaptar `llm/opencode.py` o crear `llm/openai.py`.

### Opción 4: OpenCode GO (modelos de OpenCode)

**Ventajas:** Acceso a modelos como Kimi, GLM, Qwen, etc. sin infraestructura.

```python
# config.py
LLM_PROVIDER = "opencode"
OPENCODE_MODEL = "kimi-k2.6"
```

**Requisitos:**
1. API key de OpenCode GO en `.env`:
   ```
   OPENCODE_API_KEY=tu-api-key
   ```

**Modelos disponibles:**

| Modelo | Tipo de API |
|--------|-------------|
| `kimi-k2.6`, `kimi-k2.5`, `glm-5.1`, `glm-5`, `deepseek-v4-pro`, `deepseek-v4-flash`, `mimo-v2.5`, `mimo-v2.5-pro` | OpenAI-compatible |
| `qwen3.7-max`, `qwen3.7-plus`, `qwen3.6-plus`, `minimax-m3`, `minimax-m2.7`, `minimax-m2.5` | Anthropic-compatible |

El cliente detecta automáticamente qué formato usar según el modelo.

---

## Troubleshooting

### Error: "Dimensión de vectores almacenados no coincide"

**Causa:** Cambiaste el modelo de embedding sin re-indexar.

**Solución:**
```bash
python rag.py index
```

### Error: "No se pudo conectar a Ollama"

**Causa:** Ollama no está corriendo.

**Solución:**
```bash
# Verificar si Ollama está corriendo
curl http://localhost:11434/api/tags

# Si no está, iniciarlo
ollama serve
```

### Error: "API key inválida para OpenCode"

**Causa:** `OPENCODE_API_KEY` no está configurada o es incorrecta.

**Solución:**
1. Verificá que `.env` exista y tenga la key
2. Verificá que la key sea válida
3. Recargá el entorno: `source venv/bin/activate`

### La query tarda mucho en empezar a responder

**Causa:** El modelo está "pensando" (thinking). Los modelos con razonamiento como `qwen3.7-max` generan tokens de thinking antes de la respuesta.

**Solución:** Esperá. El output por stderr muestra el thinking en tiempo real.

### Los resultados no son relevantes

**Causas posibles:**
1. **Modelo de embedding muy básico:** `all-MiniLM-L6-v2` es generalista. Probá con un modelo más grande o multilingüe.
2. **Threshold muy alto/bajo:** Ajustá `SIMILARITY_THRESHOLD` en `config.py`.
3. **Documentos mal curados:** Verificá que los `.md` tengan frontmatter correcto y contenido técnico claro.
4. **Re-ranking deshabilitado:** Activá `RERANK_ENABLED = True` para mejorar precisión.

### El contexto excede el budget del LLM

**Causa:** Los chunks son muy largos o hay muchos.

**Solución:**
- Reducí `TOP_K` (menos candidatos)
- Reducí `RERANK_TOP_K` (menos resultados finales)
- Ajustá `CONTEXT_TOKEN_BUDGET` según el modelo

---

## Tests

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt

# Correr todos los tests
pytest tests/

# Con verbose
pytest tests/ -v

# Test específico
pytest tests/test_chunker.py -v
```

**Cobertura actual:**
- `test_cache.py`: Caché de embeddings (4 tests)
- `test_chunker.py`: Parser de Markdown (5 tests)
- `test_hyde.py`: HyDE transformer (2 tests)
- `test_reranker.py`: Cross-encoder reranker (3 tests, con mock)
- `test_vectorstore.py`: VectorStore (5 tests)

**19/19 tests pasan.**

---

## Conceptos cubiertos

- **Arquitectura:** Intel x86 32-bit, Modo Protegido
- **Estructuras:** GDT (Global Descriptor Table), IDT (Interrupt Descriptor Table)
- **Gestión de memoria:** Paginación, Page Directory, Page Tables
- **Registros de control:** CR0, CR2, CR3
- **Instrucciones de sistema:** `lgdt`, `lidt`, `iret`, `cli`, `sti`, `in/out`, manipulación de EFLAGS

---

## Licencia

Open Source
