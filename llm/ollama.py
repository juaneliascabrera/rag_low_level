import requests
import json
import sys


class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, system_prompt: str, context: str, query: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {query}"}
        ]

        print(f"[Generando con {self.model}...]", file=sys.stderr)

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": True
            },
            stream=True,
            timeout=300
        )
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if data.get("done", False):
                    break
                token = data["message"]["content"]
                print(token, end="", flush=True)
                full_response += token
        print()
        return full_response
