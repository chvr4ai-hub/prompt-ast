from __future__ import annotations

from typing import Literal

from .ast import PromptAST
from .errors import LLMNotConfiguredError
from .parse import parse_prompt_heuristic, parse_prompt_hybrid, parse_prompt_llm

Mode = Literal["heuristic", "llm", "hybrid"]


def parse_prompt(text: str, mode: Mode = "hybrid", llm=None) -> PromptAST:
    text = text.strip()

    if mode == "heuristic":
        return parse_prompt_heuristic(text)

    if llm is None:
        raise LLMNotConfiguredError("LLM client required for mode='llm' or 'hybrid'.")

    if mode == "llm":
        return parse_prompt_llm(text, llm=llm)

    if mode == "hybrid":
        return parse_prompt_hybrid(text, llm=llm)

    raise ValueError(f"Unknown mode: {mode}")


__all__ = ["PromptAST", "parse_prompt", "LLMNotConfiguredError"]
