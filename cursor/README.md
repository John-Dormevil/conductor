# Conductor for Cursor

Port of [Gemini CLI Conductor](https://github.com/gemini-cli-extensions/conductor) to Cursor slash commands and global skills.

## Install (global, all projects)

```bash
./cursor/install.sh
```

This installs to `~/.cursor/`:

| Path | Content |
|------|---------|
| `~/.cursor/commands/conductor-*.md` | 6 slash commands |
| `~/.cursor/skills/conductor/SKILL.md` | Methodology + file resolution |
| `~/.cursor/conductor/templates/` | Workflow + code styleguides |
| `~/.cursor/conductor/skills/catalog.md` | Optional skill recommendations |

## Usage

1. Open any project in Cursor.
2. Run **`/conductor-setup`** once → creates `conductor/` in the repo.
3. Then: `/conductor-new-track`, `/conductor-implement`, `/conductor-status`, `/conductor-revert`, `/conductor-review`.

You can also type **`@conductor`** for context or say "run conductor setup".

## Regenerate after upstream changes

Generated files land in `cursor/generated/commands/` (not committed; `dist/` is gitignored).

Edit `commands/conductor/*.toml` in this repo, then:

```bash
./cursor/install.sh
```

## Gemini → Cursor mapping

See `cursor/shared/cursor-runtime.md`.
