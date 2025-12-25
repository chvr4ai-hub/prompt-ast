from __future__ import annotations

import os
import httpx
from ..errors import LLMNotConfiguredError


class OpenAICompatClient:
    """
    Minimal OpenAI-compatible Chat Completions client.
    Works for OpenAI or compatible gateways (via OPENAI_BASE_URL).
    """

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str = "gpt-4o-mini",
        timeout: float = 30.0,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.base_url = base_url or os.getenv(
            "OPENAI_BASE_URL", "https://api.openai.com/v1"
        )
        self.model = model
        self.timeout = timeout

        if not self.api_key:
            raise LLMNotConfiguredError("OPENAI_API_KEY not set")

    def complete(self, prompt: str) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You output ONLY valid JSON. No prose."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.0,
        }

        with httpx.Client(timeout=self.timeout) as client:
            r = client.post(url, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
            return data["choices"][0]["message"]["content"]
