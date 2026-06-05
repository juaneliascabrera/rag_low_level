# Análisis Crítico — Iteración 2

## Cambios desde el análisis 1

| Issue (análisis 1) | Commit | Estado |
|---|---|---|
| Doble inyección de contexto en prompts | `f002dfb` | **Resuelto** |
| Sin normalización de vectores | `857b622` | **Resuelto** |
| Sin batch embedding | `5e3c474` | **Resuelto** |
| `contexto_rag_x86.txt` redundante | `4b0af5d` | **Resuelto** |
| `.obsidian/` trackeado en git | `4b0af5d` | **Resuelto** |

---

## 1. PROBLEMAS NUEVOS INTRODUCIDOS POR LOS CAMBIOS

### 1.1 Storage inconsistente — hay que re-indexar

Los vectores en `storage/vectors.npy` fueron generados **antes** de agregar la normalización (`857b622`). El `search()` ahora normaliza el query vector pero los vectores almacenados NO están normalizados. Esto produce cosine similarity incorrecta hasta que se ejecute `python rag.py index` de nuevo.

**Acción:** Re-indexar o agregar migración automática que detecte vectores no normalizados y los normalice en `load()`.

### 1.2 `load()` convierte ndarray a list innecesariamente

`vectorstore/store.py:72`:
```python
self.vectors = np.load(vectors_path).tolist()
```
Se carga un `.npy` (ndarray nativo) y se convierte a lista de Python. Luego en `search()` se vuelve a convertir a `np.array()`. Doble conversión inútil. Debería mantenerse como ndarray en memoria.

### 1.3 Parámetro `context` muerto en `generate()`

`llm/ollama.py:11` y `llm/opencode.py:18`: la firma es `generate(system_prompt, context, query)` pero `context` ya no se usa en ningún lado dentro del método (se eliminó la duplicación). Se sigue pasando desde `rag.py:88` pero es un dead parameter. Debería eliminarse del signature.

---

## 2. PROBLEMAS PENDIENTES DEL ANÁLISIS 1

### 2.1 CHUNKER — Sin cambios, sigue siendo el cuello de botella principal

`chunker/markdown.py` no fue modificado. Persisten todos los problemas:

- **Solo parte por `## `.** Ignora `###`, `####`.
- **Metadatos pobres.** Solo `{source, section}`. CONTEXT.md pide `{arquitectura, componente, tipo_informacion, modo}`.
- **Sin tratamiento especial de bloques de código.** El modelo de embedding no "entiende" assembler; un bloque NASM y su explicación textual deberían tener embeddings separados o al menos metadata diferenciada (`tipo: "codigo"` vs `tipo: "explicacion"`).
- **Sin overlap entre chunks.** Se pierde continuidad contextual entre secciones relacionadas.
- **Chunk "Introducción" irrelevante.** El primer chunk es una frase genérica que no aporta al retrieval.

### 2.2 `embed_batch` parcial — solo LocalEmbedder lo implementa

El fallback en `embedder/base.py:9` es un loop secuencial de `embed()`:
```python
def embed_batch(self, texts):
    return [self.embed(text) for text in texts]
```

- **`OllamaEmbedder`:** Usa el fallback — N requests HTTP secuenciales. Debería aprovechar el endpoint `/api/embed` (plural) de Ollama que acepta batch nativo, o al menos hacer concurrent requests.
- **`OpenAIEmbedder`:** Usa el fallback — N requests HTTP secuenciales. La API de OpenAI acepta listas en `input` para batch nativo en un solo request.

### 2.3 Sin interfaz abstracta para LLMs

`OllamaClient` y `OpenCodeClient` no comparten base. Deberían tener un `LLMClient(ABC)` con método `generate()`.

### 2.4 Lógica de streaming/thinking duplicada en 3 métodos

El patrón `thinking_started` / `content_started` / `print(..., file=sys.stderr)` se repite casi idéntico en `ollama.generate`, `opencode._generate_openai`, y `opencode._generate_anthropic`. Debería extraerse a un helper compartido o a la clase base.

### 2.5 Sin re-ranking

Los resultados se devuelven por cosine similarity directo. Un cross-encoder como segunda pasada mejoraría precisión, especialmente con un modelo de embedding generalista como `all-MiniLM-L6-v2`.

### 2.6 Sin query transformation

La query se embedde tal cual. Para un dominio donde el usuario pregunta en lenguaje natural ("cómo hago un segmento de código") pero los documentos usan terminología de hardware ("descriptor de segmento, Access Byte 0x9A"), técnicas como HyDE o query expansion son críticas.

### 2.7 Sin metadata filtering

Los metadatos se almacenan pero nunca se usan para filtrar búsquedas.

### 2.8 Sin validación de dimensión al cargar

Si se cambia de modelo de embedding y se hace `query` sin re-indexar, no hay chequeo de que la dimensión de los vectores almacenados coincida con la del embedder actual. Falla silenciosamente.

### 2.9 Sin caché de embeddings

Si un chunk no cambió entre indexaciones, su embedding tampoco. Un hash del contenido evitaría recalcular.

### 2.10 Prompt sin instrucciones de formato ni citations

El system prompt no especifica formato de salida (código NASM vs explicación teórica) ni pide citar qué fragmento se usó para cada afirmación.

### 2.11 Sin tests, logging, ni manejo de errores

- Cero tests.
- Todo es `print()` sin niveles de logging.
- Si Ollama no corre, explota con `ConnectionError` crudo.

### 2.12 `storage/` sigue commiteado

Está en `.gitignore` pero los archivos ya estaban trackeados antes de agregar la regla. Git no los des-trackea automáticamente — hay que hacer `git rm --cached storage/*`.

### 2.13 `main()` descarta el retorno de `query()`

`rag.py:112` llama `rag.query(question)` pero no imprime ni usa el string retornado. La respuesta se imprime por streaming dentro del LLM client, pero el retorno se pierde.

### 2.14 `config.py` con configuración LLM confusa

Hay dos variables separadas: `LLM_MODEL = "gemma4:e4b-it-qat"` (usado por Ollama) y `OPENCODE_MODEL = "kimi-k2.6"` (usado por OpenCode). No queda claro cuál es el "activo" sin leer el código.

### 2.15 Modelo de embedding generalista

`all-MiniLM-L6-v2` es un modelo generalista de 384 dimensiones. Para un dominio tan específico como x86 assembly, la calidad de retrieval es limitada. Opciones:
- Usar un modelo más grande (`all-mpnet-base-v2`, 768 dims).
- Fine-tunear sobre pares query-document del dominio.
- Evaluar con métricas de retrieval (recall@k, MRR) para cuantificar.

---

## 3. PRIORIDADES ACTUALIZADAS

| Prioridad | Mejora | Impacto | Esfuerzo |
|---|---|---|---|
| **P0** | Re-indexar (storage inconsistente post-normalización) | Crítico — resultados incorrectos ahora | Mínimo |
| **P0** | Chunker semántico con metadatos ricos + bloques de código separados | Alto — mejora retrieval directamente | Medio |
| **P1** | Eliminar dead parameter `context` en `generate()` | Bajo — limpieza | Mínimo |
| **P1** | `load()` mantener ndarray en vez de convertir a list | Medio — eficiencia | Mínimo |
| **P1** | Validación de dimensión al cargar vs embedder actual | Medio — robustez | Mínimo |
| **P1** | `embed_batch` nativo para Ollama y OpenAI | Medio — eficiencia de indexación | Bajo |
| **P1** | Interfaz abstracta LLM + extraer streaming helper | Medio — mantenibilidad | Medio |
| **P1** | Metadata filtering en search | Alto — precisión de retrieval | Bajo |
| **P2** | Prompt: instrucciones de formato + citations | Alto — calidad de respuesta | Mínimo |
| **P2** | Re-ranking con cross-encoder | Alto — precisión final | Medio |
| **P2** | Query transformation (HyDE) | Medio-Alto — recall | Medio |
| **P2** | Caché de embeddings por hash | Medio — eficiencia de re-indexación | Bajo |
| **P2** | `git rm --cached storage/*` | Bajo — higiene | Mínimo |
| **P3** | Tests + logging + manejo de errores | Medio — robustez | Alto |
| **P3** | Migrar a FAISS cuando crezca el dataset | Medio — escalabilidad | Medio |
| **P3** | Evaluar modelo de embedding más capaz | Medio-Alto — recall | Medio |
