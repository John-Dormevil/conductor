# Conductor for Claude Code

Port of [Gemini CLI Conductor](https://github.com/gemini-cli-extensions/conductor) to Claude Code slash commands.

## Install (global, all projects)

```bash
./claude/install.sh
```

This installs to `~/.claude/`:

| Path | Content |
|------|---------|
| `~/.claude/commands/conductor/` | 6 slash commands |
| `~/.claude/extensions/conductor/templates/` | Workflow + code styleguides |
| `~/.claude/extensions/conductor/skills/catalog.md` | Optional skill recommendations |

## Usage

1. Open any project in Claude Code.
2. Run **`/conductor:setup`** once → creates `conductor/` in the repo.
3. Then: `/conductor:newTrack`, `/conductor:implement`, `/conductor:status`, `/conductor:revert`, `/conductor:review`.

## Reinstall after upstream changes

```bash
./claude/install.sh
```

## Gemini → Claude Code mapping

| Gemini CLI | Claude Code |
|------------|-------------|
| `commands/conductor/*.toml` | `.claude/commands/conductor/*.md` |
| `enter_plan_mode` / `exit_plan_mode` | Direct file creation (no equivalent) |
| `ask_user` | Inline questions in conversation |
| `.agents/skills/<name>/` | `.claude/skills/<name>/` |
| `~/.agents/extensions/conductor/` | `~/.claude/extensions/conductor/` |
