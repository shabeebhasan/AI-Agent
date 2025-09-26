# Portfolio Playbook

Use this project to highlight your ability to architect AI-first automation systems.

## Talking Points
- **Architecture**: Describe how the LangGraph state machine coordinates multiple tools and keeps reasoning transparent.
- **Multi-provider**: Emphasize support for both Gmail and Outlook with reusable connector abstractions.
- **Automation**: Showcase the n8n workflow and how it triggers the FastAPI agent, calls Slack or Teams, and logs everything.
- **Safety**: Discuss the `ALLOWED_SENDERS` allowlist and how you would extend it with DLP rules.

## Suggested Artifacts
- Sequence diagram of the agent flow (OpenAI → Agent → Gmail/Outlook → n8n).
- Screenshots of the FastAPI Swagger UI and successful `/run` invocation.
- Screenshot of the imported n8n workflow highlighting AI steps.
- Short Loom video walking through the code structure.

## Interview Demo Script
1. Introduce the business problem: overflowing inboxes.
2. Explain the agent's architecture using the README diagram.
3. Run the FastAPI endpoint locally and show logs in the terminal.
4. Trigger the n8n workflow to demonstrate automation chaining (e.g., create a task in Notion).
5. Conclude with a roadmap: add Teams connector, CRM sync, automated meeting scheduling.

## Resume Bullet Examples
- "Architected a LangGraph-based AI triage agent that autonomously summarizes and replies to executive emails across Gmail and Outlook."
- "Integrated an AI microservice with n8n to orchestrate cross-platform workflows, reducing manual email handling by 70%."
- "Implemented secure credential management and role-based guardrails for AI-generated communications."
