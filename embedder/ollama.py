import requests
from logger import get_logger
from .base import Embedder

logger = get_logger(__name__)


class OllamaEmbedder(Embedder):
    def __init__(self, model_name: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url
        logger.info(f"Inicializando OllamaEmbedder: {model_name}")
        self._dimension = self._get_dimension()
        logger.info(f"Dimensión detectada: {self._dimension}")

    def _get_dimension(self) -> int:
        test_embedding = self.embed("test")
        return len(test_embedding)

    def embed(self, text: str) -> list[float]:
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model_name, "prompt": text},
                timeout=60
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except requests.exceptions.ConnectionError:
            logger.error(f"No se pudo conectar a Ollama en {self.base_url}")
            raise RuntimeError(f"Ollama no está corriendo en {self.base_url}")
        except requests.exceptions.Timeout:
            logger.error("Timeout al generar embedding con Ollama")
            raise RuntimeError("Timeout al generar embedding con Ollama")

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        logger.info(f"Generando {len(texts)} embeddings con Ollama (batch)")
        try:
            response = requests.post(
                f"{self.base_url}/api/embed",
                json={"model": self.model_name, "input": texts},
                timeout=300
            )
            response.raise_for_status()
            return response.json()["embeddings"]
        except requests.exceptions.ConnectionError:
            logger.error(f"No se pudo conectar a Ollama en {self.base_url}")
            raise RuntimeError(f"Ollama no está corriendo en {self.base_url}")
        except requests.exceptions.HTTPError:
            logger.warning("Endpoint /api/embed no disponible, usando fallback secuencial")
            return super().embed_batch(texts)

    def dimension(self) -> int:
        return self._dimension
