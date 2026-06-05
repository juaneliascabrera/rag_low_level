# Análisis Crítico — Iteración 3

## Resumen de cambios desde análisis 2

| Issue (análisis 2) | Commit | Estado |
|---|---|---|
| Storage inconsistente post-normalización | `d17bf4b` | **Resuelto** — `add()` normaliza, `load()` valida dimensión |
| `load()` convierte ndarray a list | `d17bf4b` | **Resuelto** — mantiene ndarray en memoria |
| Parámetro `context` muerto en `generate()` | `d17bf4b` | **Resuelto** — eliminado del signature |
| Sin interfaz abstracta para LLMs | `353b54a` | **Resuelto** — `LLMClient(ABC)` en `llm/base.py` |
| Streaming/thinking duplicado | `353b54a` | **Resuelto** — helpers en base class |
| Sin logging | `353b54a` | **Resuelto** — `logger.py` con niveles |
| Sin manejo de errores | `353b54a` | **Resuelto** — try/except con mensajes claros |
| `embed_batch` parcial (Ollama/OpenAI) | `353b54a` | **Resuelto** — batch nativo para ambos |
| OpenAIEmbedder dimension hardcodeada | `353b54a` | **Resuelto** — dict `MODEL_DIMENSIONS` |
| Sin metadata filtering | `8ead644` | **Resuelto** — `_matches_filter` en search |
| Sin re-ranking | `8ead644` | **Resuelto** — `Reranker` con CrossEncoder |
| Sin query transformation (HyDE) | `8ead644` | **Resuelto** — `HyDETransformer` |
| Sin caché de embeddings | `8ead644` | **Resuelto** — `EmbeddingCache` con SHA-256 |
| Sin tests | `8ead644` | **Resuelto** — 5 archivos de test |
| Chunker sin metadatos ricos | `8ead644` | **Resuelto** — YAML frontmatter, code/explanation split |
| Prompt sin formato ni citations | `8ead644` | **Resuelto** — instrucciones de formato + `[Fragmento N]` |

**Score: 16/17 issues resueltos.** Iteración muy productiva.

---

## 1. PROBLEMAS NUEVOS INTRODUCIDOS

### 1.1 `VectorStore.add()` es O(N²) — `np.vstack` incremental

`vectorstore/store.py:28`:
```python
self.vectors = np.vstack([self.vectors, normalized])
```
Cada `add()` copia todo el array existente. Con 100 chunks son ~5000 copias de vectores. Durante indexación debería acumular en lista y construir el ndarray una sola vez al final.

### 1.2 Inconsistencia de regex en chunker — bloques de código sin lenguaje

`chunker/markdown.py:123` vs `chunker/markdown.py:128`:
- `_extract_code_blocks`: `r'```(\w+)?\n(.*?)```'` — captura bloques **con o sin** lenguaje
- `_remove_code_blocks`: `r'```\w+?\n.*?```'` — requiere **al menos un** carácter de lenguaje

Si un bloque es ` ```\ncode\n``` ` (sin lenguaje), se extrae como code chunk pero **no** se remueve del explanation chunk. Resultado: duplicación de contenido.

### 1.3 Caché sin invalidación por modelo

`embedder/cache.py:16`: El hash es solo del texto (`SHA-256(text)`). Si se cambia de modelo de embedding (ej: `all-MiniLM-L6-v2` → `all-mpnet-base-v2`), el caché devuelve vectores del modelo anterior. El hash debería incluir el nombre/dimensión del modelo.

### 1.4 HyDE imprime por stdout — confuso para el usuario

`retrieval/hyde.py:19`: `self.llm.generate()` usa el mismo LLM client que imprime thinking + respuesta por stdout/stderr. Cuando HyDE está habilitado, el usuario ve **dos** respuestas: primero el "documento hipotético" y luego la respuesta real. Debería haber un modo silencioso en el LLM client para llamadas internas.

### 1.5 `DEBUG_SHOW_CONTEXT` habilitado por defecto

`config.py:33`: Commit `e66417b` lo dejó en `True`. Debería ser `False` por defecto; es una herramienta de debug.

### 1.6 Headings dentro de bloques de código rompen el chunking

`chunker/markdown.py:64`: El regex `r'^(#{1,4})\s+(.+)$'` se aplica línea por línea sin saber si está dentro de un bloque de código. Si un bloque NASM contiene un comentario como `; ## Section`, o si hay texto literal con `##`, el parser lo interpreta como heading y corta el chunk prematuramente.

---

## 2. PROBLEMAS PENDIENTES

### 2.1 `storage/` sigue commiteado en git

Está en `.gitignore` pero los archivos ya estaban trackeados. Git no los des-trackea automáticamente. Hay que ejecutar `git rm --cached -r storage/`.

### 2.2 `config.py` con nomenclatura LLM confusa

Dos variables separadas: `LLM_MODEL = "gemma4:e4b-it-qat"` (usado por Ollama) y `OPENCODE_MODEL = "kimi-k2.6"` (usado por OpenCode). No queda claro cuál es el "activo" sin leer el código. Sugerencia: unificar en `LLM_MODEL` con un solo valor, o renombrar a `OLLAMA_MODEL`.

### 2.3 Modelo de embedding generalista

`all-MiniLM-L6-v2` (384 dims) es generalista. Para un dominio tan específico como x86 assembly, la calidad de retrieval es limitada. No hay métricas de evaluación (recall@k, MRR) para cuantificar el impacto.

### 2.4 `main()` descarta el retorno de `query()`

`rag.py:171`: `rag.query(question)` se llama pero el string retornado no se imprime ni usa. La respuesta se imprime por streaming dentro del LLM client, pero el retorno se pierde.

### 2.5 Reranker y HyDE se cargan en `__init__` — no lazy

`rag.py:23-24`: El CrossEncoder se descarga y carga en memoria al crear `RAGSystem`, incluso si solo se va a hacer `index`. Debería ser lazy-loaded (cargar en el primer `query()`).

### 2.6 Tests de reranker descargan modelo real

`tests/test_reranker.py:7`: `Reranker()` sin mock descarga el cross-encoder (~80MB). Los tests deberían ser rápidos y offline; este test depende de red y de HuggingFace.

### 2.7 `pytest` en `requirements.txt`

`requirements.txt:6`: `pytest` es dependencia de desarrollo, no de runtime. Debería estar en `requirements-dev.txt` o en un grupo separado.

### 2.8 Caché serializa vectores como JSON

`embedder/cache.py:29`: `json.dump(self.cache, f)` con vectores float de 384+ dimensiones genera archivos enormes. Con 1000 chunks de 384 dims, el JSON puede pesar 10+ MB. Alternativas: pickle, msgpack, o npy.

### 2.9 No hay `conftest.py` ni fixtures compartidas

Los tests crean `tempfile.TemporaryDirectory()` manualmente en cada método. Debería haber fixtures de pytest para el store, cache, y chunker.

### 2.10 Sin `pyproject.toml` ni `setup.py`

El proyecto no es instalable como paquete Python. No se puede hacer `pip install -e .` ni distribuir.

---

## 3. PRIORIDADES ACTUALIZADAS

| Prioridad | Mejora | Impacto | Esfuerzo |
|---|---|---|---|
| **P0** | Fix regex `_remove_code_blocks` (consistencia con `_extract`) | Alto — duplicación de chunks | Mínimo |
| **P0** | Caché: invalidación por modelo (incluir modelo en hash) | Alto — vectores incorrectos tras cambio de modelo | Mínimo |
| **P0** | `DEBUG_SHOW_CONTEXT = False` por defecto | Bajo — UX | Mínimo |
| **P1** | `VectorStore.add()` acumular en lista, construir ndarray al final | Medio — O(N²) → O(N) | Bajo |
| **P1** | Lazy-load de Reranker y HyDE | Medio — startup time y memoria | Bajo |
| **P1** | HyDE: modo silencioso en LLM client para llamadas internas | Medio — UX | Bajo |
| **P1** | Chunking: ignorar headings dentro de bloques de código | Alto — chunks rotos | Medio |
| **P1** | `git rm --cached -r storage/` | Bajo — higiene | Mínimo |
| **P2** | Tests: mock del reranker, conftest.py con fixtures | Medio — velocidad de CI | Bajo |
| **P2** | Separar `requirements-dev.txt` | Bajo — higiene | Mínimo |
| **P2** | Unificar nomenclatura LLM en config | Bajo — claridad | Mínimo |
| **P2** | Caché: formato binario (pickle/npy) en vez de JSON | Medio — eficiencia de I/O | Bajo |
| **P3** | `pyproject.toml` para instalabilidad | Bajo — distribución | Medio |
| **P3** | Evaluar modelo de embedding más capaz + métricas | Medio-Alto — recall | Alto |
