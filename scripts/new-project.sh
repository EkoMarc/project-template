#!/bin/bash
# new-project.sh — Scaffold a new project from this template
#
# Usage: ./scripts/new-project.sh <project-name> <type> [destination]
# Types:  planning | prototype | script | product
# Dest:   optional path where the project folder is created
#         (default: same folder as this template)
#
# Examples:
#   ./scripts/new-project.sh my-app product
#   ./scripts/new-project.sh my-app product ~/Projects

set -e

PROJECT_NAME="${1:-}"
PROJECT_TYPE="${2:-product}"
DEST_PARENT="${3:-}"

TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ -z "$DEST_PARENT" ]; then
    DEST_PARENT="$(dirname "$TEMPLATE_DIR")"
fi

# Default name: "new-project", incrementing to "new-project-2" etc. if exists
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME="new-project"
    if [ -d "$DEST_PARENT/$PROJECT_NAME" ]; then
        n=2
        while [ -d "$DEST_PARENT/new-project-$n" ]; do
            n=$((n + 1))
        done
        PROJECT_NAME="new-project-$n"
    fi
fi

TARGET_DIR="$DEST_PARENT/$PROJECT_NAME"

if [ -d "$TARGET_DIR" ]; then
    echo "Error: $TARGET_DIR already exists. Choose a different name."
    exit 1
fi

echo "Creating $PROJECT_TYPE project: $TARGET_DIR"
mkdir -p "$TARGET_DIR/docs" "$TARGET_DIR/scripts"

# ── Always-included files ─────────────────────────────────────────────────────
cp "$TEMPLATE_DIR/CLAUDE.md"            "$TARGET_DIR/CLAUDE.md"
cp "$TEMPLATE_DIR/AGENTS.md"            "$TARGET_DIR/AGENTS.md"
cp "$TEMPLATE_DIR/README.md"            "$TARGET_DIR/README.md"
cp "$TEMPLATE_DIR/Start.command"        "$TARGET_DIR/Start.command"
cp "$TEMPLATE_DIR/start.sh"             "$TARGET_DIR/start.sh"
cp "$TEMPLATE_DIR/docs/overview.md"     "$TARGET_DIR/docs/overview.md"
cp "$TEMPLATE_DIR/docs/tasks.md"        "$TARGET_DIR/docs/tasks.md"
cp "$TEMPLATE_DIR/docs/context.md"      "$TARGET_DIR/docs/context.md"
cp "$TEMPLATE_DIR/scripts/README.md"    "$TARGET_DIR/scripts/README.md"
cp "$TEMPLATE_DIR/scripts/dashboard.py" "$TARGET_DIR/scripts/dashboard.py"
cp "$TEMPLATE_DIR/scripts/setup.sh"     "$TARGET_DIR/scripts/setup.sh"

# ── Type-specific files ───────────────────────────────────────────────────────
case "$PROJECT_TYPE" in
    planning)
        cp "$TEMPLATE_DIR/docs/workflows.md" "$TARGET_DIR/docs/workflows.md"
        ;;
    prototype)
        cp "$TEMPLATE_DIR/docs/decisions.md" "$TARGET_DIR/docs/decisions.md"
        cp "$TEMPLATE_DIR/docs/stack.md"     "$TARGET_DIR/docs/stack.md"
        cp "$TEMPLATE_DIR/.env.example"      "$TARGET_DIR/.env.example"
        mkdir -p "$TARGET_DIR/sandbox"
        ;;
    script)
        cp "$TEMPLATE_DIR/docs/decisions.md"       "$TARGET_DIR/docs/decisions.md"
        cp "$TEMPLATE_DIR/docs/stack.md"           "$TARGET_DIR/docs/stack.md"
        cp "$TEMPLATE_DIR/.env.example"            "$TARGET_DIR/.env.example"
        cp "$TEMPLATE_DIR/scripts/containerize.sh" "$TARGET_DIR/scripts/containerize.sh"
        mkdir -p "$TARGET_DIR/src"
        ;;
    product)
        cp "$TEMPLATE_DIR/docs/decisions.md"       "$TARGET_DIR/docs/decisions.md"
        cp "$TEMPLATE_DIR/docs/stack.md"           "$TARGET_DIR/docs/stack.md"
        cp "$TEMPLATE_DIR/docs/workflows.md"       "$TARGET_DIR/docs/workflows.md"
        cp "$TEMPLATE_DIR/.env.example"            "$TARGET_DIR/.env.example"
        cp "$TEMPLATE_DIR/scripts/containerize.sh" "$TARGET_DIR/scripts/containerize.sh"
        mkdir -p "$TARGET_DIR/src"
        ;;
    *)
        echo "Unknown type '$PROJECT_TYPE' — using product defaults."
        ;;
esac

# ── Pre-fill project name and type (portable sed) ─────────────────────────────
DISPLAY_NAME=$(echo "$PROJECT_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')

fill() {
    # Portable in-place sed: works on macOS and Linux
    sed -i.bak "$1" "$2" && rm "$2.bak"
}

fill "s/\[Project Name\]/$DISPLAY_NAME/g" "$TARGET_DIR/AGENTS.md"
fill "s/\[Project Name\]/$DISPLAY_NAME/g" "$TARGET_DIR/README.md"
fill "s/\[Project Name\]/$DISPLAY_NAME/g" "$TARGET_DIR/docs/overview.md"
fill "s/\[planning | prototype | script | product\]/$PROJECT_TYPE/" "$TARGET_DIR/AGENTS.md"

# ── .gitignore ────────────────────────────────────────────────────────────────
cat > "$TARGET_DIR/.gitignore" << 'EOF'
.env
__pycache__/
*.pyc
node_modules/
.DS_Store
.claude/worktrees/
.claude/settings.local.json
EOF

# ── Make scripts executable ───────────────────────────────────────────────────
chmod +x "$TARGET_DIR/Start.command" "$TARGET_DIR/start.sh" "$TARGET_DIR/scripts/"*.sh 2>/dev/null || true

# ── Init git ──────────────────────────────────────────────────────────────────
cd "$TARGET_DIR"
if command -v git &> /dev/null; then
    git init --quiet
    git add -A
    git commit -m "init: scaffold $PROJECT_TYPE project from template" --quiet
    echo "✓ Git initialized"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "✓ Created: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. Double-click Start.command  — open dashboard"
echo "  2. Fill in docs/context.md     — define your problem"
echo "  3. Open Claude Code:  cd $TARGET_DIR && claude"
