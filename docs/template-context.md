# Template Build Context

> This file captures the decisions and reasoning behind this template so future iterations can pick up where we left off.

---

## Why this template exists

The core problem: every project starts from scratch. Agents re-invent instead of using existing tools, burn tokens without visibility, and don't retain context between sessions. Non-technical stakeholders can't navigate a folder of raw .md files. Collaboration is ad-hoc.

This template is a force-multiplier: faster agent onboarding, less course correction, a readable interface for humans (the dashboard), and automation that handles repetitive overhead.

---

## Key decisions made

| Decision | Why |
|----------|-----|
| `CLAUDE.md` stays as a 1-line redirect | Claude Code auto-loads it by filename — can't rename without losing that |
| `AGENTS.md` is the real entry point | Generic enough for any AI agent or human collaborator |
| Local dashboard (`dashboard.py`) instead of raw .md files | Non-technical stakeholders need rendered docs, not text files in editors |
| `Start.command` at root | Double-click to launch = zero terminal knowledge required for stakeholders |
| Single cascading template (not 3 separate ones) | One template that scales with the project type, controlled by a routing table in AGENTS.md |
| `scripts/` is first-class | Automation-first: agents are required to script anything repeated |
| `docs/context.md` with problem statement | Agents must ask for this if empty — prevents going off in the wrong direction |
| Agent visibility rule (3-line plan before multi-step tasks) | Prevents agents going dark and burning tokens without stakeholder awareness |
| `containerize.sh` dormant by default | Docker overhead only when team collaboration actually needs it |

---

## What's built

```
_project-template/
├── CLAUDE.md              1-line redirect to AGENTS.md
├── AGENTS.md              Agent entry point with summary, rules, routing table
├── README.md              Full human guide: setup, Claude Code vs chat, MCP, teams
├── Start.command          Double-click launcher (Mac)
├── start.sh               Cross-platform launcher
├── .env.example           Env var template
├── docs/
│   ├── overview.md        Project status + quick commands
│   ├── tasks.md           Task tracker (agents update each session)
│   ├── context.md         Problem statement + user stories
│   ├── decisions.md       Key decisions log
│   ├── stack.md           Approved libraries (pre-seeded by type)
│   ├── workflows.md       Standard process playbook
│   └── template-context.md  ← this file
└── scripts/
    ├── README.md           Scripts index (agents add entries here)
    ├── setup.sh            One-command first-run setup
    ├── dashboard.py        Local styled docs site on localhost:3100
    ├── new-project.sh      Scaffold new project by type (planning/prototype/script/product)
    └── containerize.sh     On-demand Docker setup
```

---

## What's not done yet (future iterations)

- [ ] Pre-seed `docs/stack.md` with domain-specific defaults per project type (mobile, platform, etc.)
- [ ] Add a `docs/architecture.md` stub for product-type projects
- [ ] Dashboard: pull active tasks and recent decisions into the overview page automatically (currently manual)
- [ ] Dashboard: add a dark mode / better theming pass
- [ ] `new-project.sh`: test on Linux (sed -i differs from macOS)
- [ ] Add standard workflow stubs for Arduino / hardware projects
- [ ] Consider: `scripts/health-check.sh` — verifies all required files exist and AGENTS.md is filled in
- [ ] README: add a section on how to use this with Cursor, Windsurf, or other AI coding tools

---

## How the cascade works

The `Type` field in `AGENTS.md` + the routing table tells agents which files to load. `new-project.sh` generates only the relevant subset of files for a given type. A planning project uses ~4 files. A full product uses everything.

---

## Original conversation

This template was designed and built in a single Claude Code session (worktree: `claude/gifted-cori`). The conversation covered: project structure, token efficiency, non-technical stakeholder UX, agent visibility, automation-first approach, and the CLAUDE.md vs AGENTS.md naming issue.
