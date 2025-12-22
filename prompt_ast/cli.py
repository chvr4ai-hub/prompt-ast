from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel

from . import parse_prompt
from .formats import serialize
from .errors import LLMNotConfiguredError

app = typer.Typer(add_completion=False)
console = Console()


@app.callback()
def main():
    """Prompt AST CLI."""


@app.command()
def normalize(
    text: str = typer.Argument(..., help="Raw prompt text"),
    mode: str = typer.Option("heuristic", help="heuristic|llm|hybrid"),
    fmt: str = typer.Option("json", "--format", help="json|yaml"),
    use_openai: bool = typer.Option(False, help="Use OpenAI-compatible API via env vars"),
):
    llm = None
    if mode in ("llm", "hybrid"):
        if not use_openai:
            raise LLMNotConfiguredError("Use --use-openai for llm/hybrid in CLI MVP.")
        from .llm.openai_compat import OpenAICompatClient  # lazy import (optional dep)

        llm = OpenAICompatClient()

    ast = parse_prompt(text, mode=mode, llm=llm)
    out = serialize(ast, fmt=fmt)  # returns str for json/yaml
    console.print(Panel.fit(out if isinstance(out, str) else str(out), title="Prompt AST"))


if __name__ == "__main__":
    app()
