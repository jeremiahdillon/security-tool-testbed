"""CodeRabbit adapter.

CodeRabbit reviews pull requests and posts prose comments; it has no machine-readable findings
export that maps cleanly to rule ids. Therefore CodeRabbit is scored **semi-manually**:

1. Run a round by opening PRs (see .github/workflows/land-case-prs.yml).
2. For each case, transcribe CodeRabbit's outcome into a small JSON file so the harness can
   score detection consistently. Shape:

     {"findings": [
        {"case_id": "sast-js-sqli-001", "detected": true,
         "type": "sql-injection", "file": "cases/sast/js/taskflow/routes/tasks.js",
         "line": 42, "summary_matched": true, "note": "flagged concatenated query"}
     ]}

   `summary_matched` records whether CodeRabbit's PR summary matched the case's
   `expected_summary` — this is how explainability is graded (see results/TEMPLATE.md).

If no such file exists yet, this adapter returns nothing and the round's report will show
CodeRabbit as "not scored" rather than "missed".
"""
from __future__ import annotations

import json

from .common import Finding, read_text


def parse(path: str, tool: str = "coderabbit") -> list[Finding]:
    data = json.loads(read_text(path))
    findings: list[Finding] = []
    for f in data.get("findings", []):
        if not f.get("detected", True):
            continue
        finding = Finding(
            tool=tool,
            rule=f.get("type", ""),
            file=f.get("file"),
            line=f.get("line"),
            message=f.get("note", ""),
            extra={
                "case_id": f.get("case_id"),
                "summary_matched": f.get("summary_matched"),
            },
        )
        findings.append(finding)
    return findings
