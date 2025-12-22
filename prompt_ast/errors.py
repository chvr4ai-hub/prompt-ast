class PromptAstError(Exception):
    """Base error."""


class LLMNotConfiguredError(PromptAstError):
    """Raised when LLM mode is requested but no LLM client is configured."""


class ParseError(PromptAstError):
    """Raised when parsing fails (e.g., LLM output not valid JSON)."""
