# Análisis Crítico — Iteración 4

## Resumen de cambios desde análisis 3

| Issue (análisis 3) | Commit | Estado |
|---|---|---|
| Regex inconsistente `_remove_code_blocks` | `66e813e` | **Resuelto** — `(?:\w+)?` permite bloques sin lenguaje |
| Headings dentro de bloques de código | `66e813e` | **Resuelto** — flag `in_code_block` en `_split_by_headings` |
| Caché sin invalidación por modelo | `1e78342` | **Resuelto** — hash incluye `model_name` |
| Caché en JSON (ineficiente) | `1e78342` | **Resuelto** — migrado a pickle |
| `VectorStore.add()` O(N²) | `1e78342` | **Resuelto** — `_pending_vectors` + flush batch |
| `DEBUG_SHOW_CONTEXT = True` | `3d087c9` | **Resuelto** — `False` por defecto |
| Lazy-load Reranker/HyDE | `3d087c9` | **Resuelto** — `_get_reranker()` / `_get_hyde()` |
| HyDE imprime por stdout | `3d087c9` | **Resuelto** — `silent=True` en llamada interna |
| Nomenclatura LLM confusa | `2498000` | **Resuelto** — `OLLAMA_MODEL` |
| `pytest` en `requirements.txt` | `aee2a70` | **Resuelto** — movido a `requirements-dev.txt` |
| Tests de reranker descargan modelo | `aee2a70` | **Resuelto** — `@patch('CrossEncoder')` |
| `storage/` commiteado en git | `1e78342` | **Resuelto** — ya no trackeado |

**Score: 12/12 issues resueltos.** Iteración perfecta.

---

## 1. PROBLEMAS NUEVOS INTRODUCIDOS

### 1.1 Test de normalización roto — `_pending_vectors` no se flushea

`tests/test_vectorstore.py:59-61`:
```python
store.add([2.0, 0.0, 0.0], "text1", {})
norm = np.linalg.norm(store.vectors[0])  # IndexError
```
Con el refactor de `_pending_vectors` (`1e78342`), `add()` ya no escribe directamente en `self.vectors`. El flush solo ocurre en `search()` y `save()`. El test accede a `store.vectors[0]` sin flush previo — `self.vectors` sigue siendo `np.array([])` vacío, lo que produce `IndexError`.

**Fix:** Agregar `store.save()` o llamar `store._flush_pending()` antes del assert, o testear la normalización a través de `search()`.

### 1.2 GDT.md tiene frontmatter pero el chunker lo ignora parcialmente

`data/curated/GDT.md:1-6` ahora tiene frontmatter YAML:
```yaml
---
architecture: x86_32
component: GDT
mode: protected
tags: [segmentation, memory, descriptors]
---
```
El chunker lo parsea correctamente y genera metadatos enriquecidos. Sin embargo, los vectores en `storage/` fueron indexados **antes** de agregar el frontmatter (pre-commit `8ead644`). El storage actual tiene metadatos pobres `{source, section}` sin `architecture`, `component`, `mode` ni `tags`. El metadata filtering no funciona hasta re-indexar.

**Acción:** Ejecutar `python rag.py index` para regenerar con los metadatos enriquecidos.

---

## 2. PROBLEMAS PENDIENTES (residuales)

### 2.1 `main()` descarta el retorno de `query()`

`rag.py:183`: `rag.query(question)` se llama pero el string retornado no se imprime ni captura. La respuesta se imprime por streaming dentro del LLM client, pero el valor de retorno se pierde. Si en algún momento se usa `RAGSystem` como librería (no CLI), el caller no tiene forma de obtener la respuesta si el LLM client no imprime directamente.

### 2.2 Sin `conftest.py` ni fixtures compartidas

Los 5 archivos de test crean `tempfile.TemporaryDirectory()` manualmente en cada método. Debería haber fixtures de pytest (`@pytest.fixture`) para `VectorStore`, `EmbeddingCache`, y `MarkdownChunker` con directorios temporales compartidos.

### 2.3 Sin `pyproject.toml`

El proyecto no es instalable como paquete Python. No se puede hacer `pip install -e .` ni distribuir. Los imports usan rutas relativas al CWD (`from embedder import ...`), lo que requiere ejecutar siempre desde la raíz del proyecto.

### 2.4 Modelo de embedding generalista — sin métricas

`all-MiniLM-L6-v2` (384 dims) es generalista. No hay evaluación de retrieval (recall@k, MRR, NDCG) para cuantificar la calidad actual ni comparar con modelos más capaces. Sin métricas, cualquier cambio de modelo es un salto de fe.

### 2.5 `TOP_K` y `SIMILARITY_THRESHOLD` sin justificación empírica

`config.py:24-25`: `TOP_K = 3` y `SIMILARITY_THRESHOLD = 0.3` son valores arbitrarios. El threshold fue bajado iterativamente (0.7 → 0.5 → 0.3) según el git log, sin evaluación sistemática. Con re-ranking habilitado, el `TOP_K` del retrieval inicial debería ser más alto (ej: 10) para darle más candidatos al cross-encoder.

### 2.6 Sin estrategia de context window budget

`rag.py:138-143`: Los chunks se concatenan sin límite de tokens. Si el LLM tiene un context window de 4K tokens y los 3 chunks suman 3K, la query + respuesta quedan comprimidos en 1K. No hay conteo de tokens ni truncamiento adaptativo.

### 2.7 `RERANK_TOP_K = 3` duplica `TOP_K = 3`

`config.py:24,29`: Ambos son 3. El retrieval busca 3 y el reranker devuelve 3 — el reranker no tiene efecto real porque no hay candidatos extra para reordenar. El flujo correcto sería `TOP_K = 10` → rerank → `RERANK_TOP_K = 3`.

### 2.8 Overlap contamina embeddings de código

`chunker/markdown.py:138-153`: El overlap agrega las últimas N líneas del chunk anterior al inicio del siguiente. Si el chunk anterior es un bloque NASM y el siguiente es explicación, el overlap inyecta assembler al inicio del chunk de explicación, ensuciando su embedding. El overlap debería ser consciente del tipo de chunk (`code` vs `explanation`).

### 2.9 `pickle` como formato de caché — riesgo de seguridad

`embedder/cache.py:24`: `pickle.load()` ejecuta código arbitrario al deserializar. Si el archivo de caché se corrompe o es manipulado, puede ejecutar código malicioso. Para un proyecto open-source donde los usuarios comparten cachés, esto es un vector de ataque. Alternativas: `msgpack`, `orjson`, o `numpy.save` para los vectores + JSON para las keys.

### 2.10 Sin validación de que `RERANK_TOP_K <= TOP_K`

No hay chequeo en runtime de que `RERANK_TOP_K` sea menor o igual a `TOP_K`. Si alguien configura `TOP_K = 2` y `RERANK_TOP_K = 5`, el reranker pedirá 5 resultados pero solo recibirá 2 — funciona por accidente pero la configuración es inconsistente.

### 2.11 README desactualizado

`README.md:42`: Dice `chunker/ # Parser de Markdown por headings` pero ahora es un chunker semántico con YAML frontmatter, separación de código, y overlap. No menciona `reranker/`, `retrieval/`, `logger.py`, ni las nuevas capacidades. Tampoco menciona `requirements-dev.txt`.

---

## 3. ESTADO ACTUAL DEL PIPELINE

```
┌─────────────────────────────────────────────────────────────────┐
│                        RAGSystem                                │
│                                                                 │
│  ┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌─────────┐ │
│  │ Chunker  │──>│ Embedder     │──>│ Vector   │──>│ Reranker│ │
│  │ (YAML +  │   │ (batch +     │   │ Store    │   │ (lazy)  │ │
│  │  code    │   │  cache +     │   │ (ndarray │   │         │ │
│  │  split)  │   │  model-hash) │   │  + norm) │   │         │ │
│  └──────────┘   └──────────────┘   └──────────┘   └─────────┘ │
│                                                     │           │
│  ┌──────────┐   ┌──────────────┐   ┌──────────┐   │           │
│  │ HyDE     │──>│ Embedder     │──>│ Search   │<──┘           │
│  │ (lazy +  │   │ (query)      │   │ (filter  │               │
│  │  silent) │   │              │   │  + meta) │               │
│  └──────────┘   └──────────────┘   └──────────┘               │
│                                                     │           │
│  ┌──────────────────────────────────────────────────┘           │
│  │                                                              │
│  │  ┌──────────┐                                                │
│  └─>│ LLM      │──> stdout (streaming + thinking)              │
│     │ (ABC +   │                                                │
│     │  silent) │                                                │
│     └──────────┘                                                │
└─────────────────────────────────────────────────────────────────┘
```

**Componentes maduros:** Embedder, VectorStore, Chunker, LLM abstraction, Logging, Error handling, Tests.

**Componentes que necesitan trabajo:** Evaluación de retrieval, context budget, tuning de parámetros.

---

## 4. PRIORIDADES ACTUALIZADAS

| Prioridad | Mejora | Impacto | Esfuerzo |
|---|---|---|---|
| **P0** | Fix test de normalización (`_pending_vectors`) | Crítico — test roto | Mínimo |
| **P0** | Re-indexar storage (metadatos enriquecidos de frontmatter) | Crítico — metadata filtering no funciona | Mínimo |
| **P1** | `TOP_K = 10` para dar candidatos al reranker | Alto — mejora retrieval real | Mínimo |
| **P1** | Context window budget (token counting + truncamiento) | Alto — evita overflow del LLM | Medio |
| **P1** | Overlap type-aware (no mezclar código con explicación) | Medio — calidad de embeddings | Bajo |
| **P2** | `conftest.py` con fixtures compartidas | Medio — mantenibilidad de tests | Bajo |
| **P2** | Validación `RERANK_TOP_K <= TOP_K` en config | Bajo — robustez | Mínimo |
| **P2** | Reemplazar pickle por formato seguro (msgpack/orjson) | Medio — seguridad | Bajo |
| **P2** | Actualizar README con arquitectura actual | Bajo — documentación | Mínimo |
| **P3** | Métricas de retrieval (recall@k, MRR) | Alto — evaluación objetiva | Alto |
| **P3** | `pyproject.toml` para instalabilidad | Bajo — distribución | Medio |
| **P3** | Evaluar modelo de embedding más capaz | Medio-Alto — recall | Alto |
| **P3** | Capturar retorno de `query()` en `main()` | Bajo — limpieza | Mínimo |
