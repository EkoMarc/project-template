#!/bin/bash
# containerize.sh — Docker setup for team collaboration
#
# Run this when you need to share a working environment with other developers.
# Generates stub files — edit Dockerfile for your stack before committing.
#
# Usage: ./scripts/containerize.sh

set -e
cd "$(dirname "$0")/.."

if [ -f Dockerfile ]; then
    echo "Dockerfile already exists. Delete it first to regenerate."
    exit 1
fi

# ── Dockerfile stub ───────────────────────────────────────────────────────────
cat > Dockerfile << 'EOF'
# TODO: Replace with your base image
# Examples: python:3.11-slim | node:20-alpine | ubuntu:22.04
FROM python:3.11-slim

WORKDIR /app

# TODO: Copy and install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# TODO: Set your run command
EXPOSE 3100
CMD ["python3", "scripts/dashboard.py"]
EOF

# ── docker-compose.yml stub ───────────────────────────────────────────────────
cat > docker-compose.yml << 'EOF'
version: "3.9"
services:
  app:
    build: .
    ports:
      - "3100:3100"
    volumes:
      - .:/app
    env_file:
      - .env
    restart: unless-stopped
EOF

# ── .dockerignore ─────────────────────────────────────────────────────────────
cat > .dockerignore << 'EOF'
.env
.git
.claude/
node_modules/
__pycache__/
*.pyc
.DS_Store
EOF

echo "✓ Dockerfile, docker-compose.yml, .dockerignore created"
echo ""
echo "Next:"
echo "  1. Edit Dockerfile — fill in base image, deps, run command"
echo "  2. docker compose up           — start"
echo "  3. docker compose up --build   — rebuild after changes"
echo "  4. Commit so teammates can run: docker compose up"
