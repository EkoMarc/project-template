#!/bin/bash
# setup.sh — First-run project setup
# Run this once after cloning or pulling the project.
# Usage: ./scripts/setup.sh

set -e
cd "$(dirname "$0")/.."

echo "=== Project Setup ==="
echo ""

# ── 1. Environment variables ────────────────────────────────────────────────
if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Created .env from .env.example"
        echo "  → Open .env and fill in your values before continuing."
    fi
else
    echo "✓ .env already exists"
fi

# ── 2. Python dependencies ──────────────────────────────────────────────────
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 found: $(python3 --version)"
    python3 -c "import markdown" 2>/dev/null || \
        pip3 install --user markdown --quiet 2>/dev/null || \
        pip3 install --user --break-system-packages markdown --quiet 2>/dev/null || true
    python3 -c "import markdown" 2>/dev/null && echo "✓ markdown package ready" || echo "⚠ markdown install failed — dashboard may not work"
else
    echo "✗ Python 3 not found — install from https://python.org/downloads"
    exit 1
fi

# ── 3. Make scripts executable ──────────────────────────────────────────────
chmod +x scripts/*.sh Start.command start.sh 2>/dev/null || true
echo "✓ Scripts are executable"

# ── 4. Project-specific setup ───────────────────────────────────────────────
# Add your setup steps below:
# e.g. npm install, pip install -r requirements.txt, etc.

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "=== Setup complete ==="
echo "Run: ./start.sh  (or double-click Start.command on Mac)"
echo "     → opens the project dashboard at http://localhost:3100"
