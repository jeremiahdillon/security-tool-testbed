"""Endor Labs adapter.

Endor covers SCA (with reachability), SAST, secrets, and CI posture. Its CLI can emit JSON;
export the findings list and point the harness at it. This adapter reads a generic findings
array; adjust field names in docs/tools/endor.md to match your `endorctl` output.

Expected-ish shape:
  {"findings": [
     {"category": "SQL_INJECTION", "cwe": "CWE-89", "severity": "HIGH",
      "file_path": "cases/sast/js/taskflow/routes/tasks.js", "line_number": 42,
      "reachable": true, "description": "..."}
  ]}
"""
from __future__ import annotations

import json

from .common import Finding, read_text


def parse(path: str, tool: str = "endor") -> list[Finding]:
    data = json.loads(read_text(path))
    items = data.get("findings") or data.get("results") or []
    findings: list[Finding] = []
    for f in items:
        findings.append(
            Finding(
                tool=tool,
                rule=f.get("category") or f.get("finding_category") or f.get("rule", ""),
                cwe=f.get("cwe"),
                file=f.get("file_path") or f.get("file"),
                line=f.get("line_number") or f.get("line"),
                severity=f.get("severity"),
                message=f.get("description", "") or f.get("summary", ""),
                package=f.get("dependency") or f.get("package"),
                extra={"reachable": f.get("reachable")},
            )
        )
    return findings
