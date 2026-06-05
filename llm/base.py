from abc import ABC, abstractmethod
import sys


class LLMClient(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, query: str) -> str:
        pass

    def _print_thinking_header(self):
        print("\n[Thinking]", file=sys.stderr)

    def _print_response_header(self):
        print("\n\n[Respuesta]", file=sys.stderr)

    def _print_token(self, token: str, to_stderr: bool = False):
        if to_stderr:
            print(token, end="", file=sys.stderr, flush=True)
        else:
            print(token, end="", flush=True)

    def _print_newline(self):
        print()
