# [Project Name]

> [One sentence describing what this project does and who it's for]

---

## What is this?

This is the project workspace for [Project Name]. It includes:
- A **local dashboard** where you can view project docs, tasks, and status — no code required
- **AI agent instructions** so Claude and other AI tools automatically understand the project
- **Scripts** that handle setup, collaboration, and repetitive tasks automatically

---

## Getting started

### Step 1 — First-time setup
Open **Terminal** and paste:
```
./scripts/setup.sh
```
This installs what you need. You only do this once.

> **How to open Terminal on Mac:** Press `Cmd + Space`, type "Terminal", press Enter.

### Step 2 — Open the project dashboard
Double-click **`Start.command`** in this folder.

A browser window will open at `http://localhost:3100` — this is your project dashboard. Leave the terminal window that opens running in the background.

> To stop the dashboard: click the terminal window and press `Ctrl+C`.
> To restart: double-click `Start.command` again.

### Step 3 — Fill in your project details
In the dashboard, open **Context** and describe the problem you're solving. This helps the AI understand your goals before it starts working.

---

## Working with AI

### When to use Claude Code (terminal)
Use Claude Code when you want the AI to **write, read, or change files** in this project — building features, fixing bugs, generating content, running scripts.

**How to start:**
1. Open Terminal
2. Navigate to this folder: `cd path/to/[project-name]`
3. Type: `claude`

Claude Code will automatically load `AGENTS.md` and understand your project.

### When to use Claude.ai (chat)
Use the web chat at claude.ai when you want to **talk through ideas**, ask questions, or get explanations — without making changes to files.

### Connecting this project to Claude Desktop (optional)
If you use the Claude Desktop app and want it to have context about this project:

1. Open Claude Desktop → Settings → Developer → Edit Config
2. Add this project folder as a filesystem MCP source:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/[project-name]"]
    }
  }
}
```
3. Restart Claude Desktop
4. Claude will now be able to read and reference files in this project from the chat interface

---

## For teams and developers

### Sharing with your team
To set up a containerized environment that anyone can run with one command:
```
./scripts/containerize.sh
```
Then commit the generated `Dockerfile` and `docker-compose.yml`. Team members run:
```
docker compose up
```

### Adding scripts
Automate anything you do more than once. Add scripts to `scripts/` and document them in `scripts/README.md`. The AI is instructed to do the same.

### Branching and contributing
See **Workflows** in the dashboard for the full git and collaboration process.

---

## Folder overview

| Folder / File | What it is |
|---------------|-----------|
| `docs/` | Project documentation — view it in the dashboard |
| `src/` | Project source code |
| `scripts/` | Automation — `scripts/README.md` lists all available scripts |
| `AGENTS.md` | Instructions for AI agents working on this project |
| `CLAUDE.md` | Claude Code entry point (points to AGENTS.md) |
| `.env.example` | Template for environment variables — copy to `.env` |

---

## Troubleshooting

**Dashboard doesn't open:**
Make sure Python 3 is installed. In Terminal: `python3 --version`
If not installed: https://python.org/downloads

**"Permission denied" running a script:**
```
chmod +x scripts/setup.sh && ./scripts/setup.sh
```

**Port 3100 already in use:**
Another dashboard instance is running. Find and stop it:
```
lsof -ti:3100 | xargs kill
```
Then relaunch.
