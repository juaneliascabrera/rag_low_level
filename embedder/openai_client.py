import requests
from .base import Embedder


class OpenAIEmbedder(Embedder):
    def __init__(self, api_key: str, model_name: str = "text-embedding-3-small"):
        self.api_key = api_key
        self.model_name = model_name
        self._dimension = 1536 if "small" in model_name else 3072

    def embed(self, text: str) -> list[float]:
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "input": text,
                "model": self.model_name
            }
        )
        response.raise_for_status()
        return response.json()["data"][0]["embedding"]

    def dimension(self) -> int:
        return self._dimension
