import pytest
from reranker.reranker import Reranker


class TestReranker:
    def test_rerank_basic(self):
        reranker = Reranker()
        
        results = [
            {"text": "GDT is a table", "similarity": 0.8, "metadata": {}},
            {"text": "IDT handles interrupts", "similarity": 0.7, "metadata": {}},
            {"text": "GDT contains descriptors", "similarity": 0.9, "metadata": {}}
        ]
        
        reranked = reranker.rerank("What is GDT?", results, top_k=2)
        
        assert len(reranked) == 2
        assert all("rerank_score" in r for r in reranked)

    def test_rerank_empty(self):
        reranker = Reranker()
        results = reranker.rerank("query", [], top_k=3)
        assert results == []

    def test_rerank_ordering(self):
        reranker = Reranker()
        
        results = [
            {"text": "unrelated text", "similarity": 0.5, "metadata": {}},
            {"text": "GDT Global Descriptor Table structure", "similarity": 0.6, "metadata": {}}
        ]
        
        reranked = reranker.rerank("Explain GDT structure", results, top_k=2)
        
        assert reranked[0]["rerank_score"] >= reranked[1]["rerank_score"]
