import requests


class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, system_prompt: str, context: str, query: str) -> str:
        prompt = f"{system_prompt}\n\nPregunta: {query}"

        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "system": system_prompt,
                "context": context,
                "stream": False
            }
        )
        response.raise_for_status()
        return response.json()["response"]
