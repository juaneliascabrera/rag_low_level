import requests
import json
from logger import get_logger
from .base import LLMClient

logger = get_logger(__name__)


class OpenCodeClient(LLMClient):
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://opencode.ai/zen/go/v1"

        openai_models = ["glm-5.1", "glm-5", "kimi-k2.5", "kimi-k2.6",
                        "deepseek-v4-pro", "deepseek-v4-flash",
                        "mimo-v2.5", "mimo-v2.5-pro"]

        self.api_type = "openai" if model in openai_models else "anthropic"

    def generate(self, system_prompt: str, query: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]

        logger.info(f"Generando con OpenCode {self.model}...")

        if self.api_type == "openai":
            return self._generate_openai(messages)
        else:
            return self._generate_anthropic(messages)

    def _generate_openai(self, messages: list) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": True
                },
                stream=True,
                timeout=300
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                logger.error("API key inválida para OpenCode")
                raise RuntimeError("API key inválida para OpenCode")
            raise

        full_response = ""
        thinking_started = False
        content_started = False

        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        break
                    data = json.loads(data_str)
                    if data.get('choices'):
                        delta = data['choices'][0].get('delta', {})

                        thinking = delta.get('reasoning_content', '')
                        if thinking:
                            if not thinking_started:
                                self._print_thinking_header()
                                thinking_started = True
                            self._print_token(thinking, to_stderr=True)

                        content = delta.get('content', '')
                        if content:
                            if thinking_started and not content_started:
                                self._print_response_header()
                                content_started = True
                            self._print_token(content)
                            full_response += content

        self._print_newline()
        return full_response

    def _generate_anthropic(self, messages: list) -> str:
        system_message = messages[0]["content"]
        user_message = messages[1]["content"]

        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01"
                },
                json={
                    "model": self.model,
                    "max_tokens": 16384,
                    "system": system_message,
                    "messages": [{"role": "user", "content": user_message}],
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
                logger.error("API key inválida para OpenCode")
                raise RuntimeError("API key inválida para OpenCode")
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
                            self._print_thinking_header()
                            thinking_started = True

                    elif data.get('type') == 'content_block_delta':
                        delta = data.get('delta', {})

                        if delta.get('type') == 'thinking_delta':
                            thinking = delta.get('thinking', '')
                            if thinking:
                                self._print_token(thinking, to_stderr=True)

                        elif delta.get('type') == 'text_delta':
                            token = delta.get('text', '')
                            if token:
                                if thinking_started and not content_started:
                                    self._print_response_header()
                                    content_started = True
                                self._print_token(token)
                                full_response += token

        self._print_newline()
        return full_response
