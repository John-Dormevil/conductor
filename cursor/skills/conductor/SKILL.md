---
name: conductor
description: >-
  Context-driven development with Conductor (spec, plan, tracks, implement).
  Use when the user says "conductor", context-driven development, tracks, or
  conductor/ artifacts. Points to slash commands and file resolution protocol.
---

# Conductor (Cursor)

## Slash commands

| Command | Purpose |
|---------|---------|
| `/conductor-setup` | Once per project: product, stack, workflow, first track |
| `/conductor-new-track` | New feature/bug track → `spec.md` + `plan.md` |
| `/conductor-implement` | Execute current track's `plan.md` |
| `/conductor-status` | Progress overview |
| `/conductor-revert` | Git-aware revert by track/phase/task |
| `/conductor-review` | Review against guidelines and plan |

## Artifacts (in each project)

```
conductor/
  product.md
  product-guidelines.md
  tech-stack.md
  workflow.md
  code_styleguides/
  tracks.md
  tracks/<track_id>/{spec,plan,metadata,index}.md
```

## Universal File Resolution Protocol

1. Project index: `conductor/index.md`
2. Track index: link from `conductor/tracks.md` → `conductor/tracks/<id>/index.md`
3. Defaults: `conductor/product.md`, `tech-stack.md`, `workflow.md`, `tracks.md`, `tracks/<id>/spec.md`, `plan.md`

## Templates (global)

Copy from `~/.cursor/conductor/templates/` during setup (not from Gemini paths).

## Full runtime rules

When executing a Conductor command, follow the command body plus `~/.cursor/conductor/` layout. Tool mapping: `AskQuestion`, `Write`, `StrReplace`, `Shell`.
