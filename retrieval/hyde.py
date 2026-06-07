from __future__ import annotations
from typing import TYPE_CHECKING
from logger import get_logger

if TYPE_CHECKING:
    from llm.base import LLMClient

logger = get_logger(__name__)


class HyDETransformer:
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def transform(self, query: str) -> str:
        prompt = """Generate a hypothetical technical document that answers this question about Intel x86 32-bit architecture in Protected Mode. The document must be accurate and technical, as if it were extracted from an Intel manual.

Question: {query}

Technical document:"""

        system_prompt = "You are an expert in x86 32-bit architecture. Generate accurate and concise technical documentation."

        hypothetical_doc = self.llm.generate(system_prompt, prompt.format(query=query), silent=True)
        logger.info(f"HyDE: Query transformed into hypothetical document ({len(hypothetical_doc)} chars)")
        return hypothetical_doc
