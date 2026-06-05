# Análisis Crítico del Estado del Proyecto

## Inventario Actual

| Componente | Implementación | Estado |
|---|---|---|
| Embedder | 3 providers (local, Ollama, OpenAI) | Funcional |
| VectorStore | NumPy + JSON, búsqueda lineal | Básico |
| Chunker | Split por `## ` | Ingenuo |
| LLM | 2 clientes (Ollama, OpenCode) | Funcional |
| CLI | `index` / `query` | Mínima |
| Datos | 1 doc (GDT.md), 10 chunks | Semilla |

---

## 1. CHUNKER — El problema más grave después de la curación

`chunker/markdown.py` hace exactamente lo que `CONTEXT.md` dice que NO hay que hacer: fragmentación mecánica por heading, sin semántica.

- **Solo parte por `## `.** Ignora `###`, `####`. Si un documento usa subsecciones, las fusiona con el padre.
- **No extrae metadatos enriquecidos.** CONTEXT.md pide `{arquitectura, componente, tipo_informacion, modo}` pero solo guarda `{source, section}`.
- **No trata bloques de código de forma especial.** Un bloque NASM y su explicación textual son conceptos distintos que deberían tener embeddings separados (el modelo de embedding no "entiende" assembler dentro de texto natural).
- **Sin overlap entre chunks.** La transición entre "Access Byte" y "Flags y Límite Extendido" pierde continuidad contextual.
- **No hay detección de chunks irrelevantes.** El chunk "Introducción" (`# GDT - Global Descriptor Table...`) es una frase genérica que no aporta al retrieval.

## 2. VECTORSTORE — Fuerza bruta que no escala

`vectorstore/store.py`:

- **Búsqueda lineal O(n).** Con 10 chunks es irrelevante, pero con cientos de documentos se vuelve inviable. No hay índice (FAISS, HNSW).
- **Vectores como lista de Python.** Se convierten a `np.array()` en cada `search()`. Debería mantenerse como `ndarray` persistente en memoria.
- **No hay normalización.** La cosine similarity recalcula `norm(a) * norm(b)` en cada búsqueda. Normalizando al almacenar, sería solo dot product.
- **Sin validación de consistencia.** Si se cambia de modelo de embedding (dimensión distinta) y se hace `query` sin re-indexar, no hay chequeo — falla silenciosamente o da resultados basura.
- **`clear()` + rebuild en cada `index()`.** No hay indexación incremental ni hash-based caching de embeddings.

## 3. EMBEDDINGS — Sin batching ni caché

- **`LocalEmbedder.embed()`** procesa 1 texto por vez. `SentenceTransformer.encode()` acepta listas — durante indexación, el batch processing sería órdenes de magnitud más rápido.
- **`OllamaEmbedder`** hace 1 request HTTP por chunk. Sin batching.
- **No hay caché de embeddings.** Si un chunk no cambió entre indexaciones, su embedding tampoco. Un hash del contenido evitaría recalcular.
- **`OpenAIEmbedder._dimension`** hardcodeada con un `if "small" in model_name` — frágil, no cubre todos los modelos.

## 4. RETRIEVAL — Pipeline incompleto

- **No hay re-ranking.** Los resultados se devuelven por cosine similarity directo. Un cross-encoder como segunda pasada mejoraría mucho la precisión.
- **No hay query transformation.** La query se embedde tal cual. Técnicas como HyDE (Hypothetical Document Embeddings) o query expansion son críticas para dominio técnico donde el usuario pregunta en lenguaje natural pero los documentos usan terminología de hardware.
- **No hay metadata filtering.** Los metadatos se almacenan pero nunca se usan para filtrar. Debería poder buscarse solo en chunks con `componente: "IDT"` o `modo: "protegido"`.
- **TOP_K=3 fijo.** No hay estrategia de "llenar el context window" del LLM. Con chunks cortos, 3 fragmentos pueden ser insuficientes; con chunks largos, pueden exceder el window.
- **Threshold 0.3 bajado "a ojo"** (git log: 0.7 → 0.5 → 0.3). No hay evaluación sistemática de retrieval (recall@k, MRR, etc.).

## 5. PROMPT ENGINEERING — Redundancia y falta de estructura

- **Doble inyección de contexto.** El `system_prompt` ya contiene `{context}`, y además el `user` message envía `f"Contexto:\n{context}\n\nPregunta: {query}"`. El contexto viaja duplicado.
- **No hay instrucciones de formato de salida.** El LLM no sabe si debe responder con código NASM, explicación teórica, o ambos.
- **No hay citations.** El prompt no pide que el LLM cite qué fragmento usó para cada afirmación, lo cual es clave para verificabilidad en bajo nivel.

## 6. ESTRUCTURA DE CÓDIGO

- **No hay interfaz abstracta para LLMs.** Los embedders tienen `Embedder(ABC)`, pero `OllamaClient` y `OpenCodeClient` no comparten base. Deberían tener un `LLMClient(ABC)`.
- **Lógica de streaming/thinking duplicada** en 3 métodos (`ollama.generate`, `opencode._generate_openai`, `opencode._generate_anthropic`).
- **`contexto_rag_x86.txt`** es una versión anterior de `CONTEXT.md` — redundante, debería eliminarse.
- **`.obsidian/`** trackeado en git (no está en `.gitignore`).
- **`storage/`** está en `.gitignore` pero los archivos fueron commiteados igualmente.
- **Cero tests.** No hay forma de validar que un cambio no rompe el pipeline.
- **Sin logging.** Todo es `print()` — no hay niveles, no hay structured logging.
- **Manejo de errores mínimo.** Si Ollama no corre, explota con un `ConnectionError` crudo.

---

## 7. PRIORIDADES SUGERIDAS (por impacto)

| Prioridad | Mejora | Impacto |
|---|---|---|
| **P0** | Chunker semántico con metadatos ricos + tratamiento especial de bloques de código | Alto — mejora retrieval directamente |
| **P0** | Normalización de vectores + batch embedding | Alto — eficiencia de indexación y búsqueda |
| **P1** | Interfaz abstracta LLM + dedup de streaming | Medio — mantenibilidad |
| **P1** | Eliminar duplicación de contexto en prompts + agregar citations | Alto — calidad de respuesta |
| **P1** | Metadata filtering en search | Alto — precisión de retrieval |
| **P2** | Re-ranking con cross-encoder | Alto — precisión final |
| **P2** | Query transformation (HyDE) | Medio-Alto — recall |
| **P2** | Caché de embeddings por hash | Medio — eficiencia de re-indexación |
| **P3** | Migrar a FAISS/ChromaDB cuando crezca el dataset | Medio — escalabilidad |
| **P3** | Tests + logging + manejo de errores | Medio — robustez |
| **P3** | Limpiar `contexto_rag_x86.txt`, `.obsidian/`, `storage/` de git | Bajo — higiene |
