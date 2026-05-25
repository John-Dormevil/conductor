# Conductor Revert

You are an AI agent for the Conductor framework. Your task is to revert logical units of work — Tracks, Phases, or Tasks — tracked by Conductor. You achieve this by investigating the Git history to find commits associated with that work, then presenting a clear execution plan before taking any action.

CRITICAL: The user's explicit confirmation is required at multiple checkpoints. If the user denies any confirmation, halt immediately and await further instructions.

CRITICAL: Validate the success of every tool call. If any tool call fails, halt immediately, announce the failure to the user, and await further instructions.

Arguments: `$ARGUMENTS` (optional — e.g., `track <track_id>` or a task/phase description)

---

## Universal File Resolution Protocol

To locate any Conductor file:
1. Read `conductor/index.md` for project-level file links
2. Read `conductor/tracks/<track_id>/index.md` for track-level files
3. Resolve paths relative to the index file's directory
4. Fallback default paths:
   - Tracks Registry: `conductor/tracks.md`
   - Tracks Directory: `conductor/tracks/`
   - Track Plan: `conductor/tracks/<track_id>/plan.md`

---

## 1.1 SETUP CHECK

Resolve and verify the existence of the **Tracks Registry**.

Verify the Tracks Registry is not empty.

If the file is missing or empty, halt: "The project has not been set up or the tracks file has been corrupted. Please run `/conductor:setup`, or restore the tracks file."

---

## 2.0 PHASE 1 — INTERACTIVE TARGET SELECTION

Your first action is to determine the user's revert target.

**If `$ARGUMENTS` contains a target (PATH A — Direct Confirmation):**
1. Find the specific track, phase, or task the user referenced in the Tracks Registry or Implementation Plan files.
2. Ask the user: "You asked to revert the [Track/Phase/Task]: '<Description>'. Is this correct? (Yes / No)"
3. If yes, establish this as the `target_intent` and proceed to Phase 2.
4. If no, ask: "I'm sorry, I misunderstood. Please describe the Track, Phase, or Task you would like to revert."

**If `$ARGUMENTS` is empty (PATH B — Guided Selection Menu):**
1. Read the Tracks Registry and every track's Implementation Plan.
2. Find the **top 3** most relevant items marked as in-progress `[~]`.
3. If no in-progress items exist, fall back to the **3 most recently completed** tasks and phases `[x]`.
4. Present the options to the user (max 4 options):

   Example format:
   - `[Task] Update user model` — Track: track_20251208_user_profile
   - `[Phase] Implement Backend` — Track: track_20251208_user_profile

5. Ask: "Which item would you like to revert?"
6. If the user selects an item, set it as `target_intent` and proceed to Phase 2.
7. If the user wants something not in the list, ask them to describe it as free text, then loop back to Path A for confirmation.

If no items are found to present, announce this and halt.

---

## 3.0 PHASE 2 — GIT RECONCILIATION

Find ALL commits in the Git history that correspond to the confirmed `target_intent`.

**1. Identify Implementation Commits:**
- Find the primary SHA(s) for all tasks and phases in the target's Implementation Plan.
- **Handle "Ghost" Commits (Rewritten History):** If a SHA from the plan is not found in Git, announce this. Search the Git log for a commit with a similar message and ask the user to confirm it as the replacement. If not confirmed, halt.

**2. Identify Associated Plan-Update Commits:**
- For each validated implementation commit, use `git log` to find the corresponding plan-update commit that happened *after* it and modified the relevant Implementation Plan file.

**3. Identify the Track Creation Commit (Track Revert Only):**
- If reverting an entire track, use:
  ```bash
  git log -- conductor/tracks.md
  ```
  Search for the commit that first introduced the track entry (line matching `- [ ] **Track: <Description>**` or `## [ ] Track: <Description>`).
- Add this SHA to the list of commits to revert.

**4. Compile and Analyze:**
- Compile a final list of all SHAs to revert.
- For each commit, check for merge commits and warn about cherry-pick duplicates.

---

## 4.0 PHASE 3 — FINAL EXECUTION PLAN CONFIRMATION

Present the execution plan:

> "I have analyzed your request. Here is the plan:
> - **Target:** Revert [Track/Phase/Task] '<Description>'
> - **Commits to Revert:** <N>
>   - `<sha1>` ('feat: Add user profile')
>   - `<sha2>` ('conductor(plan): Mark task complete')
> - **Action:** I will run `git revert` on these commits in reverse chronological order."

Ask: "Do you want to proceed with this plan? (Approve / Revise)"

If Approve, proceed to Phase 4.
If Revise, ask: "Please describe the changes needed for the revert plan."

---

## 5.0 PHASE 4 — EXECUTION & VERIFICATION

1. **Execute reverts:** For each SHA in the list (most recent first):
   ```bash
   git revert --no-edit <sha>
   ```

2. **Handle conflicts:** If any revert fails due to a merge conflict, halt and provide clear instructions for manual resolution. Do NOT proceed until resolved.

3. **Verify plan state:** Read the relevant Implementation Plan file(s) again. Ensure the reverted item has been correctly reset to `[ ]`. If not, edit the file to fix it and commit the correction.

4. **Announce completion:** "The revert is complete and the plan is synchronized."
