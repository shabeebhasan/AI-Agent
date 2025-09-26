# AI Email Orchestration Agent

This repository provides a production-ready template for an AI-powered email orchestration agent that can triage, summarize, and automate actions across Gmail, Outlook, and other inboxes. The project combines a LangGraph-based agent, reusable connector SDKs, and n8n workflow automation to create a portfolio-ready showcase of advanced AI engineering practices.

## Features
- **Modular LangGraph agent** with tool calling, multi-step reasoning, and memory persistence.
- **Gmail and Outlook connectors** implemented with OAuth2 credentials and pagination helpers.
- **n8n workflow** for no-code automation with AI responses and third-party integrations.
- **Infrastructure-as-code** templates for deploying the agent as a FastAPI microservice.
- **Extensive documentation** for Windows and macOS setup, environment variables, and cloud deployment.
- **Portfolio focus** with examples, diagrams, and talking points for demonstrating expertise.

## Repository Layout

```
├── README.md
├── docs
│   ├── portfolio_guide.md
│   ├── setup_mac.md
│   └── setup_windows.md
├── examples
│   └── conversation_demo.md
├── integration
│   └── n8n_email_agent.json
├── src
│   └── email_agent
│       ├── __init__.py
│       ├── agent.py
│       ├── config.py
│       ├── connectors
│       │   ├── base.py
│       │   ├── gmail.py
│       │   └── outlook.py
│       └── workflows.py
└── tests
    └── test_config.py
```

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure environment variables as described in [`docs/setup_windows.md`](docs/setup_windows.md) or [`docs/setup_mac.md`](docs/setup_mac.md).
3. Launch the FastAPI microservice:
   ```bash
   uvicorn email_agent.workflows:app --host 0.0.0.0 --port 8000
   ```
4. Import the n8n workflow from [`integration/n8n_email_agent.json`](integration/n8n_email_agent.json) and update the credentials.

## Portfolio Highlights

Use the scripts and documentation in this repo to build a compelling story for your portfolio:
- Emphasize your ability to orchestrate AI tools, email APIs, and automation platforms.
- Include screenshots of the n8n flow, FastAPI docs, and sample conversations with the agent.
- Reference the `examples/conversation_demo.md` when discussing real-world scenarios.

## Contributing

1. Fork the repository.
2. Create a branch for your feature or fix.
3. Ensure tests pass with `pytest` before submitting a PR.
4. Follow conventional commit messages (e.g., `feat: add teams connector`).

## License

This project is provided under the MIT License.
