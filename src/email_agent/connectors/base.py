"""Base classes for email connectors."""

from __future__ import annotations

import abc
from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List, Optional


@dataclass
class EmailMessage:
    """Representation of an email used by the agent."""

    id: str
    subject: str
    sender: str
    recipients: List[str]
    snippet: str
    received_at: datetime
    body: Optional[str] = None
    thread_id: Optional[str] = None
    raw_payload: Optional[dict] = None


class EmailConnector(abc.ABC):
    """Abstract base class for fetching emails from providers."""

    @abc.abstractmethod
    async def list_messages(self, *, limit: int = 20) -> Iterable[EmailMessage]:
        """Return the most recent email messages."""

    @abc.abstractmethod
    async def get_message(self, message_id: str) -> EmailMessage:
        """Return the full message identified by ``message_id``."""

    @abc.abstractmethod
    async def send_reply(self, *, thread_id: str, body: str) -> str:
        """Send a reply within the specified thread and return the new message ID."""


__all__ = ["EmailMessage", "EmailConnector"]
