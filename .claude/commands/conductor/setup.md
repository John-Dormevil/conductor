# Conductor Setup

You are an AI agent assistant for the Conductor spec-driven development framework. Your task is to initialize a project. Follow this protocol precisely and sequentially.

CRITICAL: Validate the success of every tool call. If any tool call fails, halt immediately, announce the failure to the user, and await further instructions.

---

## Universal File Resolution Protocol

To locate any Conductor file:
1. Read `conductor/index.md` for project-level file links
2. Resolve paths relative to `conductor/`
3. Fallback default paths if index is missing:
   - Product Definition: `conductor/product.md`
   - Tech Stack: `conductor/tech-stack.md`
   - Workflow: `conductor/workflow.md`
   - Product Guidelines: `conductor/product-guidelines.md`
   - Tracks Registry: `conductor/tracks.md`
   - Tracks Directory: `conductor/tracks/`

---

## 1.1 PRE-INITIALIZATION OVERVIEW

Present this overview to the user:

> "Welcome to Conductor. I will guide you through the following steps to set up your project:
> 1. **Project Discovery:** Analyze the current directory to determine if this is a new or existing project.
> 2. **Product Definition:** Collaboratively define the product's vision, design guidelines, and technology stack.
> 3. **Configuration:** Select appropriate code style guides and customize your development workflow.
> 4. **Track Generation:** Define the initial track and automatically generate a detailed plan.
>
> Let's get started!"

---

## 1.2 PROJECT AUDIT

Announce you are auditing the project for existing Conductor configuration.

Check for the existence of these in `conductor/`:
- `product.md`
- `product-guidelines.md`
- `tech-stack.md`
- `code_styleguides/`
- `workflow.md`
- `index.md`
- `tracks/*/` (specifically `plan.md` and `index.md`)

Map the state to a target section (highest match wins):

| Artifact Exists | Target Section | Announcement |
| :--- | :--- | :--- |
| All files in `tracks/<track_id>/` (`spec`, `plan`, `metadata`, `index`) | **HALT** | "The project is already initialized. Use `/conductor:newTrack` or `/conductor:implement`." |
| `index.md` (top-level) | **Section 3.0** | "Resuming setup: Scaffolding is complete. Next: generate the first track." |
| `workflow.md` | **Section 2.6** | "Resuming setup: Workflow is defined. Next: select Agent Skills." |
| `code_styleguides/` | **Section 2.5** | "Resuming setup: Guides/Tech Stack configured. Next: define project workflow." |
| `tech-stack.md` | **Section 2.4** | "Resuming setup: Tech Stack defined. Next: select Code Styleguides." |
| `product-guidelines.md` | **Section 2.3** | "Resuming setup: Guidelines are complete. Next: define the Technology Stack." |
| `product.md` | **Section 2.2** | "Resuming setup: Product Guide is complete. Next: create Product Guidelines." |
| (None) | **Section 2.0** | (None) |

Keep the target section in mind and proceed to Section 2.0 first.

---

## 2.0 PROJECT INCEPTION

**Detect Project Maturity:** Classify as Brownfield (Existing) or Greenfield (New).

Brownfield indicators:
- Dependency manifests: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Source code directories: `src/`, `app/`, `lib/`, `bin/` containing code files
- Run `git status --porcelain`. Ignore changes in `conductor/`. Uncommitted changes elsewhere suggest Brownfield.
- If ANY primary indicator is found → Brownfield.

Greenfield condition: ONLY if none of the above are found, ignoring `conductor/`, a clean `.git`, and `README.md`.

**If the target section from 1.2 is not Section 2.0:** announce the project maturity briefly (stating the specific indicator found), then immediately jump to that target section.

**If Brownfield (and target is Section 2.0):**
- Announce detection with the specific indicator (e.g., "I found a `package.json` file").
- If uncommitted changes exist outside `conductor/`, warn: "WARNING: You have uncommitted changes. Please commit or stash before proceeding."
- Ask the user for permission to perform a read-only scan to analyze the project.
- If denied, halt and await instructions.
- If granted: analyze `README.md` first, then manifest files, then directory structure (top 2 levels). Respect `.gitignore` / `.gitignore` patterns. For files over 1MB, read only the first and last 20 lines.
- Extract: Programming Language, Frameworks, Database Drivers, Architecture type, Project Goal.
- Proceed to Section 2.1.

**If Greenfield (and target is Section 2.0):**
- Announce new project initialization.
- If `.git` does not exist, run `git init` and report it.
- Ask the user: "What do you want to build?"
- Upon receiving the answer: run `mkdir -p conductor` then create `conductor/product.md` with the user's response under `# Initial Concept`.
- Proceed to Section 2.1.

---

## 2.1 GENERATE PRODUCT GUIDE (Interactive)

Announce you are creating `product.md`.

Ask the user how they'd like to define product details:
- **Interactive** — Guide through questions about target users, goals, and features
- **Autogenerate** — Draft a comprehensive guide based on the initial project goal

If **Interactive**: Ask up to 4 batched questions in one turn. For Brownfield, formulate context-aware questions based on the codebase analysis. Provide 3 high-quality suggested answers per question where possible.

If **Autogenerate**: Use your best judgment to expand on the initial concept.

Draft the document, then show it to the user and ask: "Does this accurately capture the product? (Approve / Suggest changes)". Iterate until approved.

Once approved, append the content to `conductor/product.md`, preserving any existing `# Initial Concept` section.

---

## 2.2 GENERATE PRODUCT GUIDELINES (Interactive)

Announce you are creating `product-guidelines.md`.

Ask the user:
- **Interactive** — Ask about prose style, branding, and UX principles (up to 4 batched questions, 3 suggestions each)
- **Autogenerate** — Draft standard guidelines based on best practices. For Brownfield, match the established style found in the codebase.

Draft the document, show it to the user, and iterate until approved.

Write the approved content to `conductor/product-guidelines.md`.

---

## 2.3 GENERATE TECH STACK (Interactive)

Announce you are defining the technology stack.

**For Greenfield:** Ask the user:
- **Interactive** — Ask about language, frameworks, and database (up to 4 batched questions, grouped by concern: language / backend framework / frontend framework / database). Allow multi-select for hybrid stacks.
- **Autogenerate** — Recommend a standard stack based on the project goal.

**For Brownfield:**
- CRITICAL: Your goal is to document the *existing* stack, not propose changes.
- State the inferred tech stack in the chat.
- Ask the user: "Is the inferred tech stack listed above correct? (Yes / No)"
- If No: ask the user to provide the correct stack as free text.

Draft the document, show it to the user, and iterate until approved.

Write the approved content to `conductor/tech-stack.md`.

---

## 2.4 SELECT CODE STYLE GUIDES (Interactive)

Announce you are selecting code style guides.

List available guides. Try these paths in order using Bash:
```bash
ls ~/.claude/extensions/conductor/templates/code_styleguides/ 2>/dev/null \
  || ls templates/code_styleguides/ 2>/dev/null
```

**For Greenfield:** Based on the tech stack, recommend the most appropriate guide(s) and explain why. Ask:
- **Recommended** — Use the suggested guides
- **Select from Library** — Present guides in batches of 3–4, multi-select per batch

**For Brownfield:** Announce the inferred guides and ask: "Proceed with these guides or Add More?"

Run:
```bash
mkdir -p conductor/code_styleguides
cp <source_path>/<selected_guide>.md conductor/code_styleguides/
```

---

## 2.5 SELECT WORKFLOW (Interactive)

Copy the workflow template:
```bash
cp ~/.claude/extensions/conductor/templates/workflow.md conductor/workflow.md 2>/dev/null \
  || cp templates/workflow.md conductor/workflow.md
```

Ask the user:
- **Default** — Use the standard workflow (>80% test coverage, per-task commits)
- **Customize** — Adjust settings

If **Customize**, ask about (batch in one turn):
1. Test coverage percentage (default: 80%)
2. Commit frequency: Per Task or Per Phase
3. Summary storage: Git Notes or Commit Messages

Show the resulting configuration and ask: "Anything else to change? (Leave blank to finish)"

Update `conductor/workflow.md` based on all user choices.

---

## 2.6 SELECT SKILLS (Interactive)

Read the skills catalog from:
1. `~/.claude/extensions/conductor/skills/catalog.md`
2. `skills/catalog.md` (fallback — this repo)

If catalog not found, announce "Skills catalog not found. Skipping skill selection." and jump to Section 2.7.

Detect applicable skills based on detection signals (dependencies and keywords) matched against project files and `conductor/tech-stack.md`.

If no recommended skills: announce this and skip to Section 2.7.

If skills found, present them and ask:
- **Install All** — Install all recommended skills
- **Hand-pick** — User selects from the list
- **Skip** — No installation

For each selected skill:
1. Determine installation path: `.claude/skills/<skill-name>/` (project-scoped)
2. Create the directory: `mkdir -p .claude/skills/<skill-name>/`
3. Download the skill folder content from the URL in the catalog (use `git clone` or `git sparse-checkout` for Git URLs)

If new skills were installed, tell the user: "New skills installed in `.claude/skills/`. They will be available in this and future sessions."

---

## 2.7 FINALIZATION

Create `conductor/index.md` with this exact content:
```markdown
# Project Context

## Definition
- [Product Definition](./product.md)
- [Product Guidelines](./product-guidelines.md)
- [Tech Stack](./tech-stack.md)

## Workflow
- [Workflow](./workflow.md)
- [Code Style Guides](./code_styleguides/)

## Management
- [Tracks Registry](./tracks.md)
- [Tracks Directory](./tracks/)
```

Present a summary of all actions taken (files created, guides copied, workflow configured).

Announce: "Initial setup is complete. Now let's define the first track for your project."

---

## 3.0 INITIAL PLAN AND TRACK GENERATION

**Pre-Requisite (Cleanup):** If resuming after an interrupted setup and `conductor/tracks/` exists but is incomplete, delete it entirely before proceeding to ensure a clean state.

### 3.1 GENERATE PRODUCT REQUIREMENTS (Greenfield only — skip for Brownfield)

Read `conductor/product.md`.

Ask the user:
- **Interactive** — Guide through user stories and functional/non-functional requirements (up to 4 batched questions, 3 suggestions each)
- **Autogenerate** — Draft requirements based on the Product Guide

Show the draft and iterate until approved. Retain the approved requirements in context.

### 3.2 PROPOSE A SINGLE INITIAL TRACK

Announce you will propose an initial track to get the project started.

Analyze `conductor/product.md`, `conductor/tech-stack.md`, and any gathered requirements. Generate a single track title:
- **Greenfield**: Focus on MVP core (e.g., "Build core calculator functionality")
- **Brownfield**: Focus on targeted enhancement (e.g., "Implement user authentication flow")

Ask: "To get started, I suggest the following track: '<Track Title>'. Proceed with this? (Yes / Suggest changes)"

If the user wants changes, ask them to provide the description as free text.

### 3.3 CREATE TRACK ARTIFACTS

Once the track description is confirmed:

1. **Generate a Track ID** using the format `shortname_YYYYMMDD`. Store it — use this exact ID for all subsequent steps.

2. **Create `conductor/tracks.md`:**
```markdown
# Project Tracks

This file tracks all major tracks for the project. Each track has its own detailed plan in its respective folder.

---

- [ ] **Track: <Track Description>**
  *Link: [./tracks/<track_id>/](./tracks/<track_id>/)*
```

3. **Create directory:** `mkdir -p conductor/tracks/<track_id>/`

4. **Auto-generate `spec.md`** covering: Overview, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Out of Scope.

5. **Auto-generate `plan.md`** following the workflow in `conductor/workflow.md`:
   - Structure: Phases → Tasks → Sub-tasks
   - Status markers on EVERY task and sub-task: `[ ]`
   - Parent task format: `- [ ] Task: ...`
   - Sub-task format: `    - [ ] ...`
   - CRITICAL: If a "Phase Completion Verification and Checkpointing Protocol" is defined in `conductor/workflow.md`, append a final meta-task to each Phase: `- [ ] Task: Conductor - User Manual Verification '<Phase Name>' (Protocol in workflow.md)`

6. **Create `conductor/tracks/<track_id>/metadata.json`:**
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

7. **Create `conductor/tracks/<track_id>/index.md`:**
```markdown
# Track <track_id> Context

- [Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Metadata](./metadata.json)
```

### 3.4 FINAL ANNOUNCEMENT

Commit all conductor files:
```bash
git add conductor/
git commit -m "conductor(setup): Add conductor setup files"
```

Announce: "Setup complete! Your project is ready. Run `/conductor:implement` to begin implementation."
