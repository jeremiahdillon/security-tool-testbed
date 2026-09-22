#!/usr/bin/env python3
"""Real-secret leak guard.

Purpose: prove the repo never leaks a REAL secret, while still allowing the intentional FAKE
secrets that the testbed plants. It does two things:

1. Location check (portable, runs in CI): scan every git-tracked file for high-signal provider
   credential patterns. Matches are only allowed inside the planted directories
   (`cases/`, `scoring/fixtures/`). A match anywhere else — docs, scoring code, CI config,
   a stray committed dotfile — fails the build. This is what catches an accidental real leak.

2. Collision check (best-effort, local only): confirm none of the planted fake values happens
   to equal a real secret present in this machine's secret stores (~/.aws, ~/.ssh, env, ...).
   Only match/no-match is reported; real secret contents are never printed. Skipped silently
   where those stores don't exist (e.g. CI).

Exit 0 = clean, 1 = a real-leak violation.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Directories where planted (fake) secrets are expected and allowed.
ALLOWED_PREFIXES = ("cases/", "scoring/fixtures/")

# High-signal provider credential patterns. Kept deliberately specific to avoid false alarms;
# the goal is catching a real key committed to the wrong place, not exhaustive secret scanning
# (that's the job of the tools under test).
PATTERNS = {
    "aws-access-key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "stripe-secret": re.compile(r"sk_live_[0-9a-zA-Z]{16,}"),
    "openai": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "anthropic": re.compile(r"sk-ant-[A-Za-z0-9\-_]{20,}"),
    "openrouter": re.compile(r"sk-or-v1-[0-9a-f]{32,}"),
    "github-pat": re.compile(r"gh[pousr]_[0-9A-Za-z]{36,}"),
    "slack-token": re.compile(r"xox[baprs]-[0-9A-Za-z-]{10,}"),
    "google-api-key": re.compile(r"AIza[0-9A-Za-z_\-]{35}"),
    "twilio-sid": re.compile(r"AC[0-9a-fA-F]{32}"),
    "twilio-apikey": re.compile(r"SK[0-9a-fA-F]{32}"),
    "private-key-block": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA |)?PRIVATE KEY-----"),
    "azure-accountkey": re.compile(r"AccountKey=[A-Za-z0-9+/=]{20,}"),
}

# Filenames that should never be committed to this repo (they'd carry real creds).
BAD_FILENAMES = re.compile(
    r"(^|/)(\.env(\..+)?|\.netrc|id_rsa|id_ed25519|id_dsa|.*\.pem|.*\.p12|.*\.pfx|"
    r"credentials|\.npmrc)$",
    re.IGNORECASE,
)
# Files that are allowed to match BAD_FILENAMES for legitimate reasons.
FILENAME_ALLOWLIST = {".npmrc"}  # repo root .npmrc is our ignore-scripts guard, not a credential


def tracked_files() -> list[str]:
    out = subprocess.run(
        ["git", "ls-files"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout
    return [line for line in out.splitlines() if line]


def location_check(files: list[str]) -> list[str]:
    errors: list[str] = []
    for rel in files:
        if BAD_FILENAMES.search(rel) and rel not in FILENAME_ALLOWLIST:
            errors.append(f"credential-style filename committed: {rel}")
        allowed = rel.startswith(ALLOWED_PREFIXES)
        path = REPO / rel
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, pat in PATTERNS.items():
            if pat.search(text) and not allowed:
                errors.append(
                    f"secret pattern '{name}' found OUTSIDE planted dirs: {rel} "
                    f"(planted secrets are only allowed under {', '.join(ALLOWED_PREFIXES)})"
                )
    return errors


def collision_check() -> tuple[int, int]:
    """Return (checked, collisions). Best-effort; local only."""
    stores = [
        Path.home() / p
        for p in (
            ".aws", ".ssh", ".config", ".netrc", ".npmrc", ".docker", ".gitconfig",
            "Library/Application Support/gcloud",
        )
    ]
    stores = [s for s in stores if s.exists()]
    if not stores:
        return (0, 0)
    # Extract key-like tokens from planted files.
    tokens: set[str] = set()
    for rel in tracked_files():
        if not rel.startswith(ALLOWED_PREFIXES):
            continue
        text = (REPO / rel).read_text(encoding="utf-8", errors="ignore")
        for tok in re.findall(r"[A-Za-z0-9_\-/+=]{20,}", text):
            if re.search(r"[0-9]", tok) and re.search(r"[A-Za-z]", tok):
                tokens.add(tok)
    collisions = 0
    for tok in tokens:
        # env
        if any(tok in v for v in os.environ.values()):
            print(f"  COLLISION: {tok[:5]}... appears in an environment variable")
            collisions += 1
            continue
        for store in stores:
            hit = subprocess.run(
                ["grep", "-rqIF", "--", tok, str(store)], capture_output=True
            )
            if hit.returncode == 0:
                print(f"  COLLISION: {tok[:5]}... appears under {store}")
                collisions += 1
                break
    return (len(tokens), collisions)


def main() -> int:
    files = tracked_files()
    errors = location_check(files)

    checked, collisions = collision_check()
    if collisions:
        errors.append(
            f"{collisions} planted value(s) collide with a REAL secret on this machine"
        )

    if errors:
        print("Leak check FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1

    msg = "Leak check passed: all secret patterns are inside planted dirs; no bad filenames."
    if checked:
        msg += f" Collision check: {checked} planted tokens, 0 real collisions."
    else:
        msg += " (collision check skipped — no local secret stores present)"
    print(msg)
    return 0


if __name__ == "__main__":
    sys.exit(main())
