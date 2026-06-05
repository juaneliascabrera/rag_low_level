import sys
from pathlib import Path
import config
from logger import setup_logging, get_logger
from embedder import LocalEmbedder, OllamaEmbedder, OpenAIEmbedder, EmbeddingCache
from vectorstore import VectorStore
from chunker import MarkdownChunker
from llm import OllamaClient, OpenCodeClient
from reranker import Reranker
from retrieval import HyDETransformer

setup_logging(config.LOG_LEVEL)
logger = get_logger(__name__)


class RAGSystem:
    def __init__(self):
        self.embedder = self._create_embedder()
        self.store = VectorStore(self.embedder.dimension(), config.STORAGE_DIR)
        self.chunker = MarkdownChunker()
        self.llm = self._create_llm()
        self.cache = EmbeddingCache(config.CACHE_DIR, config.EMBEDDING_MODEL)
        self._reranker = None
        self._hyde = None

    def _get_reranker(self):
        if self._reranker is None and config.RERANK_ENABLED:
            self._reranker = Reranker(config.RERANK_MODEL)
        return self._reranker

    def _get_hyde(self):
        if self._hyde is None and config.HYDE_ENABLED:
            self._hyde = HyDETransformer(self.llm)
        return self._hyde

    def _create_llm(self):
        if config.LLM_PROVIDER == "ollama":
            return OllamaClient(config.OLLAMA_BASE_URL, config.OLLAMA_MODEL)
        elif config.LLM_PROVIDER == "opencode":
            return OpenCodeClient(config.OPENCODE_MODEL, config.OPENCODE_API_KEY)
        else:
            raise ValueError(f"Proveedor de LLM no soportado: {config.LLM_PROVIDER}")

    def _create_embedder(self):
        if config.EMBEDDING_PROVIDER == "local":
            return LocalEmbedder(config.EMBEDDING_MODEL)
        elif config.EMBEDDING_PROVIDER == "ollama":
            return OllamaEmbedder(config.EMBEDDING_MODEL, config.OLLAMA_BASE_URL)
        elif config.EMBEDDING_PROVIDER == "openai":
            return OpenAIEmbedder(config.OPENAI_API_KEY, config.EMBEDDING_MODEL)
        else:
            raise ValueError(f"Proveedor de embedding no soportado: {config.EMBEDDING_PROVIDER}")

    def index(self):
        data_dir = Path(config.DATA_DIR)
        if not data_dir.exists():
            logger.error(f"Directorio {config.DATA_DIR} no existe")
            return

        md_files = list(data_dir.glob("*.md"))
        if not md_files:
            logger.warning(f"No se encontraron archivos .md en {config.DATA_DIR}")
            return

        logger.info(f"Indexando {len(md_files)} archivos...")
        logger.info(f"Modelo: {config.EMBEDDING_PROVIDER}/{config.EMBEDDING_MODEL}")
        logger.info(f"Dimensión: {self.embedder.dimension()}")

        self.store.clear()

        all_chunks = []
        for filepath in md_files:
            logger.info(f"  Procesando: {filepath.name}")
            chunks = self.chunker.chunk(str(filepath))
            all_chunks.extend(chunks)

        if all_chunks:
            logger.info(f"  Generando embeddings para {len(all_chunks)} chunks...")

            texts = [chunk["text"] for chunk in all_chunks]
            vectors = []

            texts_to_embed = []
            cache_hits = []

            for i, text in enumerate(texts):
                cached = self.cache.get(text)
                if cached:
                    vectors.append(cached)
                    cache_hits.append(i)
                else:
                    texts_to_embed.append((i, text))

            if cache_hits:
                logger.info(f"  Caché: {len(cache_hits)} chunks recuperados del caché")

            if texts_to_embed:
                logger.info(f"  Generando {len(texts_to_embed)} embeddings nuevos...")
                texts_only = [t[1] for t in texts_to_embed]
                new_vectors = self.embedder.embed_batch(texts_only)

                for (i, text), vector in zip(texts_to_embed, new_vectors):
                    self.cache.set(text, vector)
                    vectors.append(vector)

            for chunk, vector in zip(all_chunks, vectors):
                self.store.add(vector, chunk["text"], chunk["metadata"])

            self.cache.save()

        self.store.save()
        logger.info(f"Indexación completa: {len(self.store.texts)} chunks almacenados")

    def query(self, question: str, metadata_filter: dict | None = None) -> str:
        self.store.load()

        if self.store.vectors.size == 0:
            logger.error("Base de datos vacía. Ejecutá 'python rag.py index' primero.")
            return "Error: Base de datos vacía. Ejecutá 'python rag.py index' primero."

        search_query = question
        hyde = self._get_hyde()
        if hyde:
            search_query = hyde.transform(question)

        query_vector = self.embedder.embed(search_query)
        results = self.store.search(query_vector, config.TOP_K, config.SIMILARITY_THRESHOLD, metadata_filter)

        if not results:
            logger.warning("No se encontró contexto relevante para la consulta")
            return "No se encontró contexto relevante para tu consulta."

        reranker = self._get_reranker()
        if reranker:
            logger.info(f"Re-ranking {len(results)} resultados...")
            results = reranker.rerank(question, results, config.RERANK_TOP_K)

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Fragmento {i}] (similitud: {result['similarity']:.2f})\n{result['text']}")

        context = "\n\n".join(context_parts)
        system_prompt = config.SYSTEM_PROMPT.format(context=context)

        response = self.llm.generate(system_prompt, question)

        if config.DEBUG_SHOW_CONTEXT:
            print("\n" + "="*80, file=sys.stderr)
            print("CONTEXTO RECUPERADO:", file=sys.stderr)
            print("="*80, file=sys.stderr)
            for i, result in enumerate(results, 1):
                print(f"\n[Fragmento {i}] (similitud: {result['similarity']:.2f})", file=sys.stderr)
                if "rerank_score" in result:
                    print(f"Re-rank score: {result['rerank_score']:.2f}", file=sys.stderr)
                print(f"Source: {result['metadata'].get('source', 'N/A')}", file=sys.stderr)
                print(f"Section: {result['metadata'].get('section', 'N/A')}", file=sys.stderr)
                print("-"*80, file=sys.stderr)
                print(result['text'], file=sys.stderr)

        return response


def main():
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python rag.py index                    # Indexar documentos")
        print("  python rag.py query <pregunta>         # Hacer consulta")
        sys.exit(1)

    command = sys.argv[1]
    rag = RAGSystem()

    if command == "index":
        rag.index()
    elif command == "query":
        if len(sys.argv) < 3:
            logger.error("Especificá una pregunta")
            sys.exit(1)
        question = " ".join(sys.argv[2:])
        print("\n" + "="*80)
        print("RESPUESTA:")
        print("="*80)
        rag.query(question)
    else:
        logger.error(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
