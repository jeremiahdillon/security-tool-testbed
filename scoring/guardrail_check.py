#!/usr/bin/env python3
"""Repo guardrail checks (used by pre-commit and CI).

Two independent checks, both cheap and dependency-free:

1. DO-NOT block sync: the text between the `<!-- DO-NOT:BEGIN -->` and `<!-- DO-NOT:END -->`
   markers must be byte-for-byte identical across every agent-instruction file and the
   canonical source of truth in docs/safety.md.
2. No install artifacts: lockfiles / installed-dependency directories must never be committed,
   because their presence means someone installed dependencies in this testbed.

Exit code 0 = clean, 1 = a violation was found.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CANONICAL = REPO / "docs" / "safety.md"
MIRRORS = [
    REPO / "CLAUDE.md",
    REPO / "AGENTS.md",
    REPO / ".cursor" / "rules" / "testbed.mdc",
    REPO / ".github" / "copilot-instructions.md",
]

BLOCK_RE = re.compile(r"<!-- DO-NOT:BEGIN -->\n(.*?)\n<!-- DO-NOT:END -->", re.DOTALL)

# Files whose mere presence indicates an install happened.
FORBIDDEN_ARTIFACTS = {
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "poetry.lock",
    "Pipfile.lock",
}
FORBIDDEN_DIRS = {"node_modules", "__pycache__", ".venv", "venv", "target"}


def extract_block(path: Path) -> str | None:
    if not path.exists():
        return None
    m = BLOCK_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def check_sync() -> list[str]:
    errors: list[str] = []
    canonical = extract_block(CANONICAL)
    if canonical is None:
        return [f"{CANONICAL.relative_to(REPO)}: missing DO-NOT block (source of truth)"]
    for mirror in MIRRORS:
        block = extract_block(mirror)
        rel = mirror.relative_to(REPO)
        if block is None:
            errors.append(f"{rel}: missing DO-NOT block")
        elif block != canonical:
            errors.append(f"{rel}: DO-NOT block drifted from docs/safety.md")
    return errors


def check_artifacts() -> list[str]:
    errors: list[str] = []
    for path in REPO.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.name in FORBIDDEN_ARTIFACTS:
            errors.append(f"forbidden install artifact committed: {path.relative_to(REPO)}")
        if path.is_dir() and path.name in FORBIDDEN_DIRS:
            errors.append(f"forbidden install directory present: {path.relative_to(REPO)}/")
    return errors


def main() -> int:
    errors = check_sync() + check_artifacts()
    if errors:
        print("Guardrail check FAILED:")
        for e in errors:
            print(f"  - {e}")
        print("\nSee docs/safety.md. Do not install/build/run; keep the DO-NOT block in sync.")
        return 1
    print("Guardrail check passed: DO-NOT blocks in sync, no install artifacts.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
