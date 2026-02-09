from __future__ import annotations

import json
import pytest

from prompt_ast import parse_prompt
from prompt_ast.errors import LLMNotConfiguredError


def _llm_json(overrides: dict | None = None) -> str:
    payload = {
        "version": "0.1",
        "raw": "ignored",
        "role": "tester",
        "context": None,
        "task": "Do a thing",
        "constraints": [],
        "assumptions": [],
        "ambiguities": [],
        "output_spec": {"format": None, "structure": [], "language": None},
        "metadata": {"confidence": 0.7, "extracted_by": "llm"},
    }
    if overrides:
        payload.update(overrides)
    return json.dumps(payload)


class DummyLLM:
    def __init__(self, response: str):
        self.response = response
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


def test_parse_prompt_heuristic_mode_does_not_require_llm():
    ast = parse_prompt("Act as a tester. Be concise.", mode="heuristic")
    assert ast.metadata.get("extracted_by") == "heuristic"


def test_parse_prompt_llm_requires_llm():
    with pytest.raises(LLMNotConfiguredError):
        parse_prompt("Hello", mode="llm")


def test_parse_prompt_hybrid_requires_llm():
    with pytest.raises(LLMNotConfiguredError):
        parse_prompt("Hello", mode="hybrid")


def test_parse_prompt_llm_mode_uses_llm():
    llm = DummyLLM(_llm_json({"role": "from-llm"}))
    ast = parse_prompt("Hello", mode="llm", llm=llm)
    assert ast.role == "from-llm"


def test_parse_prompt_unknown_mode_raises_value_error():
    llm = DummyLLM(_llm_json())
    with pytest.raises(ValueError):
        parse_prompt("Hello", mode="unknown", llm=llm)
