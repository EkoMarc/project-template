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

> ### Agent Rules — required behavior
> 1. Update `docs/tasks.md` at the **start AND end** of every session.
> 2. Before any multi-step task: write a brief plan (3–5 lines) in `docs/tasks.md` first.
> 3. Before writing custom code: check `docs/stack.md`, then search for an existing library or tool.
> 4. Any command you run more than once → script it and add an entry to `scripts/README.md`.
> 5. Log non-obvious decisions in `docs/decisions.md`.
> 6. If `docs/context.md` has no problem statement: **ask the user** to describe the problem they're solving before starting work.
> 7. Keep relevant docs updated as you work. Don't leave them stale.
>
> **Skip:** `README.md` (human setup only). `Start.command` / `start.sh` are launcher scripts.

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
