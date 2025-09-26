import pytest

pydantic = pytest.importorskip("pydantic")
pytest.importorskip("pydantic_settings")

from email_agent.config import Settings


def test_settings_aliases(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    settings = Settings()
    assert settings.openai_api_key == "test-key"
    assert settings.openai_model == "gpt-test"
