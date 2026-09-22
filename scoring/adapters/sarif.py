"""SARIF v2.1.0 adapter.

Covers any tool that exports SARIF: CodeQL, SonarCloud (SARIF export), Semgrep, and many
others. Pass the tool key so findings are attributed correctly (e.g. --tool codeql).
"""
from __future__ import annotations

import json
import re

from .common import Finding, read_text

_CWE_RE = re.compile(r"CWE[-_ ]?(\d+)", re.IGNORECASE)


def _extract_cwe(*texts: str) -> str | None:
    for t in texts:
        if not t:
            continue
        m = _CWE_RE.search(t)
        if m:
            return f"CWE-{m.group(1)}"
    return None


def parse(path: str, tool: str = "sarif") -> list[Finding]:
    data = json.loads(read_text(path))
    findings: list[Finding] = []
    for run in data.get("runs", []):
        # Build ruleId -> rule metadata (for CWE tags / names).
        rules_meta: dict[str, dict] = {}
        driver = run.get("tool", {}).get("driver", {})
        for rule in driver.get("rules", []) or []:
            rules_meta[rule.get("id", "")] = rule
        tool_name = tool if tool != "sarif" else driver.get("name", "sarif").lower()

        for res in run.get("results", []):
            rule_id = res.get("ruleId", "")
            meta = rules_meta.get(rule_id, {})
            tags = " ".join(meta.get("properties", {}).get("tags", []) or [])
            cwe = _extract_cwe(
                rule_id,
                tags,
                json.dumps(meta.get("properties", {})),
                res.get("message", {}).get("text", ""),
            )
            loc_file = loc_line = None
            locs = res.get("locations", []) or []
            if locs:
                phys = locs[0].get("physicalLocation", {})
                loc_file = phys.get("artifactLocation", {}).get("uri")
                loc_line = phys.get("region", {}).get("startLine")
            findings.append(
                Finding(
                    tool=tool_name,
                    rule=rule_id,
                    cwe=cwe,
                    file=loc_file,
                    line=loc_line,
                    severity=res.get("level") or meta.get("defaultConfiguration", {}).get("level"),
                    message=res.get("message", {}).get("text", ""),
                )
            )
    return findings
