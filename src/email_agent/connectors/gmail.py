"""Gmail connector implementation."""

from __future__ import annotations

import base64
from datetime import datetime
from typing import Iterable, List

from google.oauth2 import service_account
from googleapiclient.discovery import build

from .base import EmailConnector, EmailMessage


SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def _parse_rfc3339(value: str) -> datetime:
    return datetime.fromtimestamp(int(value) / 1000)


class GmailConnector(EmailConnector):
    """Connector that authenticates with a service account and delegated user."""

    def __init__(self, *, service_account_file: str, delegated_user: str) -> None:
        credentials = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=SCOPES
        )
        self._credentials = credentials.with_subject(delegated_user)
        self._service = build("gmail", "v1", credentials=self._credentials, cache_discovery=False)

    async def list_messages(self, *, limit: int = 20) -> Iterable[EmailMessage]:
        response = (
            self._service.users()
            .messages()
            .list(userId="me", maxResults=limit, labelIds=["INBOX"], q="is:unread")
            .execute()
        )
        message_ids = [item["id"] for item in response.get("messages", [])]
        for message_id in message_ids:
            yield await self.get_message(message_id)

    async def get_message(self, message_id: str) -> EmailMessage:
        message = (
            self._service.users()
            .messages()
            .get(userId="me", id=message_id, format="full")
            .execute()
        )
        payload = message.get("payload", {})
        headers = {header["name"].lower(): header["value"] for header in payload.get("headers", [])}
        parts = payload.get("parts", [])
        body = ""
        for part in parts:
            if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                body = base64.urlsafe_b64decode(part["body"]["data"].encode()).decode()
                break
        return EmailMessage(
            id=message["id"],
            subject=headers.get("subject", "(no subject)"),
            sender=headers.get("from", ""),
            recipients=headers.get("to", "").split(","),
            snippet=message.get("snippet", ""),
            received_at=_parse_rfc3339(message.get("internalDate", "0")),
            body=body,
            thread_id=message.get("threadId"),
            raw_payload=message,
        )

    async def send_reply(self, *, thread_id: str, body: str) -> str:
        message = (
            self._service.users()
            .messages()
            .send(
                userId="me",
                body={
                    "threadId": thread_id,
                    "raw": base64.urlsafe_b64encode(body.encode()).decode(),
                },
            )
            .execute()
        )
        return message["id"]


__all__ = ["GmailConnector"]
