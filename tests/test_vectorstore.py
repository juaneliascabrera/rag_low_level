import pytest
import numpy as np
from vectorstore.store import VectorStore
import tempfile


class TestVectorStore:
    def test_add_and_search(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(dimension=3, storage_dir=tmpdir)
            
            store.add([1.0, 0.0, 0.0], "text1", {"source": "test1"})
            store.add([0.0, 1.0, 0.0], "text2", {"source": "test2"})
            
            results = store.search([1.0, 0.0, 0.0], top_k=2, threshold=0.5)
            
            assert len(results) >= 1
            assert results[0]["text"] == "text1"

    def test_metadata_filter(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(dimension=3, storage_dir=tmpdir)
            
            store.add([1.0, 0.0, 0.0], "text1", {"component": "GDT"})
            store.add([0.0, 1.0, 0.0], "text2", {"component": "IDT"})
            
            results = store.search([0.9, 0.1, 0.0], top_k=2, threshold=0.5, 
                                 metadata_filter={"component": "GDT"})
            
            assert all(r["metadata"]["component"] == "GDT" for r in results)

    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store1 = VectorStore(dimension=3, storage_dir=tmpdir)
            store1.add([1.0, 0.0, 0.0], "text1", {"source": "test"})
            store1.save()
            
            store2 = VectorStore(dimension=3, storage_dir=tmpdir)
            store2.load()
            
            assert len(store2.texts) == 1
            assert store2.texts[0] == "text1"

    def test_dimension_mismatch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store1 = VectorStore(dimension=3, storage_dir=tmpdir)
            store1.add([1.0, 0.0, 0.0], "text1", {})
            store1.save()
            
            store2 = VectorStore(dimension=5, storage_dir=tmpdir)
            
            with pytest.raises(ValueError, match="Dimensión"):
                store2.load()

    def test_normalization(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            store = VectorStore(dimension=3, storage_dir=tmpdir)
            
            store.add([2.0, 0.0, 0.0], "text1", {})
            
            norm = np.linalg.norm(store.vectors[0])
            assert abs(norm - 1.0) < 1e-6
