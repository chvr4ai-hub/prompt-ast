from __future__ import annotations

import json
from ..ast import PromptAST
from ..errors import ParseError
from ..llm.base import LLMClient


EXTRACTION_PROMPT = """Convert the user's prompt into Prompt AST JSON.

Return ONLY JSON matching this schema (keys may be null):
{
  "version": "0.1",
  "raw": "<original prompt>",
  "role": null|string,
  "context": null|string,
  "task": null|string,
  "constraints": [string],
  "assumptions": [string],
  "ambiguities": [string],
  "output_spec": { "format": null|string, "structure": [string], "language": null|string },
  "metadata": { "confidence": number between 0 and 1, "extracted_by": "llm" }
}

Rules:
- role: persona requested by user if present
- context: background information
- task: the primary ask
- constraints: formatting / tone / boundaries (e.g., "Be concise", "Use bullets")
- ambiguities: missing details you need to do the task well
- output_spec.format: json|yaml|markdown|table|text if implied
"""


def parse_prompt_llm(text: str, llm: LLMClient) -> PromptAST:
    prompt = f"{EXTRACTION_PROMPT}\n\nUSER PROMPT:\n{text.strip()}"
    raw = llm.complete(prompt)

    obj = _safe_json_load(raw)
    obj["raw"] = text.strip()
    obj["version"] = "0.1"
    obj.setdefault("metadata", {})
    obj["metadata"].setdefault("extracted_by", "llm")

    try:
        return PromptAST.model_validate(obj)
    except Exception as e:
        raise ParseError(f"LLM output failed schema validation: {e}") from e


def _safe_json_load(s: str) -> dict:
    try:
        return json.loads(s)
    except Exception:
        start = s.find("{")
        end = s.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(s[start : end + 1])
            except Exception as e:
                raise ParseError(f"Could not parse JSON from LLM output: {e}") from e
        raise ParseError("Could not find JSON object in LLM output.")
