#!/bin/bash
# Project Dashboard — double-click to open
# This launches a local documentation site at http://localhost:3100
# Leave this terminal window open while you're working.

cd "$(dirname "$0")"

# Check Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found."
    echo "Install it from https://python.org/downloads"
    read -p "Press Enter to close..."
    exit 1
fi

# Install markdown package if missing
python3 -c "import markdown" 2>/dev/null || pip3 install markdown --quiet

echo "Starting project dashboard..."
echo "Opening http://localhost:3100"
echo ""
echo "Leave this window open. Press Ctrl+C to stop."
echo ""

# Open browser after short delay
(sleep 1.5 && open http://localhost:3100) &

python3 scripts/dashboard.py
