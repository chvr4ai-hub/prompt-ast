from __future__ import annotations
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from pathlib import Path

from . import Mode, parse_prompt
from .formats import Format, serialize
from .errors import LLMNotConfiguredError

app = typer.Typer(add_completion=False)
console = Console()


@app.callback()
def main():
    """Prompt AST CLI."""


@app.command()
def normalize(
    text: Optional[str] = typer.Argument(
        None, help="Raw prompt text (optional if using --file)"
    ),
    file: Optional[Path] = typer.Option(
        None,
        "--file",
        "-f",
        help="Read prompt from file (alternative to text argument)",
    ),
    mode: Mode = typer.Option("heuristic", help="heuristic|llm|hybrid"),
    fmt: Format = typer.Option("json", "--format", help="json|yaml"),
    use_openai: bool = typer.Option(
        False, help="Use OpenAI-compatible API via env vars"
    ),
):
    """
    Normalize and parse prompt text into an AST.

    Provide prompt either as text argument or via --file option.
    """

    if file and text:
        console.print(
            "[red]Error: Cannot specify both text argument and --file option[/red]"
        )
        raise typer.Exit(1)

    prompt_text: str
    if file:
        if not file.exists():
            console.print(f"[red]Error: File '{file}' does not exist[/red]")
            raise typer.Exit(1)

        try:
            prompt_text = file.read_text(encoding="utf-8")
        except Exception as e:
            console.print(f"[red]Error reading file: {e}[/red]")
            raise typer.Exit(1)
    elif text:
        prompt_text = text
    else:
        console.print(
            "[red]Error: Must provide either text argument or --file option[/red]"
        )
        raise typer.Exit(1)

    llm = None
    if mode in ("llm", "hybrid"):
        if not use_openai:
            raise LLMNotConfiguredError("Use --use-openai for llm/hybrid in CLI MVP.")
        from .llm.openai_compat import OpenAICompatClient  # lazy import (optional dep)

        llm = OpenAICompatClient()

    ast = parse_prompt(prompt_text, mode=mode, llm=llm)
    out = serialize(ast, fmt=fmt)  # returns str for json/yaml
    console.print(
        Panel.fit(out if isinstance(out, str) else str(out), title="Prompt AST")
    )


if __name__ == "__main__":
    app()
