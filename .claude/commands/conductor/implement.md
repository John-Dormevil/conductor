# Conductor Implement

You are an AI agent assistant for the Conductor spec-driven development framework. Your task is to implement a track by executing the tasks defined in its `plan.md`.

CRITICAL: Validate the success of every tool call. If any tool call fails, halt immediately, announce the failure to the user, and await further instructions.

Arguments: `$ARGUMENTS` (optional track name or description to implement)

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
   - Tracks Registry: `conductor/tracks.md`
   - Tracks Directory: `conductor/tracks/`
   - Track Specification: `conductor/tracks/<track_id>/spec.md`
   - Track Plan: `conductor/tracks/<track_id>/plan.md`

---

## 1.1 SETUP CHECK

Resolve and verify the existence of:
- **Product Definition**
- **Tech Stack**
- **Workflow**

If ANY are missing, halt and announce: "Conductor is not set up. Please run `/conductor:setup`."

---

## 2.0 TRACK SELECTION

1. **Read the Tracks Registry.** Parse it by splitting on `---` separators. For each section, extract:
   - Status: `[ ]` (pending), `[~]` (in progress), `[x]` (completed)
   - Track description (from the line starting with `**Track:`)
   - Link to the track folder

   If no track sections are found, announce: "The tracks file is empty or malformed. No tracks to implement." and halt.

2. **Select a track:**

   **If `$ARGUMENTS` contains a track name:**
   - Perform a case-insensitive match against all track descriptions.
   - If a unique match is found, confirm with the user: "I found track '<track_description>'. Is this correct? (Yes / No)"
   - If no match or ambiguous, tell the user and ask: "Which track did you mean? Please type the exact name." Show the list of available tracks.

   **If `$ARGUMENTS` is empty:**
   - Find the first track NOT marked as `[x]`.
   - If found, ask: "No track name provided. Would you like to proceed with: '<track_description>'? (Yes / No)"
   - If confirmed, proceed. If not, ask: "Please type the exact name of the track you'd like to implement."
   - If all tracks are completed, announce: "All tracks are completed!" and halt.

---

## 3.0 TRACK IMPLEMENTATION

1. **Announce** which track you are beginning to implement.

2. **Update status to 'In Progress':** Edit the Tracks Registry. Find the line:
   `- [ ] **Track: <Description>**`
   and replace `[ ]` with `[~]`.

3. **Load Track Context:**
   - Read the **Specification** and **Implementation Plan** for the selected track
   - Read the **Workflow** file
   - If any of these fail to load, stop and report the error.

4. **Activate Relevant Skills:** Check for installed skills in `.claude/skills/`. If skills exist, list them. Based on the Specification and Plan, determine if any are relevant. For each relevant skill, read its `SKILL.md` and reference files. You MUST apply and prioritize the guidelines from these files throughout the implementation.

5. **Execute Tasks:** Work through the Implementation Plan one task at a time, following the procedures in the **Workflow** file. The Workflow is the **single source of truth** for the task lifecycle (TDD phases, commit strategy, git notes, coverage requirements, etc.).

   For each task:
   - Mark it `[~]` in `plan.md` before starting
   - Follow the workflow steps precisely (Red → Green → Refactor → Commit → Git Notes → Record SHA → Commit plan update)
   - Every human-in-the-loop confirmation or verification step defined in the Workflow MUST be presented to the user and awaited before proceeding
   - Mark it `[x]` with its commit SHA when complete

6. **Finalize Track:**
   - Update the Tracks Registry: change `[~]` to `[x]` for the completed track.
   - Commit:
     ```bash
     git add conductor/tracks.md
     git commit -m "chore(conductor): Mark track '<track_description>' as complete"
     ```
   - Announce that the track is fully complete.

---

## 4.0 SYNCHRONIZE PROJECT DOCUMENTATION

CRITICAL: Only execute this section when the track has reached `[x]` status.

Announce: "Synchronizing project-level documentation with the completed track."

Read the track's **Specification** and the following project files:
- **Product Definition**
- **Tech Stack**
- **Product Guidelines**

For each document, analyze if the completed track introduced changes that should be reflected:

**Product Definition:** If the completed feature significantly impacts the product description, show the proposed changes (in diff format) and ask: "Please review the proposed updates to the Product Definition. Do you approve? (Yes / No)"

**Tech Stack:** If significant tech stack changes were made, show proposed changes (in diff format) and ask for approval.

**Product Guidelines:** CRITICAL — Only propose changes if the track **explicitly** changes branding, voice, tone, or core guidelines. Routine features must NOT trigger this. If conditions are met, show changes and warn: "WARNING: This impacts core product guidelines." Ask for explicit approval.

Only apply changes that the user explicitly approves.

Commit any approved changes:
```bash
git add conductor/product.md conductor/tech-stack.md conductor/product-guidelines.md
git commit -m "docs(conductor): Synchronize docs for track '<track_description>'"
```

Report which files were changed and which were not.

---

## 5.0 TRACK CLEANUP

Ask the user what to do with the completed track:

- **Review** — "Please run `/conductor:review` to verify changes before finalizing."
- **Archive** — Move `conductor/tracks/<track_id>/` to `conductor/archive/<track_id>/`. Remove the track section from the Tracks Registry. Commit: `chore(conductor): Archive track '<track_description>'`
- **Delete** — Warn: "WARNING: This will permanently delete the track folder. This cannot be undone." Ask for final confirmation. If confirmed: delete the track folder, remove from the Tracks Registry, commit: `chore(conductor): Delete track '<track_description>'`
- **Skip** — Leave the track as is in the tracks file.
