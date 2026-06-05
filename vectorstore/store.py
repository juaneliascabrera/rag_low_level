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

    def _normalize(self, vector: np.ndarray) -> np.ndarray:
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

    def add(self, vector: list[float], text: str, metadata: dict):
        normalized = self._normalize(np.array(vector))
        if self.vectors.size == 0:
            self.vectors = np.array([normalized])
        else:
            self.vectors = np.vstack([self.vectors, normalized])
        self.texts.append(text)
        self.metadata.append(metadata)

    def search(self, query_vector: list[float], top_k: int = 3, threshold: float = 0.7, 
               metadata_filter: dict | None = None) -> list[dict]:
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

        logger.info(f"VectorStore guardado: {len(self.texts)} vectores en {self.storage_dir}")

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
                f"Dimensión de vectores almacenados ({self.vectors.shape[1]}) "
                f"no coincide con el embedder actual ({self.dimension}). "
                f"Ejecutá 'python rag.py index' para re-indexar."
            )

        logger.info(f"VectorStore cargado: {len(self.texts)} vectores")

    def clear(self):
        self.vectors = np.array([])
        self.texts = []
        self.metadata = []
        logger.info("VectorStore limpiado")
