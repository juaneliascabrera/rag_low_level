from sentence_transformers import SentenceTransformer
from .base import Embedder


class LocalEmbedder(Embedder):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()

    def embed(self, text: str) -> list[float]:
        return self.model.encode(text).tolist()

    def dimension(self) -> int:
        return self._dimension
