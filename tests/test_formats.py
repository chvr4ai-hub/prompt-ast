from __future__ import annotations

import pytest

from prompt_ast.ast import PromptAST
from prompt_ast.formats import serialize


def test_serialize_dict():
    ast = PromptAST(raw="Hello", task="Say hello")
    out = serialize(ast, fmt="dict")
    assert isinstance(out, dict)
    assert out["task"] == "Say hello"


def test_serialize_json():
    ast = PromptAST(raw="Hello", task="Say hello")
    out = serialize(ast, fmt="json")
    assert isinstance(out, str)
    assert '"task": "Say hello"' in out


def test_serialize_yaml():
    ast = PromptAST(raw="Hello", task="Say hello")
    out = serialize(ast, fmt="yaml")
    assert isinstance(out, str)
    assert "task:" in out


def test_serialize_unsupported_format():
    ast = PromptAST(raw="Hello", task="Say hello")
    with pytest.raises(ValueError):
        serialize(ast, fmt="xml")  # type: ignore[arg-type]
