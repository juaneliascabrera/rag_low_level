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
            {"role": "user", "content": query}
        ]

        print(f"[Generando con {self.model}...]", file=sys.stderr)

        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "stream": True,
                "think": True
            },
            stream=True,
            timeout=300
        )
        response.raise_for_status()

        full_response = ""
        thinking_started = False
        content_started = False

        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if data.get("done", False):
                    break

                thinking = data["message"].get("thinking", "")
                content = data["message"].get("content", "")

                if thinking and not thinking_started:
                    print("\n[Thinking]", file=sys.stderr)
                    thinking_started = True

                if thinking:
                    print(thinking, end="", file=sys.stderr, flush=True)

                if content:
                    if thinking_started and not content_started:
                        print("\n\n[Respuesta]", file=sys.stderr)
                        content_started = True
                    print(content, end="", flush=True)
                    full_response += content

        print()
        return full_response
