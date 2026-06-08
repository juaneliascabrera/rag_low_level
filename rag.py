import sys
from pathlib import Path
from tqdm import tqdm
import config
from logger import setup_logging, get_logger
from embedder import LocalEmbedder, OllamaEmbedder, OpenAIEmbedder, EmbeddingCache
from vectorstore import VectorStore
from chunker import MarkdownChunker
from llm import OllamaClient, OpenCodeClient, ClaudeClient
from reranker import Reranker
from retrieval import HyDETransformer

setup_logging(config.LOG_LEVEL)
logger = get_logger(__name__)


class RAGSystem:
    def __init__(self):
        if config.RERANK_ENABLED and config.RERANK_TOP_K > config.TOP_K:
            raise ValueError(
                f"RERANK_TOP_K ({config.RERANK_TOP_K}) cannot be greater than TOP_K ({config.TOP_K})"
            )
        self.embedder = self._create_embedder()
        self.store = VectorStore(self.embedder.dimension(), config.STORAGE_DIR)
        self.store.load()
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
        elif config.LLM_PROVIDER == "claude":
            return ClaudeClient(config.CLAUDE_MODEL, config.ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported LLM provider: {config.LLM_PROVIDER}")

    def _create_embedder(self):
        if config.EMBEDDING_PROVIDER == "local":
            return LocalEmbedder(config.EMBEDDING_MODEL)
        elif config.EMBEDDING_PROVIDER == "ollama":
            return OllamaEmbedder(config.EMBEDDING_MODEL, config.OLLAMA_BASE_URL)
        elif config.EMBEDDING_PROVIDER == "openai":
            return OpenAIEmbedder(config.OPENAI_API_KEY, config.EMBEDDING_MODEL)
        else:
            raise ValueError(f"Unsupported embedding provider: {config.EMBEDDING_PROVIDER}")

    def index(self):
        data_dir = Path(config.DATA_DIR)
        if not data_dir.exists():
            logger.error(f"Directory {config.DATA_DIR} does not exist")
            return

        md_files = list(data_dir.glob("*.md"))
        if not md_files:
            logger.warning(f"No .md files found in {config.DATA_DIR}")
            return

        logger.info(f"Indexing {len(md_files)} files...")
        logger.info(f"Model: {config.EMBEDDING_PROVIDER}/{config.EMBEDDING_MODEL}")
        logger.info(f"Dimension: {self.embedder.dimension()}")

        self.store.clear()

        all_chunks = []
        # Process files with progress bar
        for filepath in tqdm(md_files, desc="Processing files", unit="file"):
            chunks = self.chunker.chunk(str(filepath))
            all_chunks.extend(chunks)

        if all_chunks:
            logger.info(f"Total chunks: {len(all_chunks)}")

            texts = [chunk["text"] for chunk in all_chunks]
            vectors = [None] * len(texts)

            texts_to_embed = []
            cache_hits = []

            # Check cache with progress
            for i, text in enumerate(tqdm(texts, desc="Checking cache", unit="chunk")):
                cached = self.cache.get(text)
                if cached:
                    vectors[i] = cached
                    cache_hits.append(i)
                else:
                    texts_to_embed.append((i, text))

            if cache_hits:
                logger.info(f"Cache: {len(cache_hits)} chunks retrieved from cache")

            if texts_to_embed:
                logger.info(f"Generating {len(texts_to_embed)} new embeddings...")
                
                # Process embeddings in batches with progress
                BATCH_SIZE = 32
                total_batches = (len(texts_to_embed) + BATCH_SIZE - 1) // BATCH_SIZE
                
                for batch_idx in tqdm(range(total_batches), desc="Embedding", unit="batch"):
                    start_idx = batch_idx * BATCH_SIZE
                    end_idx = min(start_idx + BATCH_SIZE, len(texts_to_embed))
                    batch_items = texts_to_embed[start_idx:end_idx]
                    batch_texts = [t[1] for t in batch_items]
                    
                    # Generate embeddings for this batch
                    batch_vectors = self.embedder.embed_batch(batch_texts)
                    
                    # Store in cache and vectors array
                    for (i, text), vector in zip(batch_items, batch_vectors):
                        self.cache.set(text, vector)
                        vectors[i] = vector

            # Add all vectors to store
            for chunk, vector in zip(all_chunks, vectors):
                self.store.add(vector, chunk["text"], chunk["metadata"])

            self.cache.save()

        self.store.save()
        logger.info(f"Indexing complete: {len(self.store.texts)} chunks stored")

    def _deduplicate_fragments(self, results: list[dict]) -> list[dict]:
        deduplicated = []
        seen_texts = set()
        for result in results:
            text = result["text"]
            # Skip exact duplicates
            if text in seen_texts:
                continue
            seen_texts.add(text)
            deduplicated.append(result)
        return deduplicated

    def query(self, question: str, metadata_filter: dict | None = None) -> str:
        if self.store.vectors.size == 0:
            logger.error("Empty database. Run 'python rag.py index' first.")
            return "Error: Empty database. Run 'python rag.py index' first."

        search_query = question
        hyde = self._get_hyde()
        if hyde:
            search_query = hyde.transform(question)

        query_vector = self.embedder.embed(search_query)
        results = self.store.search(query_vector, config.TOP_K, config.SIMILARITY_THRESHOLD, metadata_filter)

        if not results:
            logger.warning("No relevant context found for the query")
            return "No relevant context found for your query."

        reranker = self._get_reranker()
        if reranker:
            logger.info(f"Re-ranking {len(results)} results...")
            results = reranker.rerank(question, results, config.RERANK_TOP_K)

        results = self._deduplicate_fragments(results)

        context_parts = []
        total_tokens = 0
        for i, result in enumerate(results, 1):
            fragment = f"[Fragment {i}] (similarity: {result['similarity']:.2f})\n{result['text']}"
            fragment_tokens = len(fragment) // config.CHARS_PER_TOKEN
            if total_tokens + fragment_tokens > config.CONTEXT_TOKEN_BUDGET:
                logger.warning(f"Context budget reached: {total_tokens} tokens, truncating at fragment {i}")
                break
            context_parts.append(fragment)
            total_tokens += fragment_tokens

        context = "\n\n".join(context_parts)
        logger.info(f"Context: {len(context_parts)} fragments, ~{total_tokens} tokens")
        system_prompt = config.SYSTEM_PROMPT.format(context=context)

        response = self.llm.generate(system_prompt, question)

        if config.DEBUG_SHOW_CONTEXT:
            print("\n" + "="*80, file=sys.stderr)
            print("RETRIEVED CONTEXT:", file=sys.stderr)
            print("="*80, file=sys.stderr)
            for i, result in enumerate(results, 1):
                print(f"\n[Fragment {i}] (similarity: {result['similarity']:.2f})", file=sys.stderr)
                if "rerank_score" in result:
                    print(f"Re-rank score: {result['rerank_score']:.2f}", file=sys.stderr)
                print(f"Source: {result['metadata'].get('source', 'N/A')}", file=sys.stderr)
                print(f"Section: {result['metadata'].get('section', 'N/A')}", file=sys.stderr)
                print("-"*80, file=sys.stderr)
                print(result['text'], file=sys.stderr)

        return response


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python rag.py index                    # Index documents")
        print("  python rag.py query <question>         # Make a query")
        sys.exit(1)

    command = sys.argv[1]

    try:
        rag = RAGSystem()
    except (RuntimeError, ValueError) as e:
        logger.error(f"Failed to initialize: {e}")
        sys.exit(1)

    if command == "index":
        rag.index()
    elif command == "query":
        if len(sys.argv) < 3:
            logger.error("Please specify a question")
            sys.exit(1)
        question = " ".join(sys.argv[2:])
        print("\n" + "="*80)
        print("ANSWER:")
        print("="*80)
        try:
            rag.query(question)
        except KeyboardInterrupt:
            print("\n\nInterrupted.")
            sys.exit(130)
    else:
        logger.error(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
