#!/usr/bin/env bash
# Install Conductor for Claude Code globally (~/.claude)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
CONDUCTOR_EXT="$CLAUDE_HOME/extensions/conductor"

echo "==> Installing slash commands to $CLAUDE_HOME/commands/conductor/"
mkdir -p "$CLAUDE_HOME/commands/conductor"
cp "$REPO_ROOT/.claude/commands/conductor/"*.md "$CLAUDE_HOME/commands/conductor/"

echo "==> Installing Conductor templates..."
mkdir -p "$CONDUCTOR_EXT/templates"
rsync -a --delete "$REPO_ROOT/templates/" "$CONDUCTOR_EXT/templates/"

echo "==> Installing skills catalog..."
mkdir -p "$CONDUCTOR_EXT/skills"
cp "$REPO_ROOT/skills/catalog.md" "$CONDUCTOR_EXT/skills/catalog.md"

echo ""
echo "Conductor for Claude Code installed."
echo ""
echo "  Commands (in any project):"
echo "    /conductor:setup"
echo "    /conductor:newTrack"
echo "    /conductor:implement"
echo "    /conductor:status"
echo "    /conductor:revert"
echo "    /conductor:review"
echo ""
echo "  Extensions: $CONDUCTOR_EXT"
echo ""
echo "In a new project, run /conductor:setup once, then use the other commands."
