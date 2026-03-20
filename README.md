# [Project Name]

> [One sentence describing what this project does and who it's for]

---

## What is this?

This is the project workspace for [Project Name]. It includes:
- A **local dashboard** to view docs, tasks, and status — no code required
- **AI agent instructions** so Claude and other AI tools automatically understand the project
- **Scripts** that handle setup, collaboration, and repetitive tasks automatically

---

## Getting started

### Step 1 — First-time setup
Open **Terminal** and paste:
```
./scripts/setup.sh
```
You only do this once. It installs what the dashboard needs to run.

> **How to open Terminal on Mac:** Press `Cmd + Space`, type "Terminal", press Enter.

### Step 2 — Open the project dashboard
Double-click **`Start.command`** in this folder.

Your browser opens automatically — this is your project dashboard. Leave the terminal window running in the background while you work.

> To stop: click the terminal window and press `Ctrl+C`
> To reopen: double-click `Start.command` again

### Step 3 — Fill in your project details
In the dashboard, open **Context** and answer the scoping questions. This is what the AI reads to understand your project before starting work.

---

## Starting a new project from this template

### Option A — Double-click (easiest)
Double-click **`New Project.command`** in this folder.

Terminal will open and ask you three questions:
1. What's the project name?
2. What type is it? (planning / prototype / script / product)
3. Where do you want to create it?

It then creates the project, opens its dashboard, and you're ready to go.

### Option B — Terminal command
```
./scripts/new-project.sh my-project-name product ~/Projects
```

### What's the difference between this and just copying the folder?
Both work. The difference: this script copies only the files relevant to your project type (a planning project doesn't need Docker setup or environment variables), pre-fills your project name everywhere, and runs `git init` automatically. Copying the folder is fine too — just delete `docs/template-context.md` afterward (it's about this template, not your project) and fill in `AGENTS.md` manually.

---

## Working with AI

### Claude Code (makes changes to files)
Use this when you want the AI to write, build, fix, or generate anything in the project.

1. Open Terminal
2. `cd path/to/your-project`
3. `claude`

Claude Code automatically reads `AGENTS.md` and understands your project.

### Claude.ai chat (ideas and questions)
Use the web chat when you want to think through a problem, ask questions, or get explanations — without the AI touching any files.

### Connecting to Claude Desktop (optional)
To give the Claude Desktop app access to your project files:

1. Open Claude Desktop → Settings → Developer → Edit Config
2. Add:
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/your-project"]
    }
  }
}
```
3. Restart Claude Desktop — it can now read and reference your files in chat

---

## For teams

### Share a working environment
```
./scripts/containerize.sh
```
Generates a `Dockerfile` and `docker-compose.yml`. Edit the Dockerfile for your stack, then commit. Teammates run `docker compose up` to get started.

### Adding automation
Add scripts to `scripts/` and document them in `scripts/README.md`. The AI is instructed to do the same.

### Branching and contributing
See **Workflows** in the dashboard.

---

## Folder overview

| Folder / File | What it is |
|---------------|-----------|
| `docs/` | Project documentation — view in the dashboard |
| `src/` | Project source code |
| `scripts/` | Automation scripts — see `scripts/README.md` |
| `AGENTS.md` | AI agent instructions for this project |
| `CLAUDE.md` | Claude Code entry point (redirects to AGENTS.md) |
| `.env.example` | Environment variable template — copy to `.env` and fill in |

---

## Troubleshooting

**Dashboard doesn't open:**
Make sure Python 3 is installed — in Terminal: `python3 --version`
If missing: https://python.org/downloads

**"Permission denied" running a script:**
```
chmod +x scripts/setup.sh && ./scripts/setup.sh
```

**Two projects open at the same time:**
No action needed — the dashboard automatically picks a free port if 3100 is taken.
