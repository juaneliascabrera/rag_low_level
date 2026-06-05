import pytest
from unittest.mock import Mock, patch
from reranker.reranker import Reranker


class TestReranker:
    @patch('reranker.reranker.CrossEncoder')
    def test_rerank_basic(self, mock_cross_encoder):
        mock_model = Mock()
        mock_model.predict.return_value = [0.9, 0.7, 0.95]
        mock_cross_encoder.return_value = mock_model
        
        reranker = Reranker()
        
        results = [
            {"text": "GDT is a table", "similarity": 0.8, "metadata": {}},
            {"text": "IDT handles interrupts", "similarity": 0.7, "metadata": {}},
            {"text": "GDT contains descriptors", "similarity": 0.9, "metadata": {}}
        ]
        
        reranked = reranker.rerank("What is GDT?", results, top_k=2)
        
        assert len(reranked) == 2
        assert all("rerank_score" in r for r in reranked)

    @patch('reranker.reranker.CrossEncoder')
    def test_rerank_empty(self, mock_cross_encoder):
        mock_model = Mock()
        mock_cross_encoder.return_value = mock_model
        
        reranker = Reranker()
        results = reranker.rerank("query", [], top_k=3)
        assert results == []

    @patch('reranker.reranker.CrossEncoder')
    def test_rerank_ordering(self, mock_cross_encoder):
        mock_model = Mock()
        mock_model.predict.return_value = [0.3, 0.9]
        mock_cross_encoder.return_value = mock_model
        
        reranker = Reranker()
        
        results = [
            {"text": "unrelated text", "similarity": 0.5, "metadata": {}},
            {"text": "GDT Global Descriptor Table structure", "similarity": 0.6, "metadata": {}}
        ]
        
        reranked = reranker.rerank("Explain GDT structure", results, top_k=2)
        
        assert reranked[0]["rerank_score"] >= reranked[1]["rerank_score"]
