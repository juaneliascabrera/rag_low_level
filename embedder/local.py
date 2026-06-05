from sentence_transformers import SentenceTransformer
from logger import get_logger
from .base import Embedder

logger = get_logger(__name__)


class LocalEmbedder(Embedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        logger.info(f"Cargando modelo de embedding local: {model_name}")
        self.model = SentenceTransformer(model_name)
        self._dimension = self.model.get_embedding_dimension()
        logger.info(f"Modelo cargado. Dimensión: {self._dimension}")

    def embed(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        logger.info(f"Generando embeddings para {len(texts)} textos (batch)")
        embeddings = self.model.encode(texts, batch_size=32, show_progress_bar=True)
        return embeddings.tolist()

    def dimension(self) -> int:
        return self._dimension
