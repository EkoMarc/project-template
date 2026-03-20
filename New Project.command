#!/bin/bash
# New Project.command — double-click to scaffold a new project from this template

TEMPLATE_DIR="$(cd "$(dirname "$0")" && pwd)"

clear
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  New Project"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# ── Project name ──────────────────────────────────────────────────────────────
read -p "Project name (e.g. my-dashboard): " PROJECT_NAME
if [ -z "$PROJECT_NAME" ]; then
    echo "No name entered. Exiting."
    exit 1
fi

echo ""

# ── Project type ──────────────────────────────────────────────────────────────
echo "Project type:"
echo "  1) planning  — tasks, docs, no code"
echo "  2) prototype — explorations, sandboxes"
echo "  3) script    — a tool or automation"
echo "  4) product   — full build (all files)"
echo ""
read -p "Choose 1–4 [4]: " TYPE_CHOICE

case "$TYPE_CHOICE" in
    1) PROJECT_TYPE="planning" ;;
    2) PROJECT_TYPE="prototype" ;;
    3) PROJECT_TYPE="script" ;;
    *) PROJECT_TYPE="product" ;;
esac

echo ""

# ── Destination ───────────────────────────────────────────────────────────────
DEFAULT_DEST="$(dirname "$TEMPLATE_DIR")"
read -p "Where to create it? [${DEFAULT_DEST}]: " DEST_INPUT
DEST_PARENT="${DEST_INPUT:-$DEFAULT_DEST}"
DEST_PARENT="${DEST_PARENT/#\~/$HOME}"  # expand ~ if entered

TARGET_DIR="$DEST_PARENT/$PROJECT_NAME"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Name:        $PROJECT_NAME"
echo "  Type:        $PROJECT_TYPE"
echo "  Location:    $TARGET_DIR"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Create project? [Y/n]: " CONFIRM
if [[ "$CONFIRM" =~ ^[Nn] ]]; then
    echo "Cancelled."
    exit 0
fi

echo ""

# ── Run scaffold script ───────────────────────────────────────────────────────
bash "$TEMPLATE_DIR/scripts/new-project.sh" "$PROJECT_NAME" "$PROJECT_TYPE" "$DEST_PARENT"

# ── Open the new project's dashboard ─────────────────────────────────────────
NEW_START="$TARGET_DIR/Start.command"
if [ -f "$NEW_START" ]; then
    echo ""
    read -p "Open the new project dashboard now? [Y/n]: " OPEN_NOW
    if [[ ! "$OPEN_NOW" =~ ^[Nn] ]]; then
        open "$NEW_START"
    fi
fi

echo ""
echo "Done. Press Enter to close this window."
read
