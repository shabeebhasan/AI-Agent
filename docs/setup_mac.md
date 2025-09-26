# macOS Setup Guide

Launch the AI email orchestration agent on macOS Sonoma or later.

## 1. Prerequisites
- Install [Homebrew](https://brew.sh/).
- Install Python and Git:
  ```bash
  brew install python@3.11 git
  ```
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) if you plan to self-host n8n.
- Ensure you have access to OpenAI, Google Cloud, and Azure credentials.

## 2. Clone the Repository
```bash
git clone https://github.com/<your-handle>/ai-email-agent.git
cd ai-email-agent
```

## 3. Create a Virtual Environment
```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

## 4. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Environment Variables
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o
GMAIL_SERVICE_ACCOUNT_FILE=/Users/you/credentials/service-account.json
GMAIL_DELEGATED_USER=you@company.com
OUTLOOK_CLIENT_ID=...
OUTLOOK_CLIENT_SECRET=...
OUTLOOK_TENANT_ID=...
OUTLOOK_USER_ID=you@company.com
ALLOWED_SENDERS=ceo@company.com,cto@company.com
```

## 6. Test the Agent
```bash
uvicorn email_agent.workflows:app --reload
```

Visit http://127.0.0.1:8000/docs and execute the `/run` endpoint with `{ "provider": "outlook" }` to validate credentials.

## 7. Optional: Run n8n Locally
```bash
docker run -it --rm -p 5678:5678 n8nio/n8n:latest
```
Import `integration/n8n_email_agent.json` via *Settings → Import from File*.

## 8. Deploy to the Cloud
- Use `uvicorn` behind an [NGINX reverse proxy](https://www.nginx.com/) on an Ubuntu VM.
- Or deploy to [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/) with environment secrets.
- Configure HTTPS using Let's Encrypt and automate certificate renewal with Certbot.

## 9. Troubleshooting
- Verify Gmail service accounts have domain-wide delegation.
- Confirm the Microsoft Graph application has the `Mail.ReadWrite` application permission and admin consent.
- Use `python -m http.server` to confirm your firewall allows inbound requests.
