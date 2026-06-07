import json
import numpy as np
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)


class VectorStore:
    def __init__(self, dimension: int, storage_dir: str):
        self.dimension = dimension
        self.storage_dir = Path(storage_dir)
        self.vectors = np.array([])
        self.texts = []
        self.metadata = []
        self._pending_vectors = []

    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

    def add(self, vector: list[float], text: str, metadata: dict):
        vec_array = np.array(vector)
        if vec_array.shape[0] != self.dimension:
            raise ValueError(
                f"Vector dimension mismatch: expected {self.dimension}, got {vec_array.shape[0]}"
            )
        normalized = self._normalize(vec_array)
        self._pending_vectors.append(normalized)
        self.texts.append(text)
        self.metadata.append(metadata)

    def _flush_pending(self):
        if self._pending_vectors:
            pending = np.array(self._pending_vectors)
            if self.vectors.size == 0:
                self.vectors = pending
            else:
                self.vectors = np.vstack([self.vectors, pending])
            self._pending_vectors = []

    def search(self, query_vector: list[float], top_k: int = 3, threshold: float = 0.7, 
               metadata_filter: dict | None = None) -> list[dict]:
        self._flush_pending()
        if self.vectors.size == 0:
            return []

        query = self._normalize(np.array(query_vector))

        similarities = np.dot(self.vectors, query)

        results = []
        for i, similarity in enumerate(similarities):
            if similarity >= threshold:
                if metadata_filter and not self._matches_filter(self.metadata[i], metadata_filter):
                    continue
                results.append({
                    "text": self.texts[i],
                    "metadata": self.metadata[i],
                    "similarity": float(similarity)
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def _matches_filter(self, metadata: dict, filter_dict: dict) -> bool:
        for key, value in filter_dict.items():
            if key not in metadata:
                return False
            if isinstance(value, list):
                if metadata[key] not in value:
                    return False
            else:
                if metadata[key] != value:
                    return False
        return True

    def save(self):
        self._flush_pending()
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        if self.vectors.size > 0:
            np.save(self.storage_dir / "vectors.npy", self.vectors)

        with open(self.storage_dir / "texts.json", 'w', encoding='utf-8') as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)

        with open(self.storage_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

        config = {
            "dimension": self.dimension,
            "num_vectors": len(self.texts)
        }
        with open(self.storage_dir / "config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

        logger.info(f"VectorStore saved: {len(self.texts)} vectors in {self.storage_dir}")

    def load(self):
        vectors_path = self.storage_dir / "vectors.npy"
        texts_path = self.storage_dir / "texts.json"
        metadata_path = self.storage_dir / "metadata.json"

        if vectors_path.exists():
            self.vectors = np.load(vectors_path)

        if texts_path.exists():
            with open(texts_path, 'r', encoding='utf-8') as f:
                self.texts = json.load(f)

        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)

        if self.vectors.size > 0 and self.vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Stored vector dimension ({self.vectors.shape[1]}) "
                f"does not match the current embedder ({self.dimension}). "
                f"Run 'python rag.py index' to re-index."
            )

        logger.info(f"VectorStore loaded: {len(self.texts)} vectors")

    def clear(self):
        self.vectors = np.array([])
        self.texts = []
        self.metadata = []
        self._pending_vectors = []
        logger.info("VectorStore cleared")
