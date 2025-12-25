from __future__ import annotations

from typing import Any, Literal
from pydantic import BaseModel, Field


SchemaVersion = Literal["0.1"]


class OutputSpec(BaseModel):
    """How the user expects the output to look (format + optional structure)."""

    format: str | None = None  # json|yaml|markdown|table|text
    structure: list[str] = Field(default_factory=list)  # e.g. ["Summary", "Steps"]
    language: str | None = None  # e.g. "English"


class PromptAST(BaseModel):
    """
    Prompt AST = an abstract, structured representation of a human prompt.

    Philosophy:
    - keep it minimal
    - keep it extensible
    - keep it safe (no persistence)
    """

    version: SchemaVersion = "0.1"
    raw: str

    role: str | None = None
    context: str | None = None
    task: str | None = None

    constraints: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    ambiguities: list[str] = Field(default_factory=list)

    output_spec: OutputSpec = Field(default_factory=OutputSpec)

    # Free-form room for integrations (confidence, extracted_by, tags, etc.)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="python")

    def to_json(self, **kwargs: Any) -> str:
        return self.model_dump_json(indent=2, **kwargs)

    def to_yaml(self) -> str:
        try:
            import yaml  # type: ignore
        except ImportError as e:
            raise ImportError(
                "Install YAML support: pip install prompt-ast[yaml]"
            ) from e
        return yaml.safe_dump(self.to_dict(), sort_keys=False, allow_unicode=True)
