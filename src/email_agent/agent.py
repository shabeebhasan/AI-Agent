"""LangGraph agent that orchestrates email triage."""

from __future__ import annotations

import asyncio
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Literal, Optional, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from .config import get_settings
from .connectors.base import EmailConnector, EmailMessage


class AgentState(TypedDict):
    """State container for LangGraph."""

    conversation: List[Any]
    task: Optional[str]
    message: Optional[EmailMessage]
    action: Optional[str]
    result: Optional[str]


@dataclass
class ToolResponse:
    name: str
    content: str

    def to_message(self) -> AIMessage:
        return AIMessage(content=self.content, name=self.name)


def _format_email_summary(message: EmailMessage) -> str:
    return (
        f"Subject: {message.subject}\n"
        f"From: {message.sender}\n"
        f"To: {', '.join(message.recipients)}\n"
        f"Received: {message.received_at.isoformat()}\n\n"
        f"Snippet:\n{message.snippet}\n\n"
        f"Body:\n{message.body or '(body not fetched)'}"
    )


def build_agent_executor(connector: EmailConnector) -> Any:
    """Create a LangGraph executor configured for email triage."""

    settings = get_settings()
    llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.1)

    @tool
    def summarize_email(email: Dict[str, Any]) -> str:
        """Summarize the important details of an email."""

        return _format_email_summary(EmailMessage(**email))

    @tool
    def craft_reply(email: Dict[str, Any], intent: Literal["acknowledge", "schedule_call", "delegate"], notes: str) -> str:
        """Generate a short reply email text for the provided intent."""

        prompt = (
            "You are an executive assistant. Write a concise email reply given the user's intent.\n"
            f"Intent: {intent}\nNotes: {notes}\n"
            f"Email: {_format_email_summary(EmailMessage(**email))}"
        )
        response = llm.invoke([SystemMessage(content="You write professional email replies."), HumanMessage(content=prompt)])
        return response.content

    async def select_email(state: AgentState) -> AgentState:
        if state.get("message"):
            return state
        messages = []
        async for message in connector.list_messages(limit=1):
            messages.append(message)
        if not messages:
            return {**state, "task": "idle"}
        message = messages[0]
        allowed = get_settings().allowed_senders
        if allowed and message.sender not in allowed:
            return {**state, "message": message, "task": "ignore"}
        return {**state, "message": message, "task": "triage"}

    async def analyze(state: AgentState) -> AgentState:
        message = state.get("message")
        if not message:
            return state
        system_prompt = SystemMessage(
            content="You are an AI email chief of staff who classifies emails and decides the best action."
        )
        user_prompt = HumanMessage(
            content=(
                "Determine the best action for this email. Respond with JSON containing "
                "{\"action\": <acknowledge|schedule_call|delegate|ignore>, \"notes\": "
                "<reasoning>}.\n\nEmail:\n" + _format_email_summary(message)
            )
        )
        response = llm.invoke([system_prompt, user_prompt])
        state["conversation"].extend([system_prompt, user_prompt, response])
        try:
            payload = response.response_metadata.get("parsed", None) or response.additional_kwargs
            action = payload.get("action") if isinstance(payload, dict) else None
            notes = payload.get("notes") if isinstance(payload, dict) else None
        except Exception:  # pragma: no cover
            action = None
            notes = None
        if action not in {"acknowledge", "schedule_call", "delegate", "ignore"}:
            action = "acknowledge"
        return {**state, "action": action, "result": notes or ""}

    async def perform_action(state: AgentState) -> AgentState:
        message = state.get("message")
        if not message:
            return state
        action = state.get("action")
        if action in {"acknowledge", "schedule_call", "delegate"}:
            reply = craft_reply.invoke({
                "email": asdict(message),
                "intent": action,
                "notes": state.get("result", ""),
            })
            await connector.send_reply(thread_id=message.thread_id or message.id, body=reply)
            return {**state, "result": reply}
        return {**state, "result": state.get("result", ""), "action": action}

    async def finalize(state: AgentState) -> AgentState:
        return state

    workflow = StateGraph(AgentState)
    workflow.add_node("select_email", select_email)
    workflow.add_node("analyze", analyze)
    workflow.add_node("perform_action", perform_action)
    workflow.add_node("finalize", finalize)

    workflow.add_edge(START, "select_email")
    workflow.add_conditional_edges(
        "select_email",
        lambda state: state.get("task"),
        {
            "triage": "analyze",
            "ignore": "finalize",
            "idle": END,
        },
    )
    workflow.add_edge("analyze", "perform_action")
    workflow.add_edge("perform_action", "finalize")
    workflow.add_edge("finalize", END)

    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)

    async def run() -> AgentState:
        initial_state: AgentState = {
            "conversation": [],
            "task": None,
            "message": None,
            "action": None,
            "result": None,
        }
        async for state in graph.astream(initial_state):
            last_state = state
        return last_state  # type: ignore[misc]

    return {
        "graph": graph,
        "run": run,
        "tools": {"summarize_email": summarize_email, "craft_reply": craft_reply},
    }


__all__ = ["build_agent_executor", "AgentState"]
