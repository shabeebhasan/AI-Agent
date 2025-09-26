# Conversation Demo

```text
User (CEO): Hey team, we just received a partnership inquiry from Acme Corp. Can someone triage and propose next steps?

Agent: Checking the latest unread emails from allowed senders...

Agent: Found email "Partnership Proposal from Acme Corp". Classifying intent...

Agent: Action = schedule_call
Reasoning = "This email proposes a strategic partnership and requests a follow-up meeting."

Agent: Drafting reply with LangGraph `craft_reply` tool...

Agent: Reply sent! "Hi Jordan, thrilled to explore a partnership. I've shared availability for next week so we can dive into details."

n8n: Received webhook response and automatically created a task in Notion + notified Slack channel.
```
