# Conductor for Claude Code

Port of [Gemini CLI Conductor](https://github.com/gemini-cli-extensions/conductor) to Claude Code slash commands.

## Background

Conductor originally shipped only as a Gemini CLI extension. This port exists because Claude Code
users were asking for the same spec-driven workflow (`setup` → `newTrack` → `implement` → `status` →
`revert` → `review`) that Gemini CLI users already had. The six Markdown commands under
`.claude/commands/conductor/` reproduce the same protocol as the Gemini `.toml` commands — see the
"Key differences" section in the root `CLAUDE.md` for what had to change (no Plan Mode equivalent,
inline questions instead of `ask_user`, etc.). `install.sh` makes the port usable globally without
cloning this repo into every project.

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
