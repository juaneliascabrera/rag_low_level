import json
import numpy as np
from pathlib import Path


class VectorStore:
    def __init__(self, dimension: int, storage_dir: str):
        self.dimension = dimension
        self.storage_dir = Path(storage_dir)
        self.vectors = []
        self.texts = []
        self.metadata = []

    def add(self, vector: list[float], text: str, metadata: dict):
        self.vectors.append(vector)
        self.texts.append(text)
        self.metadata.append(metadata)

    def search(self, query_vector: list[float], top_k: int = 3, threshold: float = 0.7) -> list[dict]:
        if not self.vectors:
            return []

        query = np.array(query_vector)
        vectors_array = np.array(self.vectors)

        similarities = np.dot(vectors_array, query) / (
            np.linalg.norm(vectors_array, axis=1) * np.linalg.norm(query)
        )

        results = []
        for i, similarity in enumerate(similarities):
            if similarity >= threshold:
                results.append({
                    "text": self.texts[i],
                    "metadata": self.metadata[i],
                    "similarity": float(similarity)
                })

        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]

    def save(self):
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        if self.vectors:
            np.save(self.storage_dir / "vectors.npy", np.array(self.vectors))

        with open(self.storage_dir / "texts.json", 'w', encoding='utf-8') as f:
            json.dump(self.texts, f, ensure_ascii=False, indent=2)

        with open(self.storage_dir / "metadata.json", 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)

        config = {
            "dimension": self.dimension,
            "num_vectors": len(self.vectors)
        }
        with open(self.storage_dir / "config.json", 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)

    def load(self):
        vectors_path = self.storage_dir / "vectors.npy"
        texts_path = self.storage_dir / "texts.json"
        metadata_path = self.storage_dir / "metadata.json"

        if vectors_path.exists():
            self.vectors = np.load(vectors_path).tolist()

        if texts_path.exists():
            with open(texts_path, 'r', encoding='utf-8') as f:
                self.texts = json.load(f)

        if metadata_path.exists():
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)

    def clear(self):
        self.vectors = []
        self.texts = []
        self.metadata = []
