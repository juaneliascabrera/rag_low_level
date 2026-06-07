import requests
from logger import get_logger
from .base import Embedder

logger = get_logger(__name__)

MODEL_DIMENSIONS = {
    "text-embedding-3-small": 1536,
    "text-embedding-3-large": 3072,
    "text-embedding-ada-002": 1536,
}


class OpenAIEmbedder(Embedder):
    def __init__(self, api_key: str, model_name: str = "text-embedding-3-small",
                 base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model_name = model_name
        self.base_url = base_url
        self._dimension = MODEL_DIMENSIONS.get(model_name, 1536)
        logger.info(f"Initializing OpenAIEmbedder: {model_name} (dimension: {self._dimension})")

    def embed(self, text: str) -> list[float]:
        try:
            response = requests.post(
                f"{self.base_url}/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": text,
                    "model": self.model_name
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["data"][0]["embedding"]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Invalid OpenAI API key")
                raise RuntimeError("Invalid OpenAI API key")
            raise
        except requests.exceptions.Timeout:
            logger.error("Timeout while generating embedding with OpenAI")
            raise RuntimeError("Timeout while generating embedding with OpenAI")

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        logger.info(f"Generating {len(texts)} embeddings with OpenAI (batch)")
        try:
            response = requests.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "input": texts,
                    "model": self.model_name
                },
                timeout=120
            )
            response.raise_for_status()
            data = response.json()["data"]
            return [item["embedding"] for item in sorted(data, key=lambda x: x["index"])]
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Invalid OpenAI API key")
                raise RuntimeError("Invalid OpenAI API key")
            raise

    def dimension(self) -> int:
        return self._dimension
