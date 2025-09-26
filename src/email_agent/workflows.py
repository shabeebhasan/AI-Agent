"""FastAPI application exposing the agent as an HTTP API."""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from .agent import AgentState, build_agent_executor
from .config import Settings, get_settings
from .connectors.gmail import GmailConnector
from .connectors.outlook import OutlookConnector

app = FastAPI(title="AI Email Orchestration Agent", version="1.0.0")


class Provider(str):
    GMAIL = "gmail"
    OUTLOOK = "outlook"


class RunRequest(BaseModel):
    provider: Literal["gmail", "outlook"]


class RunResponse(BaseModel):
    action: Optional[str]
    result: Optional[str]


async def get_connector(settings: Settings, provider: Provider = Provider.GMAIL):
    if provider == Provider.GMAIL:
        if not (settings.gmail_service_account_file and settings.gmail_delegated_user):
            raise HTTPException(status_code=400, detail="Gmail credentials are not configured")
        return GmailConnector(
            service_account_file=settings.gmail_service_account_file,
            delegated_user=settings.gmail_delegated_user,
        )
    if provider == Provider.OUTLOOK:
        required = [
            settings.outlook_client_id,
            settings.outlook_client_secret,
            settings.outlook_tenant_id,
            settings.outlook_user_id,
        ]
        if any(value is None for value in required):
            raise HTTPException(status_code=400, detail="Outlook credentials are not configured")
        return OutlookConnector(
            client_id=settings.outlook_client_id or "",
            client_secret=settings.outlook_client_secret or "",
            tenant_id=settings.outlook_tenant_id or "",
            user_id=settings.outlook_user_id or "",
        )
    raise HTTPException(status_code=404, detail=f"Unsupported provider {provider}")


@app.post("/run", response_model=RunResponse)
async def run_agent(payload: RunRequest, settings: Settings = Depends(get_settings)) -> RunResponse:
    connector = await get_connector(settings, Provider(payload.provider))
    executor = build_agent_executor(connector)
    state: AgentState = await executor["run"]()
    return RunResponse(action=state.get("action"), result=state.get("result"))


@app.get("/healthz")
async def healthcheck() -> dict:
    return {"status": "ok"}
