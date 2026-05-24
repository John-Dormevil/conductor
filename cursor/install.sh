#!/usr/bin/env bash
# Install Conductor for Cursor globally (~/.cursor)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CURSOR_HOME="${CURSOR_HOME:-$HOME/.cursor}"
CONDUCTOR_HOME="$CURSOR_HOME/conductor"

echo "==> Generating commands from Gemini TOML sources..."
python3 "$REPO_ROOT/cursor/scripts/generate_commands.py"

echo "==> Installing slash commands to $CURSOR_HOME/commands/"
mkdir -p "$CURSOR_HOME/commands"
cp "$REPO_ROOT/cursor/generated/commands/"*.md "$CURSOR_HOME/commands/"

echo "==> Installing Conductor skill..."
mkdir -p "$CURSOR_HOME/skills/conductor"
cp "$REPO_ROOT/cursor/skills/conductor/SKILL.md" "$CURSOR_HOME/skills/conductor/"

echo "==> Installing Conductor home (templates + catalog)..."
mkdir -p "$CONDUCTOR_HOME/skills"
rsync -a --delete "$REPO_ROOT/templates/" "$CONDUCTOR_HOME/templates/"
cp "$REPO_ROOT/skills/catalog.md" "$CONDUCTOR_HOME/skills/catalog.md"
cp "$REPO_ROOT/cursor/conductor-home/CURSOR.md" "$CONDUCTOR_HOME/CURSOR.md"

echo ""
echo "Conductor for Cursor installed."
echo ""
echo "  Commands (in any project):"
echo "    /conductor-setup"
echo "    /conductor-new-track"
echo "    /conductor-implement"
echo "    /conductor-status"
echo "    /conductor-revert"
echo "    /conductor-review"
echo ""
echo "  Skill: @conductor or /conductor"
echo "  Home:  $CONDUCTOR_HOME"
echo ""
echo "In a new project, run /conductor-setup once, then use the other commands."
