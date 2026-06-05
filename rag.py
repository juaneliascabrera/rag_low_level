import sys
from pathlib import Path
import config
from embedder import LocalEmbedder, OllamaEmbedder, OpenAIEmbedder
from vectorstore import VectorStore
from chunker import MarkdownChunker
from llm import OllamaClient, OpenCodeClient


class RAGSystem:
    def __init__(self):
        self.embedder = self._create_embedder()
        self.store = VectorStore(self.embedder.dimension(), config.STORAGE_DIR)
        self.chunker = MarkdownChunker()
        self.llm = self._create_llm()

    def _create_llm(self):
        if config.LLM_PROVIDER == "ollama":
            return OllamaClient(config.OLLAMA_BASE_URL, config.LLM_MODEL)
        elif config.LLM_PROVIDER == "opencode":
            return OpenCodeClient(config.OPENCODE_MODEL)
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
            print(f"Error: Directorio {config.DATA_DIR} no existe")
            return

        md_files = list(data_dir.glob("*.md"))
        if not md_files:
            print(f"No se encontraron archivos .md en {config.DATA_DIR}")
            return

        print(f"Indexando {len(md_files)} archivos...")
        print(f"Modelo: {config.EMBEDDING_PROVIDER}/{config.EMBEDDING_MODEL}")
        print(f"Dimensión: {self.embedder.dimension()}")

        self.store.clear()

        for filepath in md_files:
            print(f"  Procesando: {filepath.name}")
            chunks = self.chunker.chunk(str(filepath))
            for chunk in chunks:
                vector = self.embedder.embed(chunk["text"])
                self.store.add(vector, chunk["text"], chunk["metadata"])

        self.store.save()
        print(f"Indexación completa: {len(self.store.vectors)} chunks almacenados")

    def query(self, question: str) -> str:
        self.store.load()

        if not self.store.vectors:
            return "Error: Base de datos vacía. Ejecutá 'python rag.py index' primero."

        query_vector = self.embedder.embed(question)
        results = self.store.search(query_vector, config.TOP_K, config.SIMILARITY_THRESHOLD)

        if not results:
            return "No se encontró contexto relevante para tu consulta."

        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[Fragmento {i}] (similitud: {result['similarity']:.2f})\n{result['text']}")

        context = "\n\n".join(context_parts)
        system_prompt = config.SYSTEM_PROMPT.format(context=context)

        response = self.llm.generate(system_prompt, context, question)
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
            print("Error: Especificá una pregunta")
            sys.exit(1)
        question = " ".join(sys.argv[2:])
        print("\n" + "="*80)
        print("RESPUESTA:")
        print("="*80)
        rag.query(question)
    else:
        print(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
