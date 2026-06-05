import requests
import json
from logger import get_logger
from .base import LLMClient

logger = get_logger(__name__)


class OllamaClient(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, system_prompt: str, query: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        logger.info(f"Generando con {self.model}...")

        try:
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
        except requests.exceptions.ConnectionError:
            logger.error(f"No se pudo conectar a Ollama en {self.base_url}")
            raise RuntimeError(f"Ollama no está corriendo en {self.base_url}")
        except requests.exceptions.Timeout:
            logger.error("Timeout al conectar con Ollama")
            raise RuntimeError("Timeout al conectar con Ollama (300s)")

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
                    self._print_thinking_header()
                    thinking_started = True

                if thinking:
                    self._print_token(thinking, to_stderr=True)

                if content:
                    if thinking_started and not content_started:
                        self._print_response_header()
                        content_started = True
                    self._print_token(content)
                    full_response += content

        self._print_newline()
        return full_response
