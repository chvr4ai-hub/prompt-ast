from __future__ import annotations

import json
import pytest

from prompt_ast.errors import ParseError
from prompt_ast.parse.hybrid import parse_prompt_hybrid


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


def test_parse_prompt_hybrid_uses_llm_refinement():
    llm = DummyLLM(_llm_json({"role": "refined"}))
    ast = parse_prompt_hybrid("Act as a tester. Be concise.", llm=llm)
    assert ast.role == "refined"
    assert llm.prompts, "LLM was not called"
    assert "ORIGINAL PROMPT" in llm.prompts[0]
    assert "CURRENT AST JSON" in llm.prompts[0]


def test_parse_prompt_hybrid_raises_on_invalid_json():
    llm = DummyLLM("{not json}")
    with pytest.raises(ParseError):
        parse_prompt_hybrid("Hello", llm=llm)
