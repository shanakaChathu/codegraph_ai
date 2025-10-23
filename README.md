# CodeGraph.AI (MVP)
Agentic pipeline that reads a Jira story, builds a knowledge graph of a Python repo, chooses the right function to modify using OpenAI models, applies the change, creates a branch, and opens a GitHub Pull Request. Optionally runs pytest and comments results.

## Quick Start
1. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. Copy `.env.example` → `.env` and fill OpenAI/Jira/GitHub credentials
4. Start API: `uvicorn server:app --reload --port 8000`

### Trigger a run
```bash
curl -X POST http://127.0.0.1:8000/run \
  -H "Content-Type: application/json" \
  -d '{"jira_id": "CGAI-1", "repo_path": "/absolute/path/to/local/repo"}'
