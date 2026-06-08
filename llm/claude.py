import requests
import json
from logger import get_logger
from .base import LLMClient

logger = get_logger(__name__)


class ClaudeClient(LLMClient):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"

    def generate(self, system_prompt: str, query: str, silent: bool = False) -> str:
        logger.info(f"Generating with Claude {self.model}...")

        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                    "anthropic-beta": "prompt-caching-2024-07-31"
                },
                json={
                    "model": self.model,
                    "max_tokens": 16384,
                    "system": system_prompt,
                    "messages": [{"role": "user", "content": query}],
                    "stream": True,
                    "thinking": {
                        "type": "enabled",
                        "budget_tokens": 10000
                    }
                },
                stream=True,
                timeout=300
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("Invalid Anthropic API key")
                raise RuntimeError("Invalid Anthropic API key")
            raise

        full_response = ""
        thinking_started = False
        content_started = False

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    data = json.loads(data_str)

                    if data.get('type') == 'content_block_start':
                        block = data.get('content_block', {})
                        if block.get('type') == 'thinking':
                            self._print_thinking_header(silent)
                            thinking_started = True

                    elif data.get('type') == 'content_block_delta':
                        delta = data.get('delta', {})

                        if delta.get('type') == 'thinking_delta':
                            thinking = delta.get('thinking', '')
                            if thinking:
                                self._print_token(thinking, to_stderr=True, silent=silent)

                        elif delta.get('type') == 'text_delta':
                            token = delta.get('text', '')
                            if token:
                                if thinking_started and not content_started:
                                    self._print_response_header(silent)
                                    content_started = True
                                self._print_token(token, silent=silent)
                                full_response += token

        self._print_newline(silent)
        return full_response
