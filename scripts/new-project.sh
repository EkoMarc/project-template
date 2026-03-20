#!/bin/bash
# new-project.sh — Scaffold a new project from this template
#
# Usage: ./scripts/new-project.sh <project-name> <type>
# Types: planning | prototype | script | product
#
# Creates a new project folder at the same level as this template.

set -e

# ── Args ──────────────────────────────────────────────────────────────────────
PROJECT_NAME="${1:-}"
PROJECT_TYPE="${2:-product}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./scripts/new-project.sh <project-name> <type>"
    echo "Types: planning | prototype | script | product"
    exit 1
fi

TEMPLATE_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="$(dirname "$TEMPLATE_DIR")/$PROJECT_NAME"

if [ -d "$TARGET_DIR" ]; then
    echo "Error: $TARGET_DIR already exists."
    exit 1
fi

echo "Creating $PROJECT_TYPE project: $PROJECT_NAME"
mkdir -p "$TARGET_DIR"

# ── Always-included files ─────────────────────────────────────────────────────
copy_file() { cp "$TEMPLATE_DIR/$1" "$TARGET_DIR/$1"; }
copy_dir()  { cp -r "$TEMPLATE_DIR/$1" "$TARGET_DIR/$1"; }

# Root files
cp "$TEMPLATE_DIR/CLAUDE.md"      "$TARGET_DIR/CLAUDE.md"
cp "$TEMPLATE_DIR/AGENTS.md"      "$TARGET_DIR/AGENTS.md"
cp "$TEMPLATE_DIR/README.md"      "$TARGET_DIR/README.md"
cp "$TEMPLATE_DIR/Start.command"  "$TARGET_DIR/Start.command"
cp "$TEMPLATE_DIR/start.sh"       "$TARGET_DIR/start.sh"

# Always: overview, tasks, context, scripts/README, dashboard, setup
mkdir -p "$TARGET_DIR/docs"
mkdir -p "$TARGET_DIR/scripts"
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
        cp "$TEMPLATE_DIR/docs/decisions.md"        "$TARGET_DIR/docs/decisions.md"
        cp "$TEMPLATE_DIR/docs/stack.md"            "$TARGET_DIR/docs/stack.md"
        cp "$TEMPLATE_DIR/.env.example"             "$TARGET_DIR/.env.example"
        cp "$TEMPLATE_DIR/scripts/containerize.sh"  "$TARGET_DIR/scripts/containerize.sh"
        mkdir -p "$TARGET_DIR/src"
        ;;
    product)
        cp "$TEMPLATE_DIR/docs/decisions.md"        "$TARGET_DIR/docs/decisions.md"
        cp "$TEMPLATE_DIR/docs/stack.md"            "$TARGET_DIR/docs/stack.md"
        cp "$TEMPLATE_DIR/docs/workflows.md"        "$TARGET_DIR/docs/workflows.md"
        cp "$TEMPLATE_DIR/.env.example"             "$TARGET_DIR/.env.example"
        cp "$TEMPLATE_DIR/scripts/containerize.sh"  "$TARGET_DIR/scripts/containerize.sh"
        mkdir -p "$TARGET_DIR/src"
        ;;
    *)
        echo "Unknown type: $PROJECT_TYPE. Using product defaults."
        ;;
esac

# ── Pre-fill project name ─────────────────────────────────────────────────────
DISPLAY_NAME=$(echo "$PROJECT_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) substr($i,2)} 1')

sed -i.bak "s/\[Project Name\]/$DISPLAY_NAME/g" "$TARGET_DIR/AGENTS.md" && rm "$TARGET_DIR/AGENTS.md.bak"
sed -i.bak "s/\[Project Name\]/$DISPLAY_NAME/g" "$TARGET_DIR/README.md" && rm "$TARGET_DIR/README.md.bak"
sed -i.bak "s/\[Project Name\]/$DISPLAY_NAME/g" "$TARGET_DIR/docs/overview.md" && rm "$TARGET_DIR/docs/overview.md.bak"

# Fill type in AGENTS.md
sed -i.bak "s/\[planning | prototype | script | product\]/$PROJECT_TYPE/" "$TARGET_DIR/AGENTS.md" && rm "$TARGET_DIR/AGENTS.md.bak"

# ── Make scripts executable ───────────────────────────────────────────────────
chmod +x "$TARGET_DIR/Start.command" "$TARGET_DIR/start.sh" "$TARGET_DIR/scripts/"*.sh 2>/dev/null || true

# ── Init git ──────────────────────────────────────────────────────────────────
cd "$TARGET_DIR"
if command -v git &> /dev/null; then
    git init --quiet
    # Create .gitignore
    cat > .gitignore << 'EOF'
.env
__pycache__/
*.pyc
node_modules/
.DS_Store
EOF
    git add -A
    git commit -m "init: scaffold $PROJECT_TYPE project from template" --quiet
    echo "✓ Git repository initialized"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo "✓ Project created: $TARGET_DIR"
echo ""
echo "Next steps:"
echo "  1. cd $TARGET_DIR"
echo "  2. ./scripts/setup.sh          (first-time setup)"
echo "  3. Double-click Start.command  (open dashboard)"
echo "  4. Fill in docs/context.md     (define your problem)"
