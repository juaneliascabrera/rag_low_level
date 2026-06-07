import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from llm.ollama import OllamaClient
from llm.opencode import OpenCodeClient


class TestOllamaClient:
    def test_init(self):
        client = OllamaClient("http://localhost:11434", "test-model")
        assert client.base_url == "http://localhost:11434"
        assert client.model == "test-model"

    @patch('llm.ollama.requests.post')
    def test_generate_basic(self, mock_post):
        # Simulate streaming response with two chunks + done
        chunks = [
            json.dumps({"message": {"content": "Hello "}, "done": False}).encode(),
            json.dumps({"message": {"content": "world"}, "done": False}).encode(),
            json.dumps({"message": {"content": ""}, "done": True}).encode(),
        ]
        mock_response = Mock()
        mock_response.iter_lines.return_value = chunks
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = OllamaClient("http://localhost:11434", "test")
        result = client.generate("system", "query", silent=True)

        assert result == "Hello world"

    @patch('llm.ollama.requests.post')
    def test_generate_connection_error(self, mock_post):
        import requests
        mock_post.side_effect = requests.exceptions.ConnectionError()

        client = OllamaClient("http://localhost:11434", "test")
        with pytest.raises(RuntimeError, match="Ollama is not running"):
            client.generate("system", "query", silent=True)

    @patch('llm.ollama.requests.post')
    def test_generate_with_thinking(self, mock_post):
        chunks = [
            json.dumps({"message": {"thinking": "Let me think...", "content": ""}, "done": False}).encode(),
            json.dumps({"message": {"thinking": "", "content": "Answer"}, "done": False}).encode(),
            json.dumps({"message": {"content": ""}, "done": True}).encode(),
        ]
        mock_response = Mock()
        mock_response.iter_lines.return_value = chunks
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = OllamaClient("http://localhost:11434", "test")
        result = client.generate("system", "query", silent=True)

        assert result == "Answer"


class TestOpenCodeClient:
    def test_init_openai_model(self):
        client = OpenCodeClient("kimi-k2.6", "test-key")
        assert client.api_type == "openai"

    def test_init_anthropic_model(self):
        client = OpenCodeClient("claude-3-opus", "test-key")
        assert client.api_type == "anthropic"

    def test_init_explicit_api_type(self):
        client = OpenCodeClient("some-model", "test-key", api_type="openai")
        assert client.api_type == "openai"

    @patch('llm.opencode.requests.post')
    def test_generate_openai_format(self, mock_post):
        chunks = [
            b'data: ' + json.dumps({"choices": [{"delta": {"content": "Hello"}}]}).encode(),
            b'data: ' + json.dumps({"choices": [{"delta": {"content": " world"}}]}).encode(),
            b'data: [DONE]',
        ]
        mock_response = Mock()
        mock_response.iter_lines.return_value = chunks
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        client = OpenCodeClient("kimi-k2.6", "test-key")
        result = client.generate("system", "query", silent=True)

        assert result == "Hello world"

    @patch('llm.opencode.requests.post')
    def test_generate_auth_error(self, mock_post):
        import requests
        mock_resp = Mock()
        mock_resp.status_code = 401
        mock_resp.raise_for_status.side_effect = requests.exceptions.HTTPError(response=mock_resp)
        mock_post.return_value = mock_resp

        client = OpenCodeClient("kimi-k2.6", "test-key")
        with pytest.raises(RuntimeError, match="Invalid OpenCode API key"):
            client.generate("system", "query", silent=True)
