from __future__ import annotations

import pytest

from prompt_ast.errors import LLMNotConfiguredError
from prompt_ast.llm.openai_compat import OpenAICompatClient


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload
        self.raise_called = False

    def raise_for_status(self) -> None:
        self.raise_called = True

    def json(self) -> dict:
        return self._payload


class _FakeHttpxClient:
    last_instance = None

    def __init__(self, timeout: float | None = None):
        self.timeout = timeout
        self.post_args: tuple | None = None
        self.response = _FakeResponse(
            {"choices": [{"message": {"content": "ok"}}]}
        )
        _FakeHttpxClient.last_instance = self

    def post(self, url: str, headers: dict | None = None, json: dict | None = None):
        self.post_args = (url, headers, json)
        return self.response

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_openai_client_requires_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(LLMNotConfiguredError):
        OpenAICompatClient()


def test_openai_client_env_defaults(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com/v1")
    client = OpenAICompatClient()
    assert client.api_key == "test-key"
    assert client.base_url == "https://example.com/v1"


def test_openai_client_complete_makes_request(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://example.com/v1")
    import prompt_ast.llm.openai_compat as oc

    monkeypatch.setattr(oc.httpx, "Client", _FakeHttpxClient)

    client = OpenAICompatClient(model="gpt-test", timeout=12.3)
    result = client.complete("Hello")

    assert result == "ok"

    fake_client = _FakeHttpxClient.last_instance
    assert fake_client is not None
    url, headers, payload = fake_client.post_args
    assert url == "https://example.com/v1/chat/completions"
    assert headers == {"Authorization": "Bearer test-key"}
    assert payload["model"] == "gpt-test"
    assert payload["temperature"] == 0.0
    assert payload["messages"][0]["role"] == "system"
    assert payload["messages"][1]["content"] == "Hello"
    assert fake_client.response.raise_called is True
