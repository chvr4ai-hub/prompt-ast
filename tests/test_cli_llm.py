from __future__ import annotations

import json
from typer.testing import CliRunner

from prompt_ast.cli import app
from prompt_ast.errors import LLMNotConfiguredError


runner = CliRunner()


class _FakeOpenAICompatClient:
    def complete(self, _prompt: str) -> str:
        return json.dumps(
            {
                "version": "0.1",
                "raw": "ignored",
                "role": None,
                "context": None,
                "task": "Do a thing",
                "constraints": [],
                "assumptions": [],
                "ambiguities": [],
                "output_spec": {"format": None, "structure": [], "language": None},
                "metadata": {"confidence": 0.7, "extracted_by": "llm"},
            }
        )


def test_cli_llm_mode_requires_use_openai():
    result = runner.invoke(app, ["normalize", "hello", "--mode", "llm"])
    assert result.exit_code == 1
    assert isinstance(result.exception, LLMNotConfiguredError)


def test_cli_llm_mode_with_use_openai(monkeypatch):
    import prompt_ast.llm.openai_compat as oc

    monkeypatch.setattr(oc, "OpenAICompatClient", _FakeOpenAICompatClient)
    result = runner.invoke(
        app, ["normalize", "hello", "--mode", "llm", "--use-openai"]
    )
    assert result.exit_code == 0
    assert "Prompt AST" in result.stdout


def test_cli_hybrid_mode_with_use_openai(monkeypatch):
    import prompt_ast.llm.openai_compat as oc

    monkeypatch.setattr(oc, "OpenAICompatClient", _FakeOpenAICompatClient)
    result = runner.invoke(
        app, ["normalize", "hello", "--mode", "hybrid", "--use-openai"]
    )
    assert result.exit_code == 0
