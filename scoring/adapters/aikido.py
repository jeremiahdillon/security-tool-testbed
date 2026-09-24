"""Aikido adapter (semi-manual).

Aikido's free tier (as evaluated here) exposes findings only through the dashboard UI / a PDF
export, not a machine-readable SARIF/JSON download. So Aikido is transcribed semi-manually from
the dashboard into a small JSON file, with each finding mapped to a **canonical taxonomy type**
so the harness matches it directly (rule == type). Shape:

  {"findings": [
     {"type": "command-injection", "file": "cases/sast/js/taskflow/routes/attachments.js"},
     {"type": "vulnerable-dependency", "package": "lodash",
      "file": "cases/dependencies/js/package.json"}
  ]}

`line` is optional (the dashboard groups by file, not line); when omitted the harness matches on
file alone for SAST/secret/IaC, and on package name for dependency findings. If Aikido ever
offers a SARIF export, prefer the sarif adapter with `--tool aikido` instead.
"""
from __future__ import annotations

import json

from .common import Finding, read_text


def parse(path: str, tool: str = "aikido") -> list[Finding]:
    data = json.loads(read_text(path))
    findings: list[Finding] = []
    for f in data.get("findings", []):
        findings.append(
            Finding(
                tool=tool,
                rule=f.get("type", ""),          # already a canonical taxonomy type
                file=f.get("file"),
                line=f.get("line"),
                package=f.get("package"),
                message=f.get("note", ""),
            )
        )
    return findings
