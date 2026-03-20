#!/bin/bash
# Project Dashboard — cross-platform launcher
# Starts the local documentation site at http://localhost:3100

cd "$(dirname "$0")"

if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found."
    echo "Install it from https://python.org/downloads"
    exit 1
fi

python3 -c "import markdown" 2>/dev/null || pip3 install markdown --quiet

echo "Starting project dashboard at http://localhost:3100"
echo "Press Ctrl+C to stop."

# Try to open browser (works on Mac, Linux with xdg-open)
(sleep 1.5 && (open http://localhost:3100 2>/dev/null || xdg-open http://localhost:3100 2>/dev/null || true)) &

python3 scripts/dashboard.py
