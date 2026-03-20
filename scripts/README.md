# Scripts

<!-- Agents: If you run a command more than once, script it and add an entry here.
     This is the automation registry for this project. -->

---

## Standard Scripts

| Script | What it does | Run with |
|--------|-------------|----------|
| `setup.sh` | Install dependencies, configure env, first-run setup | `./scripts/setup.sh` |
| `dashboard.py` | Serve `docs/` as a local styled site on port 3100 | `python3 scripts/dashboard.py` |
| `new-project.sh` | Scaffold a new project from this template | `./scripts/new-project.sh [name] [type]` |
| `containerize.sh` | Generate Docker setup for team collaboration | `./scripts/containerize.sh` |

---

## Project Scripts

<!-- Agents: Add entries here as you create project-specific scripts -->

| Script | What it does | Run with |
|--------|-------------|----------|
| | | |

---

## Adding a script

1. Create the script in `scripts/`
2. Make it executable: `chmod +x scripts/your-script.sh`
3. Add a row to the **Project Scripts** table above
4. Keep scripts focused — one purpose per script
