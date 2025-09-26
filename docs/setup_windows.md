# Windows Setup Guide

Follow this checklist to launch the AI email orchestration agent on Windows 11.

## 1. Prerequisites
- Install [Python 3.11](https://www.python.org/downloads/windows/).
- Install [Git for Windows](https://git-scm.com/downloads).
- Optional: Install [Windows Subsystem for Linux](https://learn.microsoft.com/windows/wsl/install) for a Linux-like environment.
- Create OpenAI, Google Cloud, and Microsoft Azure accounts with the required API access.

## 2. Clone the Repository
```powershell
git clone https://github.com/<your-handle>/ai-email-agent.git
cd ai-email-agent
```

## 3. Create a Virtual Environment
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
```

## 4. Install Dependencies
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Environment Variables
Create a `.env` file in the repository root:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
GMAIL_SERVICE_ACCOUNT_FILE=C:\\path\\to\\service-account.json
GMAIL_DELEGATED_USER=you@company.com
OUTLOOK_CLIENT_ID=...
OUTLOOK_CLIENT_SECRET=...
OUTLOOK_TENANT_ID=...
OUTLOOK_USER_ID=you@company.com
ALLOWED_SENDERS=ceo@company.com,cto@company.com
```

## 6. Prepare Credentials
- **Gmail**: Create a Google Cloud project, enable the Gmail API, and download a service account JSON file. Delegate domain-wide authority and grant the scopes listed in `src/email_agent/connectors/gmail.py`.
- **Outlook**: Register an Azure AD application with the Microsoft Graph `Mail.ReadWrite` permission. Create a client secret and record the tenant ID.

## 7. Launch the API
```powershell
uvicorn email_agent.workflows:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000/docs to access the interactive Swagger UI.

## 8. Import the n8n Workflow
1. Start n8n via Docker or the desktop app.
2. Open *Settings → Import from File* and select `integration/n8n_email_agent.json`.
3. Update the HTTP Request node URL to point to your FastAPI endpoint.
4. Configure credentials inside n8n for Gmail/Outlook actions if needed.

## 9. Run the Agent
Trigger the n8n workflow or send a `POST` request:
```powershell
curl -X POST http://localhost:8000/run -H "Content-Type: application/json" -d '{"provider": "gmail"}'
```

## 10. Production Tips
- Use [pm2](https://pm2.keymetrics.io/) or Windows Services to keep the API running.
- Store secrets in Azure Key Vault or AWS Secrets Manager.
- Enable HTTPS with a reverse proxy (IIS, Nginx, or Caddy).
