from __future__ import annotations

from typing import Literal
from .ast import PromptAST

Format = Literal["json", "yaml", "dict"]


def serialize(ast: PromptAST, fmt: Format) -> str | dict:
    if fmt == "dict":
        return ast.to_dict()
    if fmt == "json":
        return ast.to_json()
    if fmt == "yaml":
        return ast.to_yaml()
    raise ValueError(f"Unsupported format: {fmt}")
