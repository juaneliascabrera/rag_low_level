from abc import ABC, abstractmethod
import sys


class LLMClient(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, query: str, silent: bool = False) -> str:
        pass

    def _print_thinking_header(self, silent: bool = False):
        if not silent:
            print("\n[Thinking]", file=sys.stderr)

    def _print_response_header(self, silent: bool = False):
        if not silent:
            print("\n\n[Respuesta]", file=sys.stderr)

    def _print_token(self, token: str, to_stderr: bool = False, silent: bool = False):
        if silent:
            return
        if to_stderr:
            print(token, end="", file=sys.stderr, flush=True)
        else:
            print(token, end="", flush=True)

    def _print_newline(self, silent: bool = False):
        if not silent:
            print()
