# [Project Name]
> [One sentence: what this is and who it's for]

## Summary — stop reading here unless your task requires more
**Mission:** [core objective in one line]
**Type:** [planning | prototype | script | product]
**Status:** [active | paused | complete] — [1-line status, updated each session]
**Stack:** [key tech] — full details in docs/stack.md
**Run:** `[command to start the project]`
**Dashboard:** `python3 scripts/dashboard.py` → http://localhost:3100

---

> ### Agent Rules
> 1. Update `docs/tasks.md` at the **start AND end** of every session. Write a plan there before any multi-step task.
> 2. Before writing custom code: check `docs/stack.md`, then search for an existing library. Script any command you run more than once and add it to `scripts/README.md`.
> 3. Log non-obvious decisions in `docs/decisions.md`. Keep docs updated as you work.
> 4. If `docs/context.md` Scoping Questions are unanswered: **ask the user first** — don't touch files or make structural decisions.
> 5. If scope seems multi-service or is growing beyond a single focus: read `docs/workflows.md` → Structural Decisions before creating folders or services.
>
> **Skip:** `README.md`, `Start.command`, `start.sh` — human-facing files only.

---

## Routing — load only what your task needs

| Need | File |
|------|------|
| Active tasks + current status | `docs/tasks.md` |
| Why we're building this | `docs/context.md` |
| Approved tech / libraries | `docs/stack.md` |
| Past decisions | `docs/decisions.md` |
| Standard build processes | `docs/workflows.md` |
| Available automation scripts | `scripts/README.md` |

---

## Project type reference

| Type | Active files |
|------|-------------|
| planning | tasks.md · context.md · workflows.md |
| prototype | tasks.md · context.md · stack.md · decisions.md |
| script | tasks.md · context.md · stack.md · decisions.md · scripts/ |
| product | all files |
