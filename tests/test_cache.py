import pytest
from embedder.cache import EmbeddingCache
import tempfile
import os


class TestEmbeddingCache:
    def test_cache_set_and_get(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir, "test-model")
            text = "test text"
            embedding = [0.1, 0.2, 0.3]
            
            cache.set(text, embedding)
            result = cache.get(text)
            
            assert result == embedding

    def test_cache_miss(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir, "test-model")
            result = cache.get("nonexistent")
            
            assert result is None

    def test_cache_persistence(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache1 = EmbeddingCache(tmpdir, "test-model")
            text = "test text"
            embedding = [0.1, 0.2, 0.3]
            
            cache1.set(text, embedding)
            cache1.save()
            
            cache2 = EmbeddingCache(tmpdir, "test-model")
            result = cache2.get(text)
            
            assert result == embedding

    def test_cache_clear(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = EmbeddingCache(tmpdir, "test-model")
            cache.set("text1", [0.1])
            cache.set("text2", [0.2])
            
            cache.clear()
            
            assert cache.get("text1") is None
            assert cache.get("text2") is None
