#!/bin/bash
# Project Dashboard — cross-platform launcher
# Starts the local documentation site at http://localhost:3100

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found."
    echo "Install it from https://python.org/downloads"
    exit 1
fi

python3 -c "import markdown" 2>/dev/null || \
    pip3 install --user markdown --quiet 2>/dev/null || \
    pip3 install --user --break-system-packages markdown --quiet 2>/dev/null || true

echo "Starting project dashboard..."
echo "Press Ctrl+C to stop."

PORT=3100
while lsof -ti:$PORT &>/dev/null; do PORT=$((PORT+1)); done

(sleep 1.5 && (open "http://localhost:$PORT" 2>/dev/null || xdg-open "http://localhost:$PORT" 2>/dev/null || true)) &

python3 scripts/dashboard.py
