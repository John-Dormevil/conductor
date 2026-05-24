# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

Conductor is a **spec-driven development framework** available as both a Gemini CLI extension and a set of Claude Code slash commands. It is not a runnable application — there is no build step, no package manager, and no test suite. The repo is composed of TOML/Markdown command definitions, Markdown templates, and configuration files that the respective AI CLI tools load and execute.

## Repository Structure

```
commands/conductor/          # Six TOML command definitions for Gemini CLI
.claude/commands/conductor/  # Six Markdown command definitions for Claude Code
templates/
  workflow.md                # Default workflow template copied into user projects on setup
  code_styleguides/          # Per-language style guides copied into user projects on setup
skills/catalog.md            # Registry of installable agent skills with detection signals
policies/conductor.toml      # Gemini CLI security policies permitting Plan Mode file writes
GEMINI.md                    # Context file auto-loaded by Gemini CLI; defines the Universal File Resolution Protocol
gemini-extension.json        # Gemini CLI extension manifest
```

## Commands

This repo ships commands for **two AI CLIs**. The logic is identical; only the format differs.

### Gemini CLI (`commands/conductor/`)

Each file is a TOML with `description` and `prompt` fields. The prompt is the full protocol the agent executes.

| File | Command |
|------|---------|
| `setup.toml` | `/conductor:setup` |
| `newTrack.toml` | `/conductor:newTrack` |
| `implement.toml` | `/conductor:implement` |
| `status.toml` | `/conductor:status` |
| `revert.toml` | `/conductor:revert` |
| `review.toml` | `/conductor:review` |

### Claude Code (`.claude/commands/conductor/`)

Each file is a Markdown file whose content is the prompt given to Claude Code. Files in `.claude/commands/conductor/` are accessible as `/conductor:<name>`.

| File | Command | Purpose |
|------|---------|---------|
| `setup.md` | `/conductor:setup` | One-time project initialization; creates `conductor/` artifacts |
| `newTrack.md` | `/conductor:newTrack` | Generates `spec.md` + `plan.md` for a new feature/bug track |
| `implement.md` | `/conductor:implement` | Executes tasks from the active track's `plan.md` |
| `status.md` | `/conductor:status` | Parses all track plans and reports progress |
| `revert.md` | `/conductor:revert` | Git-aware revert targeting tracks, phases, or tasks |
| `review.md` | `/conductor:review` | Code review against guidelines and the active plan |

**Key differences between Gemini CLI and Claude Code versions:**
- Gemini CLI uses native tools (`ask_user`, `enter_plan_mode`, `write_file`); Claude Code uses its built-in tools (`Bash`, `Write`, `Edit`, `Read`) and asks questions inline.
- Gemini CLI Plan Mode is replaced by direct file creation in Claude Code (no equivalent gating mechanism).
- Skills install to `.claude/skills/<skill-name>/` instead of `.agents/skills/<skill-name>/`.
- `{{args}}` in TOML prompts becomes `$ARGUMENTS` in Markdown prompts.

## Key Concepts

**Universal File Resolution Protocol** (defined in `GEMINI.md`): All commands locate project files via `conductor/index.md` and track files via `conductor/tracks/<track_id>/index.md` rather than hardcoded paths. Fallback default paths exist if index files are absent.

**Tracks**: A track is a unit of work (feature, bug, chore). Each track lives in `conductor/tracks/<track_id>/` and contains `spec.md`, `plan.md`, `metadata.json`, and `index.md`. Track status is mirrored in `conductor/tracks.md` (the Tracks Registry) using `[ ]`, `[~]`, `[x]` markers.

**Plan Mode (Gemini CLI only)**: `setup.toml` and `newTrack.toml` use Gemini CLI's `enter_plan_mode`/`exit_plan_mode` tools to create files. The policy in `policies/conductor.toml` allows `write_file`, `replace`, and specific shell commands during Plan Mode for paths under `conductor/`. Claude Code has no equivalent — files are created directly.

**Skills**: Agent skills are knowledge documents (a `SKILL.md` and references) downloaded to a local directory. The agent reads them during implementation for domain-specific guidance. In Gemini CLI: `.agents/skills/<skill-name>/` (project) or `~/.agents/extensions/conductor/skills/<skill-name>/` (global). In Claude Code: `.claude/skills/<skill-name>/`. `skills/catalog.md` lists available skills with detection signals used by `setup` and `newTrack` to recommend relevant ones.

**Workflow Template**: `templates/workflow.md` is the canonical TDD workflow template. It defines the per-task lifecycle (Red → Green → Refactor → Commit → Git Notes), phase checkpoint protocol, quality gates, and commit message format. It is copied to `conductor/workflow.md` in user projects and may be customized.

## Artifacts Generated in User Projects

`/conductor:setup` creates:
- `conductor/index.md` — project context index (root of the resolution protocol)
- `conductor/product.md`, `product-guidelines.md`, `tech-stack.md`, `workflow.md`
- `conductor/code_styleguides/` — copies of selected style guides from `templates/`
- `conductor/tracks.md` — Tracks Registry

`/conductor:newTrack` creates per-track:
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/metadata.json`
- `conductor/tracks/<track_id>/index.md`

## Releases

Releases are managed by `release-please` (config in `release-please-config.json`, manifest in `.release-please-manifest.json`). The CI workflow is in `.github/workflows/release-please.yml`. To release, merge to `main`; release-please opens a release PR automatically.

## Making Changes

- **Gemini CLI command behavior**: edit the `prompt` field in the corresponding `.toml` under `commands/conductor/`.
- **Claude Code command behavior**: edit the corresponding `.md` file under `.claude/commands/conductor/`.
- **Both CLIs share the same logic** — changes to one should generally be mirrored to the other.
- **Default workflow template**: edit `templates/workflow.md`.
- **Code style guides**: add/edit `.md` files in `templates/code_styleguides/`.
- **Skills catalog**: add entries to `skills/catalog.md` following the existing format (name, description, URL, party, detection signals).
- **Gemini CLI Plan Mode permissions**: edit `policies/conductor.toml`.
- **Universal File Resolution Protocol**: defined in `GEMINI.md` (auto-loaded by Gemini CLI) and embedded directly in each `.claude/commands/conductor/*.md` file (since Claude Code has no separate auto-loaded extension context).
