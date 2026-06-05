from sentence_transformers import CrossEncoder
from logger import get_logger

logger = get_logger(__name__)


class Reranker:
    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        logger.info(f"Loading re-ranking model: {model_name}")
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, results: list[dict], top_k: int = 3) -> list[dict]:
        if not results:
            return results

        pairs = [(query, result["text"]) for result in results]
        scores = self.model.predict(pairs)

        for result, score in zip(results, scores):
            result["rerank_score"] = float(score)

        results.sort(key=lambda x: x["rerank_score"], reverse=True)
        return results[:top_k]
