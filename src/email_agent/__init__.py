"""AI Email Orchestration Agent package."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from .agent import build_agent_executor
    from .workflows import app


def __getattr__(name: str) -> Any:
    if name == "build_agent_executor":
        return import_module("email_agent.agent").build_agent_executor
    if name == "app":
        return import_module("email_agent.workflows").app
    raise AttributeError(name)


__all__ = ["build_agent_executor", "app"]
