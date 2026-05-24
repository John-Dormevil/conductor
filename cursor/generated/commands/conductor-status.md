---
description: "Displays the current progress of the project"
---

# Conductor — Displays the current progress of the project

> **Cursor global command.** Artifacts live in `conductor/` in the current project. Templates: `~/.cursor/conductor/templates/`.

## Runtime (Cursor)

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


## Universal File Resolution Protocol

# Universal File Resolution Protocol

**PROTOCOL: How to locate files.**

To find a file (e.g., "**Product Definition**") within Project Root or a Track:

1. **Identify Index:**
   - **Project Context:** `conductor/index.md`
   - **Track Context:** Read **Tracks Registry** → follow link to track folder → `<track_folder>/index.md`
   - **Fallback:** `<Tracks Directory>/<track_id>/index.md`

2. **Check Index:** Read the index and find a matching link label.

3. **Resolve Path:** Resolve relative to the directory containing that `index.md`.

4. **Fallback:** Use default paths below if index missing.

5. **Verify:** Confirm the file exists.

**Default paths (project):**

- **Product Definition**: `conductor/product.md`
- **Tech Stack**: `conductor/tech-stack.md`
- **Workflow**: `conductor/workflow.md`
- **Product Guidelines**: `conductor/product-guidelines.md`
- **Tracks Registry**: `conductor/tracks.md`
- **Tracks Directory**: `conductor/tracks/`

**Default paths (track):**

- **Specification**: `conductor/tracks/<track_id>/spec.md`
- **Implementation Plan**: `conductor/tracks/<track_id>/plan.md`
- **Metadata**: `conductor/tracks/<track_id>/metadata.json`


---


## 1.0 SYSTEM DIRECTIVE
You are an AI agent. Your primary function is to provide a status overview of the current tracks file. This involves reading the **Tracks Registry** file, parsing its content, and summarizing the progress of tasks.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---


## 1.1 SETUP CHECK
**PROTOCOL: Verify that the Conductor environment is properly set up.**

1.  **Verify Core Context:** Using the **Universal File Resolution Protocol**, resolve and verify the existence of:
    -   **Tracks Registry**
    -   **Product Definition**
    -   **Tech Stack**
    -   **Workflow**

2.  **Handle Failure:**
    -   If ANY of these files are missing, you MUST halt the operation immediately.
    -   Announce: "Conductor is not set up. Please run `/conductor-setup` to set up the environment."
    -   Do NOT proceed to Status Overview Protocol.

---

## 2.0 STATUS OVERVIEW PROTOCOL
**PROTOCOL: Follow this sequence to provide a status overview.**

### 2.1 Read Project Plan
1.  **Locate and Read:** Read the content of the **Tracks Registry** (resolved via **Universal File Resolution Protocol**).
2.  **Locate and Read Tracks:**
    -   Parse the **Tracks Registry** to identify all registered tracks and their paths.
        *   **Parsing Logic:** When reading the **Tracks Registry** to identify tracks, look for lines matching either the new standard format `- [ ] **Track:` or the legacy format `## [ ] Track:`.
    -   For each track, resolve and read its **Implementation Plan** (using **Universal File Resolution Protocol** via the track's index file).

### 2.2 Parse and Summarize Plan
1.  **Parse Content:**
    -   Identify major project phases/sections (e.g., top-level markdown headings).
    -   Identify individual tasks and their current status (e.g., bullet points under headings, looking for keywords like "COMPLETED", "IN PROGRESS", "PENDING").
2.  **Generate Summary:** Create a concise summary of the project's overall progress. This should include:
    -   The total number of major phases.
    -   The total number of tasks.
    -   The number of tasks completed, in progress, and pending.

### 2.3 Present Status Overview
1.  **Output Summary:** Present the generated summary to the user in a clear, readable format. The status report must include:
    -   **Current Date/Time:** The current timestamp.
    -   **Project Status:** A high-level summary of progress (e.g., "On Track", "Behind Schedule", "Blocked").
    -   **Current Phase and Task:** The specific phase and task currently marked as "IN PROGRESS".
    -   **Next Action Needed:** The next task listed as "PENDING".
    -   **Blockers:** Any items explicitly marked as blockers in the plan.
    -   **Phases (total):** The total number of major phases.
    -   **Tasks (total):** The total number of tasks.
    -   **Progress:** The overall progress of the plan, presented as tasks_completed/tasks_total (percentage_completed%).


