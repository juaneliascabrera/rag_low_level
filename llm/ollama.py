import requests
import json
from logger import get_logger
from .base import LLMClient

logger = get_logger(__name__)


class OllamaClient(LLMClient):
    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def generate(self, system_prompt: str, query: str, silent: bool = False) -> str:
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
            logger.error(f"Could not connect to Ollama at {self.base_url}")
            raise RuntimeError(f"Ollama is not running at {self.base_url}")
        except requests.exceptions.Timeout:
            logger.error("Timeout while connecting to Ollama")
            raise RuntimeError("Timeout while connecting to Ollama (300s)")

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
                    self._print_thinking_header(silent)
                    thinking_started = True

                if thinking:
                    self._print_token(thinking, to_stderr=True, silent=silent)

                if content:
                    if thinking_started and not content_started:
                        self._print_response_header(silent)
                        content_started = True
                    self._print_token(content, silent=silent)
                    full_response += content

        self._print_newline(silent)
        return full_response
