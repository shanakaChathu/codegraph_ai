Step 2 — Start the FastAPI Server

From the root of the backend (where main.py is located), run:

uvicorn main:app --reload --host 127.0.0.1 --port 8000


✅ Expected output:

INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.


Verify it’s running by visiting:
👉 http://127.0.0.1:8000

You should see:

{"status": "CodeGraph.AI backend is running"}

💡 3️⃣ VS Code Extension Installation

The CodeGraph.AI VS Code extension (.vsix file) allows developers to run the agent directly inside VS Code.

The .vsix file is included in this repository (e.g. codegraph-ai-0.0.1.vsix).

Option A — Install via Command Line

Open a terminal and run:

code --install-extension ./codegraph-ai-0.0.1.vsix


Example:

code --install-extension C:\Projects\CodeGraph_AI\codegraph-ai-0.0.1.vsix


✅ You’ll see:

Extension 'codegraph-ai' was successfully installed!

Option B — Install via VS Code Interface

Open Visual Studio Code

Go to Extensions (Ctrl + Shift + X)

Click the “⋯” (three dots) menu in the top-right corner

Choose “Install from VSIX…”

Select the codegraph-ai-0.0.1.vsix file

✅ Wait for the confirmation that installation was successful

🧩 4️⃣ Running the Extension

Once installed:

Open your main repository (the one where you want CodeGraph.AI to make changes)

Ensure your FastAPI backend is running (http://127.0.0.1:8000)

In VS Code, press Ctrl + Shift + P

Type and select:

Run CodeGraph.AI Agent


Enter:

Jira ID → e.g. JIRA-123

Branch name → e.g. feature/new-module

✅ The extension will call the FastAPI endpoint /run-agent and return the result directly in VS Code.

⚙️ 5️⃣ Configuration (Optional)

You can configure the backend URL or default behavior via VS Code settings:

Open:

Settings → Extensions → CodeGraph.AI


Update Backend URL to match your environment:

http://127.0.0.1:8000


or your remote backend, e.g.:

https://api.codegraph.ai

🔁 6️⃣ Updating the Extension

When a new version is shared (e.g. codegraph-ai-0.0.2.vsix):

Optional — uninstall the old version:

code --uninstall-extension codegraph-ai


Install the new version:

code --install-extension ./codegraph-ai-0.0.2.vsix


VS Code will automatically replace the old version.

🧾 7️⃣ Verifying Setup
✅ Check Backend

Visit: http://127.0.0.1:8000

Response should be:

{"status": "CodeGraph.AI backend is running"}

✅ Check Extension

In VS Code:

Open Extensions tab

Confirm CodeGraph.AI is listed under Installed extensions

✅ Test Command

Press Ctrl + Shift + P → run Run CodeGraph.AI Agent
Check your FastAPI terminal — it should log incoming requests.

🚀 8️⃣ Common Commands
Purpose	Command
Start FastAPI	uvicorn main:app --reload --host 127.0.0.1 --port 8000
Install Extension	code --install-extension ./codegraph-ai-0.0.1.vsix
Uninstall Extension	code --uninstall-extension codegraph-ai
List Installed Extensions	code --list-extensions
👥 9️⃣ Team Setup Workflow
Step	Who	Description
1	You	Push repo (including .vsix file)
2	Teammate	Clone the repo
3	Teammate	Install Python dependencies
4	Teammate	Start FastAPI backend
5	Teammate	Install .vsix extension
6	Teammate	Open repo in VS Code & run “Run CodeGraph.AI Agent”
🧠 10️⃣ Architecture Overview
flowchart TD
    A[VS Code Extension (CodeGraph.AI)] -->|API Call| B[FastAPI Backend]
    B -->|GitHub PR Creation| C[GitHub]
    B -->|Story Fetch & Update| D[Jira]
    B -->|Logs & Response| A

👨‍💻 Author

Shanaka Chathuranga
Creator of CodeGraph.AI
✨ Empowering developers with intelligent, agent-based automation for Jira and GitHub workflows.