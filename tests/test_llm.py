from __future__ import annotations

import json
import pytest

from prompt_ast.errors import ParseError
from prompt_ast.parse.llm import parse_prompt_llm


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
        "output_spec": {"format": "json", "structure": [], "language": None},
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


def test_parse_prompt_llm_accepts_clean_json():
    llm = DummyLLM(_llm_json({"role": "clean"}))
    ast = parse_prompt_llm("Input text", llm=llm)
    assert ast.role == "clean"
    assert ast.raw == "Input text"


def test_parse_prompt_llm_recovers_json_with_wrapped_text():
    wrapped = f"Here is JSON:\n{_llm_json({'role': 'wrapped'})}\nThanks."
    llm = DummyLLM(wrapped)
    ast = parse_prompt_llm("Input text", llm=llm)
    assert ast.role == "wrapped"


def test_parse_prompt_llm_sets_metadata_extracted_by_if_missing():
    raw = json.dumps(
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
        }
    )
    llm = DummyLLM(raw)
    ast = parse_prompt_llm("Input text", llm=llm)
    assert ast.metadata.get("extracted_by") == "llm"


def test_parse_prompt_llm_raises_on_invalid_json():
    llm = DummyLLM("not json at all")
    with pytest.raises(ParseError):
        parse_prompt_llm("Input text", llm=llm)


def test_parse_prompt_llm_raises_on_schema_validation_error():
    bad = _llm_json({"constraints": "not-a-list"})
    llm = DummyLLM(bad)
    with pytest.raises(ParseError):
        parse_prompt_llm("Input text", llm=llm)
