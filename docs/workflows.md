# Standard Workflows

<!-- Agents: Follow the relevant workflow for your task type.
     Update or add a workflow when a new repeatable process is established.
     This is the "don't reinvent the wheel" reference. -->

---

## Git & Collaboration

### Branch naming
| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/[name]` | `feature/user-auth` |
| Bug fix | `fix/[name]` | `fix/login-error` |
| Prototype/exploration | `exploration/[name]` | `exploration/onboarding-v2` |
| Chore / maintenance | `chore/[name]` | `chore/update-deps` |

### Commit messages
```
feat: add user authentication
fix: resolve login redirect loop
update: improve error message clarity
docs: update setup instructions
chore: bump dependencies
```

### PR process
1. Branch off `main`
2. Make changes, commit with clear messages
3. Open PR with description of what changed and why
4. Request review if collaborating
5. Merge to `main` when approved

---

## Team Collaboration (containerized)

For sharing a working environment with engineers:
```bash
./scripts/containerize.sh
```
This generates a `Dockerfile` and `docker-compose.yml` and documents how to use them.

---

## Mobile App

1. Scaffold: define screens in a flow doc, scaffold component structure
2. Build: implement screens in order of user flow
3. Test: device testing on iOS + Android
4. Deploy: TestFlight (iOS), Play Console internal track (Android)
5. Document: update stack.md with any new dependencies

---

## Simple Site / Landing Page

1. Scaffold: `src/index.html` + `src/style.css`, no build step
2. Build: implement in pure HTML/CSS/JS, import tokens from CSS vars
3. Test: browser check on mobile + desktop
4. Deploy: Netlify drop, Vercel, or GitHub Pages
5. Document: add deploy URL to overview.md

---

## Platform / API

1. Scaffold: define endpoints, data models, auth strategy in decisions.md
2. Build: implement routes, models, middleware
3. Test: integration tests against real database (not mocks)
4. Deploy: containerize (`./scripts/containerize.sh`), then to cloud
5. Document: update stack.md, add API reference to docs/

---

## Data Pipeline / Script

1. Scaffold: define input/output format, dependencies in stack.md
2. Build: implement with CLI interface (Click), log with Rich
3. Test: pytest with real data samples
4. Deploy: add to scripts/README.md, schedule if recurring
5. Document: usage instructions in scripts/README.md

---

## Design Library

1. Scaffold: define token structure, component inventory
2. Build: implement tokens first, then components
3. Test: visual review in target environments
4. Deploy: publish to package registry or share as static assets
5. Document: component API in docs/, decisions in decisions.md

---

<!-- Add new workflows here as processes are established -->
