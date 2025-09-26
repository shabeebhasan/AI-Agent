"""Configuration management for the AI email agent."""

from __future__ import annotations

from functools import lru_cache
from typing import List, Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central configuration object loaded from environment variables."""

    openai_api_key: str = Field(..., alias="OPENAI_API_KEY", description="API key for OpenAI models.")
    openai_model: str = Field("gpt-4o", alias="OPENAI_MODEL", description="LLM model to use for the agent.")

    gmail_service_account_file: Optional[str] = Field(
        None,
        alias="GMAIL_SERVICE_ACCOUNT_FILE",
        description="Path to a Google service account JSON file with Gmail API scopes.",
    )
    gmail_delegated_user: Optional[str] = Field(
        None,
        alias="GMAIL_DELEGATED_USER",
        description="Email address to impersonate when using a service account.",
    )

    outlook_client_id: Optional[str] = Field(None, alias="OUTLOOK_CLIENT_ID")
    outlook_client_secret: Optional[str] = Field(None, alias="OUTLOOK_CLIENT_SECRET")
    outlook_tenant_id: Optional[str] = Field(None, alias="OUTLOOK_TENANT_ID")
    outlook_user_id: Optional[str] = Field(None, alias="OUTLOOK_USER_ID", description="User ID or email for Microsoft Graph.")

    allowed_senders: List[str] = Field(
        default_factory=list,
        alias="ALLOWED_SENDERS",
        description="Optional comma-separated list of email addresses the agent is allowed to respond to.",
    )

    redis_url: Optional[str] = Field(
        None,
        alias="REDIS_URL",
        description="Optional Redis URL for storing conversation state when running multiple replicas.",
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        populate_by_name = True


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings loaded from the environment."""

    return Settings()


__all__ = ["Settings", "get_settings"]
