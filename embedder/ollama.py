import requests
from .base import Embedder


class OllamaEmbedder(Embedder):
    def __init__(self, model_name: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        self._dimension = self._get_dimension()

    def _get_dimension(self) -> int:
        test_embedding = self.embed("test")
        return len(test_embedding)

    def embed(self, text: str) -> list[float]:
        response = requests.post(
            f"{self.base_url}/api/embeddings",
            json={"model": self.model_name, "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]

    def dimension(self) -> int:
        return self._dimension
