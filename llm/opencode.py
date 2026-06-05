import requests
import json
import sys


class OpenCodeClient:
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.base_url = "https://opencode.ai/zen/go/v1"

        openai_models = ["glm-5.1", "glm-5", "kimi-k2.5", "kimi-k2.6",
                        "deepseek-v4-pro", "deepseek-v4-flash",
                        "mimo-v2.5", "mimo-v2.5-pro"]

        self.api_type = "openai" if model in openai_models else "anthropic"

    def generate(self, system_prompt: str, context: str, query: str) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Contexto:\n{context}\n\nPregunta: {query}"}
        ]

        print(f"[Generando con OpenCode {self.model}...]", file=sys.stderr)

        if self.api_type == "openai":
            return self._generate_openai(messages)
        else:
            return self._generate_anthropic(messages)

    def _generate_openai(self, messages: list) -> str:
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

        full_response = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    if data_str == '[DONE]':
                        break
                    data = json.loads(data_str)
                    if data.get('choices') and data['choices'][0].get('delta', {}).get('content'):
                        token = data['choices'][0]['delta']['content']
                        print(token, end="", flush=True)
                        full_response += token

        print()
        return full_response

    def _generate_anthropic(self, messages: list) -> str:
        system_message = messages[0]["content"]
        user_message = messages[1]["content"]

        response = requests.post(
            f"{self.base_url}/messages",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            },
            json={
                "model": self.model,
                "max_tokens": 4096,
                "system": system_message,
                "messages": [{"role": "user", "content": user_message}],
                "stream": True
            },
            stream=True,
            timeout=300
        )
        response.raise_for_status()

        full_response = ""
        for line in response.iter_lines():
            if line:
                line_str = line.decode('utf-8')
                if line_str.startswith('data: '):
                    data_str = line_str[6:]
                    data = json.loads(data_str)

                    if data.get('type') == 'content_block_delta':
                        delta = data.get('delta', {})
                        if delta.get('type') == 'text_delta':
                            token = delta.get('text', '')
                            print(token, end="", flush=True)
                            full_response += token

        print()
        return full_response
