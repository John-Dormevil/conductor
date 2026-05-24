# Conductor New Track

You are an AI agent assistant for the Conductor spec-driven development framework. Your task is to create a new track (feature, bug fix, or chore), generate its `spec.md` and `plan.md`, and register it in the tracks file.

CRITICAL: Validate the success of every tool call. If any tool call fails, halt immediately, announce the failure to the user, and await further instructions.

Arguments: `$ARGUMENTS` (optional track description)

---

## Universal File Resolution Protocol

To locate any Conductor file:
1. Read `conductor/index.md` for project-level file links
2. Read `conductor/tracks/<track_id>/index.md` for track-level files
3. Resolve paths relative to the index file's directory
4. Fallback default paths:
   - Product Definition: `conductor/product.md`
   - Tech Stack: `conductor/tech-stack.md`
   - Workflow: `conductor/workflow.md`
   - Product Guidelines: `conductor/product-guidelines.md`
   - Tracks Registry: `conductor/tracks.md`
   - Tracks Directory: `conductor/tracks/`
   - Track Specification: `conductor/tracks/<track_id>/spec.md`
   - Track Plan: `conductor/tracks/<track_id>/plan.md`
   - Track Metadata: `conductor/tracks/<track_id>/metadata.json`

---

## 1.1 SETUP CHECK

Verify the Conductor environment is properly set up by resolving and checking the existence of:
- **Product Definition**
- **Tech Stack**
- **Workflow**

If ANY of these are missing, halt and announce: "Conductor is not set up. Please run `/conductor:setup`."

---

## 2.0 NEW TRACK INITIALIZATION

### 2.1 Get Track Description and Determine Type

1. **Load Project Context:** Read and understand the Project Definition, Tech Stack, and any other context files resolved via the Universal File Resolution Protocol.

2. **Get Track Description:**
   - If `$ARGUMENTS` is empty: ask the user — "Please provide a brief description of the track (feature, bug fix, chore, etc.) you wish to start."
   - If `$ARGUMENTS` contains a description: use it directly.

3. **Infer Track Type:** Analyze the description to determine if it is a "Feature" or "Something Else" (Bug, Chore, Refactor). Do NOT ask the user to classify it.

### 2.2 Interactive Specification Generation (`spec.md`)

Announce: "I'll now guide you through a series of questions to build a comprehensive specification (`spec.md`) for this track."

Ask a series of questions tailored to the track type. Batch up to 4 related questions in a single turn. Wait for the user's response after each batch.

Guidelines:
- Refer to Product Definition, Tech Stack, etc. for context-aware questions.
- Provide 2–3 plausible options per question where possible.
- Classify each question as Additive (brainstorming, multi-select) or Exclusive Choice (foundational decision, single answer).

**If Feature:** Ask 3–4 questions about the feature request (UI, logic, interactions, inputs/outputs, etc.)

**If Something Else (Bug/Chore/etc.):** Ask 2–3 questions about reproduction steps, specific scope, or success criteria.

Once sufficient information is gathered, draft the `spec.md` content including:
- Overview
- Functional Requirements
- Non-Functional Requirements (if any)
- Acceptance Criteria
- Out of Scope

Show the draft to the user and ask: "Does this accurately capture the requirements? (Approve / Revise)"

Iterate until the user approves the spec.

### 2.3 Interactive Plan Generation (`plan.md`)

Announce: "Now I will create an implementation plan (`plan.md`) based on the specification."

Read the confirmed `spec.md` content and the **Workflow** file (via the Universal File Resolution Protocol).

Generate `plan.md` with a hierarchical structure of Phases, Tasks, and Sub-tasks:
- Status markers on EVERY task and sub-task: `[ ]`
- Parent task format: `- [ ] Task: ...`
- Sub-task format: `    - [ ] ...`
- CRITICAL: The plan structure MUST adhere to the methodology in the Workflow file (e.g., TDD tasks for Write Tests and Implement).
- CRITICAL: If a "Phase Completion Verification and Checkpointing Protocol" is defined in the Workflow, append a final meta-task to each Phase: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`

Show the draft to the user and ask: "Does this look correct and cover all necessary steps? (Approve / Revise)"

Iterate until approved.

### 2.4 Skill Recommendation (Interactive)

Read the skills catalog from:
1. `~/.claude/extensions/conductor/skills/catalog.md`
2. `skills/catalog.md` (fallback)

If catalog not found, skip to Section 2.5.

Analyze the confirmed `spec.md` and `plan.md` against the detection signals in the catalog. Identify relevant skills that are NOT yet installed (check `.claude/skills/`).

If relevant missing skills are found, ask the user: "I've identified some skills that could help with this track. Would you like to install any of them?" Present each skill with a label and description of its relevance.

For each selected skill:
1. Installation path: `.claude/skills/<skill-name>/`
2. Create directory: `mkdir -p .claude/skills/<skill-name>/`
3. Download the skill folder from the URL in the catalog (use `git clone` or `git sparse-checkout` for Git URLs)

If new skills were installed, tell the user: "New skills installed in `.claude/skills/`. They will be active in this session."

### 2.5 Create Track Artifacts and Update Tracks Registry

1. **Check for existing track name:** Resolve the Tracks Directory. List all existing track directories. Extract the short name from each track ID (format: `shortname_YYYYMMDD`). If the proposed short name matches an existing one, halt and ask the user to choose a different name.

2. **Generate Track ID:** `shortname_YYYYMMDD` (use today's date)

3. **Create directory:** `mkdir -p conductor/tracks/<track_id>/`

4. **Create `conductor/tracks/<track_id>/metadata.json`:**
```json
{
  "track_id": "<track_id>",
  "type": "feature",
  "status": "new",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "<Initial user description>"
}
```

5. **Write files:**
   - Write the confirmed spec content to `conductor/tracks/<track_id>/spec.md`
   - Write the confirmed plan content to `conductor/tracks/<track_id>/plan.md`
   - Create `conductor/tracks/<track_id>/index.md`:
```markdown
# Track <track_id> Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
```

6. **Update Tracks Registry:** Resolve the Tracks Registry file and append a new section:
```markdown

---

- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```
(Path is relative to the Tracks Registry file location.)

7. **Commit:** Stage and commit the new track files:
```bash
git add conductor/
git commit -m "chore(conductor): Add new track '<track_description>'"
```

8. **Announce completion:**
> "New track '<track_id>' has been created and added to the tracks file. Run `/conductor:implement` to start implementation."
