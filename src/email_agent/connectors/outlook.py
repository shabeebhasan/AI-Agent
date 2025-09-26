"""Outlook connector implementation using Microsoft Graph."""

from __future__ import annotations

from datetime import datetime
from typing import Iterable

import httpx
from msal import ConfidentialClientApplication

from .base import EmailConnector, EmailMessage


class OutlookConnector(EmailConnector):
    """Connector using OAuth client credentials to access Microsoft Graph."""

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        user_id: str,
        scope: str = "https://graph.microsoft.com/.default",
    ) -> None:
        self._user_id = user_id
        self._app = ConfidentialClientApplication(
            client_id, authority=f"https://login.microsoftonline.com/{tenant_id}", client_credential=client_secret
        )
        self._scope = [scope]
        self._client = httpx.AsyncClient(base_url="https://graph.microsoft.com/v1.0")

    async def _get_token(self) -> str:
        result = self._app.acquire_token_silent(self._scope, account=None)
        if not result:
            result = self._app.acquire_token_for_client(scopes=self._scope)
        if "access_token" not in result:
            raise RuntimeError(f"Failed to acquire token: {result.get('error_description', 'unknown error')}")
        return result["access_token"]

    async def list_messages(self, *, limit: int = 20) -> Iterable[EmailMessage]:
        token = await self._get_token()
        response = await self._client.get(
            f"/users/{self._user_id}/messages",
            params={"$top": limit, "$orderby": "receivedDateTime desc", "$filter": "isRead eq false"},
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        for item in response.json().get("value", []):
            yield self._parse_message(item)

    async def get_message(self, message_id: str) -> EmailMessage:
        token = await self._get_token()
        response = await self._client.get(
            f"/users/{self._user_id}/messages/{message_id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return self._parse_message(response.json())

    async def send_reply(self, *, thread_id: str, body: str) -> str:
        token = await self._get_token()
        response = await self._client.post(
            f"/users/{self._user_id}/messages/{thread_id}/createReply",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        draft_id = response.json()["id"]
        send_response = await self._client.post(
            f"/users/{self._user_id}/messages/{draft_id}/send",
            headers={"Authorization": f"Bearer {token}"},
            json={"body": {"contentType": "Text", "content": body}},
        )
        send_response.raise_for_status()
        return draft_id

    def _parse_message(self, payload: dict) -> EmailMessage:
        return EmailMessage(
            id=payload["id"],
            subject=payload.get("subject", "(no subject)"),
            sender=payload.get("from", {}).get("emailAddress", {}).get("address", ""),
            recipients=[recipient["emailAddress"]["address"] for recipient in payload.get("toRecipients", [])],
            snippet=payload.get("bodyPreview", ""),
            received_at=datetime.fromisoformat(payload.get("receivedDateTime")),
            body=payload.get("body", {}).get("content"),
            thread_id=payload.get("id"),
            raw_payload=payload,
        )


__all__ = ["OutlookConnector"]
