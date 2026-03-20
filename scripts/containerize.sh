#!/bin/bash
# containerize.sh — On-demand Docker setup for team collaboration
#
# Run this when you need to share a working environment with other developers.
# Generates Dockerfile and docker-compose.yml based on your project's stack.
#
# Usage: ./scripts/containerize.sh

set -e
cd "$(dirname "$0")/.."

echo "=== Docker Setup ==="
echo ""

# Check if Docker files already exist
if [ -f Dockerfile ]; then
    echo "Dockerfile already exists. Delete it first if you want to regenerate."
    exit 1
fi

# ── Detect project type from AGENTS.md ───────────────────────────────────────
PROJECT_TYPE="generic"
if [ -f AGENTS.md ]; then
    TYPE_LINE=$(grep "^\*\*Type:\*\*" AGENTS.md | head -1 || true)
    if echo "$TYPE_LINE" | grep -q "script"; then PROJECT_TYPE="python"; fi
    if echo "$TYPE_LINE" | grep -q "prototype"; then PROJECT_TYPE="node"; fi
    if echo "$TYPE_LINE" | grep -q "product"; then PROJECT_TYPE="node"; fi
fi

# ── Generate Dockerfile ───────────────────────────────────────────────────────
if [ "$PROJECT_TYPE" = "python" ]; then
cat > Dockerfile << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt* ./
RUN pip install --no-cache-dir -r requirements.txt 2>/dev/null || true
COPY . .
EXPOSE 3100
CMD ["python3", "scripts/dashboard.py"]
EOF
else
cat > Dockerfile << 'EOF'
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci 2>/dev/null || true
COPY . .
RUN apt-get update && apt-get install -y python3 python3-pip --no-install-recommends 2>/dev/null || \
    apk add --no-cache python3 py3-pip 2>/dev/null || true
RUN pip3 install markdown --quiet 2>/dev/null || true
EXPOSE 3100
CMD ["python3", "scripts/dashboard.py"]
EOF
fi

# ── Generate docker-compose.yml ───────────────────────────────────────────────
cat > docker-compose.yml << 'EOF'
version: "3.9"
services:
  app:
    build: .
    ports:
      - "3100:3100"
    volumes:
      - .:/app
      - /app/node_modules
    env_file:
      - .env
    restart: unless-stopped
EOF

# ── Generate .dockerignore ────────────────────────────────────────────────────
cat > .dockerignore << 'EOF'
.env
.git
node_modules
__pycache__
*.pyc
.DS_Store
EOF

echo "✓ Generated: Dockerfile"
echo "✓ Generated: docker-compose.yml"
echo "✓ Generated: .dockerignore"
echo ""
echo "=== How to use ==="
echo ""
echo "Start:   docker compose up"
echo "Stop:    docker compose down"
echo "Rebuild: docker compose up --build"
echo ""
echo "Share this repo with your team — they run 'docker compose up' to get started."
echo ""

# ── Document in workflows.md ──────────────────────────────────────────────────
if [ -f docs/workflows.md ]; then
    echo "Note: Docker files have been generated. Document any project-specific"
    echo "      Docker instructions in docs/workflows.md."
fi
