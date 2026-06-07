import pickle
import hashlib
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)


class EmbeddingCache:
    def __init__(self, cache_dir: str, model_name: str):
        self.cache_dir = Path(cache_dir)
        self.cache_file = self.cache_dir / "embedding_cache.pkl"
        self.model_name = model_name
        self.cache = {}
        self._load()

    def _hash(self, text: str) -> str:
        key_data = f"{self.model_name}:{text}"
        return hashlib.sha256(key_data.encode('utf-8')).hexdigest()

    def _load(self):
        if self.cache_file.exists():
            with open(self.cache_file, 'rb') as f:
                self.cache = pickle.load(f)
            logger.info(f"Embedding cache loaded: {len(self.cache)} entries")
        else:
            logger.info("Embedding cache is empty")

    def save(self):
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        with open(self.cache_file, 'wb') as f:
            pickle.dump(self.cache, f)
        logger.info(f"Embedding cache saved: {len(self.cache)} entries")

    def get(self, text: str) -> list[float] | None:
        key = self._hash(text)
        return self.cache.get(key)

    def set(self, text: str, embedding: list[float]):
        key = self._hash(text)
        self.cache[key] = embedding

    def clear(self):
        self.cache = {}
        logger.info("Embedding cache cleared")
