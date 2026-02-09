import builtins
import pytest

from prompt_ast.ast import PromptAST


def test_ast_json_serialization():
    ast = PromptAST(raw="Hello", task="Say hello")
    j = ast.to_json()
    assert '"task": "Say hello"' in j


def test_ast_yaml_serialization():
    ast = PromptAST(raw="Hello", task="Say hello")
    y = ast.to_yaml()
    assert "task:" in y


def test_ast_yaml_missing_dependency_raises(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ImportError("no yaml")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(ImportError) as excinfo:
        PromptAST(raw="Hello").to_yaml()
    assert "Install YAML support" in str(excinfo.value)
