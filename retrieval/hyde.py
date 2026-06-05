from logger import get_logger

logger = get_logger(__name__)


class HyDETransformer:
    def __init__(self, llm_client):
        self.llm = llm_client

    def transform(self, query: str) -> str:
        prompt = """Generá un documento técnico hipotético que responda esta pregunta sobre arquitectura x86 de 32 bits en Modo Protegido. El documento debe ser preciso y técnico, como si fuera extraído de un manual de Intel.

Pregunta: {query}

Documento técnico:"""

        system_prompt = "Sos un experto en arquitectura x86 de 32 bits. Generá documentación técnica precisa y concisa."

        hypothetical_doc = self.llm.generate(system_prompt, prompt.format(query=query))
        logger.info(f"HyDE: Query transformada en documento hipotético ({len(hypothetical_doc)} chars)")
        return hypothetical_doc
