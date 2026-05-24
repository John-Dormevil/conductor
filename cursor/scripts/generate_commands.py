#!/usr/bin/env python3
"""Generate Cursor slash commands from Gemini Conductor TOML prompts."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "commands" / "conductor"
SHARED = ROOT / "cursor" / "shared"
OUT = ROOT / "cursor" / "generated" / "commands"

COMMAND_MAP = {
    "setup.toml": ("conductor-setup.md", "setup"),
    "newTrack.toml": ("conductor-new-track.md", "newTrack"),
    "implement.toml": ("conductor-implement.md", "implement"),
    "status.toml": ("conductor-status.md", "status"),
    "revert.toml": ("conductor-revert.md", "revert"),
    "review.toml": ("conductor-review.md", "review"),
}

PLAN_MODE_CURSOR = """**CURSOR PLAN MODE:** For steps that require Plan Mode, ask the user to enable **Plan mode** in Cursor (or use SwitchMode → plan). You may create and edit only under `conductor/` using relative paths. Use `Write` and `StrReplace` — not shell redirection. Allowed shell: `git status`, `git diff`, `ls`, `mkdir`, `cp`, `git init`, `git add`, `git commit`."""

REPLACEMENTS: list[tuple[str, str]] = [
    ("/conductor:setup", "/conductor-setup"),
    ("/conductor:newTrack", "/conductor-new-track"),
    ("/conductor:implement", "/conductor-implement"),
    ("/conductor:status", "/conductor-status"),
    ("/conductor:revert", "/conductor-revert"),
    ("/conductor:review", "/conductor-review"),
    ("`/conductor:setup`", "`/conductor-setup`"),
    ("`/conductor:newTrack`", "`/conductor-new-track`"),
    ("`/conductor:implement`", "`/conductor-implement`"),
    ("`/conductor:status`", "`/conductor-status`"),
    ("`/conductor:revert`", "`/conductor-revert`"),
    ("`/conductor:review`", "`/conductor-review`"),
    ("`ask_user`", "`AskQuestion`"),
    ("ask_user tool", "AskQuestion tool"),
    ("the ask_user tool", "the AskQuestion tool"),
    ("`write_file`", "`Write`"),
    ("`replace`", "`StrReplace`"),
    ("`run_shell_command`", "`Shell`"),
    ("~/.gemini/extensions/conductor/", "~/.cursor/conductor/"),
    (".geminiignore", ".cursorignore"),
    ("~/.agents/extensions/conductor/skills/", "~/.cursor/skills/"),
    (".agents/skills/", ".cursor/skills/"),
    ("Please run `/skills reload`", "New skills are in `~/.cursor/skills/` or `.cursor/skills/` — Cursor loads them automatically"),
    ("run `/skills reload`", "reload is not needed on Cursor"),
    ("`{{args}}`", "text the user provided after the slash command (if none, ask)"),
]


def extract_toml_fields(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    desc_m = re.search(r'^description\s*=\s*"(.*)"\s*$', text, re.MULTILINE)
    prompt_m = re.search(r'prompt\s*=\s*"""(.*)"""\s*$', text, re.DOTALL)
    if not prompt_m:
        raise ValueError(f"No prompt found in {path}")
    description = desc_m.group(1) if desc_m else path.stem
    return description, prompt_m.group(1)


def adapt_prompt(body: str) -> str:
    body = re.sub(
        r"PLAN MODE PROTOCOL:.*?(?=\n---|\n## )",
        PLAN_MODE_CURSOR + "\n",
        body,
        flags=re.DOTALL,
    )
    body = re.sub(
        r"\*\*Enter Plan Mode:\*\* Call the `enter_plan_mode` tool[^\n]*\n",
        "**Enter Plan Mode:** Ask the user to enable Plan mode in Cursor (or SwitchMode → plan).\n",
        body,
    )
    body = re.sub(
        r"Call the `enter_plan_mode` tool[^\n]*\n",
        "Ask the user to enable Plan mode in Cursor (or SwitchMode → plan).\n",
        body,
    )
    body = re.sub(
        r"\*\*Exit Plan Mode:\*\* Call the `exit_plan_mode` tool[^\n]*\n",
        "**Exit Plan Mode:** Ask the user to return to Agent mode when done.\n",
        body,
    )
    body = re.sub(
        r"Call the `exit_plan_mode` tool[^\n]*\n",
        "Ask the user to return to Agent mode when scaffolding is complete.\n",
        body,
    )
    for old, new in REPLACEMENTS:
        body = body.replace(old, new)
    return body


def build_command(description: str, body: str) -> str:
    runtime = (SHARED / "cursor-runtime.md").read_text(encoding="utf-8")
    ufrp = (SHARED / "universal-file-resolution.md").read_text(encoding="utf-8")
    desc_escaped = description.replace('"', '\\"')
    return f"""---
description: "{desc_escaped}"
---

# Conductor — {description}

> **Cursor global command.** Artifacts live in `conductor/` in the current project. Templates: `~/.cursor/conductor/templates/`.

## Runtime (Cursor)

{runtime}

## Universal File Resolution Protocol

{ufrp}

---

{adapt_prompt(body)}
"""


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for src_name, (out_name, _) in COMMAND_MAP.items():
        src_path = SRC / src_name
        if not src_path.exists():
            print(f"Missing {src_path}", file=sys.stderr)
            return 1
        description, body = extract_toml_fields(src_path)
        out_path = OUT / out_name
        out_path.write_text(build_command(description, body), encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
