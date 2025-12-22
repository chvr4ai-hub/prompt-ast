from __future__ import annotations

from ..ast import PromptAST
from ..llm.base import LLMClient
from .heuristic import parse_prompt_heuristic
from .llm import parse_prompt_llm


REFINE_PROMPT = """Refine the given Prompt AST based on the original prompt.
Return ONLY JSON matching the same schema.

Guidance:
- Keep correct fields.
- Fill missing fields.
- Move output formatting requirements into constraints and output_spec.
- Add ambiguities when key details are missing.

ORIGINAL PROMPT:
{raw}

CURRENT AST JSON:
{ast_json}
"""


def parse_prompt_hybrid(text: str, llm: LLMClient) -> PromptAST:
    base = parse_prompt_heuristic(text)

    # Ask LLM to refine the existing AST
    prompt = REFINE_PROMPT.format(raw=text.strip(), ast_json=base.to_json())
    refined_text = llm.complete(prompt)

    # parse refined result using same loader/validator
    # by reusing parse_prompt_llm-style validation
    return parse_prompt_llm(text, llm=_OverrideClient(refined_text))


class _OverrideClient:
    """Tiny adapter so we can reuse parse_prompt_llm validation path."""

    def __init__(self, fixed_response: str):
        self.fixed_response = fixed_response

    def complete(self, _prompt: str) -> str:
        return self.fixed_response
