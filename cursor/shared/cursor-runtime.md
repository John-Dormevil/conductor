# Conductor on Cursor — runtime

You are running **Conductor for Cursor** (global install). The workflow matches Gemini Conductor: context → spec & plan → implement.

## Tool mapping (Gemini → Cursor)

| Gemini | Cursor |
|--------|--------|
| `ask_user` | `AskQuestion` — batch questions in one call when possible |
| `write_file` | `Write` |
| `replace` | `StrReplace` |
| `run_shell_command` | `Shell` |
| `enter_plan_mode` | Ask the user to enable **Plan mode** in Cursor (or use `SwitchMode` with `target_mode_id: plan` if available). Explain that only `conductor/**` files should be created/edited during scaffolding. |
| `exit_plan_mode` | Ask the user to return to **Agent mode** when scaffolding is done (or `SwitchMode` → `agent`). |

## Paths (global install)

| Resource | Path |
|----------|------|
| Conductor home (templates, catalog) | `~/.cursor/conductor/` |
| Code style templates | `~/.cursor/conductor/templates/code_styleguides/` |
| Workflow template | `~/.cursor/conductor/templates/workflow.md` |
| Skills catalog | `~/.cursor/conductor/skills/catalog.md` |
| Global Cursor skills (optional installs) | `~/.cursor/skills/<skill-name>/` |
| Project Cursor skills | `.cursor/skills/<skill-name>/` |
| Project artifacts (always in repo) | `conductor/` at project root |

## Plan mode on Cursor

When the protocol says **Plan Mode**:

1. Prefer **Plan mode** for creating/editing only under `conductor/`.
2. Use **relative paths** only (e.g. `conductor/product.md`), never absolute paths for those files.
3. Do **not** use shell redirection (`>`, `>>`) to write files — use `Write` / `StrReplace`.
4. Allowed shell prefixes during setup: `git status`, `git diff`, `ls`, `mkdir`, `cp`, `git init`, `git add`, `git commit`.

## Ignore files

Respect `.cursorignore` and `.gitignore` when scanning the codebase (same role as `.geminiignore` on Gemini).

## Slash commands

| Gemini | Cursor (type `/` in chat) |
|--------|---------------------------|
| `/conductor:setup` | `/conductor-setup` |
| `/conductor:newTrack` | `/conductor-new-track` |
| `/conductor:implement` | `/conductor-implement` |
| `/conductor:status` | `/conductor-status` |
| `/conductor:revert` | `/conductor-revert` |
| `/conductor:review` | `/conductor-review` |

## Skills after install

Cursor loads skills from `~/.cursor/skills/` automatically. **No `/skills reload`** — tell the user new skills are available on the next message after install.

## User arguments

If the prompt references command arguments: use text the user typed **after** the slash command in chat. If empty, ask via `AskQuestion` or a short chat question.

## Commits

Only create git commits when the user explicitly asks, except where this protocol explicitly requires a Conductor setup/track commit message.
