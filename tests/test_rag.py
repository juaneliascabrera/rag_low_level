import pytest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile
import os


class TestRAGSystem:
    """Tests for the RAG pipeline orchestration."""

    @patch('rag.Reranker')
    @patch('rag.EmbeddingCache')
    @patch('rag.VectorStore')
    @patch('rag.MarkdownChunker')
    @patch('rag.OllamaEmbedder')
    @patch('rag.OllamaClient')
    @patch('rag.setup_logging')
    def _create_rag(self, mock_setup, mock_llm_cls, mock_emb_cls,
                    mock_chunker_cls, mock_store_cls, mock_cache_cls,
                    mock_reranker_cls):
        """Helper to create a RAGSystem with all dependencies mocked."""
        mock_embedder = Mock()
        mock_embedder.dimension.return_value = 768
        mock_emb_cls.return_value = mock_embedder

        mock_store = Mock()
        mock_store.vectors = np.array([[1.0] * 768])
        mock_store.texts = ["test text"]
        mock_store_cls.return_value = mock_store

        mock_cache = Mock()
        mock_cache_cls.return_value = mock_cache

        mock_llm = Mock()
        mock_llm.generate.return_value = "Test response"
        mock_llm_cls.return_value = mock_llm

        mock_chunker = Mock()
        mock_chunker_cls.return_value = mock_chunker

        mock_reranker = Mock()
        mock_reranker_cls.return_value = mock_reranker

        import rag
        system = rag.RAGSystem()
        return system, {
            'embedder': mock_embedder,
            'store': mock_store,
            'cache': mock_cache,
            'llm': mock_llm,
            'chunker': mock_chunker,
            'reranker': mock_reranker,
        }

    @patch('rag.config')
    def test_query_returns_response(self, mock_config):
        mock_config.RERANK_ENABLED = False
        mock_config.HYDE_ENABLED = False
        mock_config.LLM_PROVIDER = 'ollama'
        mock_config.OLLAMA_BASE_URL = 'http://localhost:11434'
        mock_config.OLLAMA_MODEL = 'test'
        mock_config.EMBEDDING_PROVIDER = 'ollama'
        mock_config.EMBEDDING_MODEL = 'test'
        mock_config.STORAGE_DIR = '/tmp/test_storage'
        mock_config.CACHE_DIR = '/tmp/test_cache'
        mock_config.TOP_K = 5
        mock_config.SIMILARITY_THRESHOLD = 0.3
        mock_config.RERANK_TOP_K = 3
        mock_config.CONTEXT_TOKEN_BUDGET = 3000
        mock_config.CHARS_PER_TOKEN = 4
        mock_config.DEBUG_SHOW_CONTEXT = False
        mock_config.SYSTEM_PROMPT = "Context: {context}"

        system, mocks = self._create_rag()

        mocks['embedder'].embed.return_value = [0.1] * 768
        mocks['store'].search.return_value = [
            {"text": "GDT is a table", "metadata": {"source": "test.md"}, "similarity": 0.9}
        ]
        mocks['llm'].generate.return_value = "The GDT is..."

        result = system.query("What is GDT?")

        assert isinstance(result, str)
        assert len(result) > 0
        mocks['embedder'].embed.assert_called_once()
        mocks['store'].search.assert_called_once()
        mocks['llm'].generate.assert_called_once()

    def test_deduplicate_exact_duplicates(self):
        import rag
        system = Mock(spec=rag.RAGSystem)
        results = [
            {"text": "same text", "similarity": 0.9},
            {"text": "same text", "similarity": 0.8},
            {"text": "different text", "similarity": 0.7},
        ]
        deduped = rag.RAGSystem._deduplicate_fragments(system, results)
        assert len(deduped) == 2

    def test_deduplicate_no_duplicates(self):
        import rag
        system = Mock(spec=rag.RAGSystem)
        results = [
            {"text": "text a", "similarity": 0.9},
            {"text": "text b", "similarity": 0.8},
        ]
        deduped = rag.RAGSystem._deduplicate_fragments(system, results)
        assert len(deduped) == 2

    def test_deduplicate_empty(self):
        import rag
        system = Mock(spec=rag.RAGSystem)
        deduped = rag.RAGSystem._deduplicate_fragments(system, [])
        assert deduped == []
