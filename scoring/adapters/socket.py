"""Socket adapter (dependency + supply-chain findings).

Socket's export shapes vary by surface (GitHub App, CLI `socket report`, API). This adapter is
deliberately permissive: it walks a JSON document for objects that look like alerts and maps
their `type` to canonical taxonomy keys via the taxonomy alias table.

Expected-ish shape (adjust in docs/tools/socket.md to match your export):
  {"alerts": [
     {"type": "malware", "package": "left-pad-cli", "severity": "critical",
      "file": "cases/supply-chain/package.json", "description": "..."}
  ]}
"""
from __future__ import annotations

import json

from .common import Finding, read_text

# Socket alert types that indicate supply-chain risk vs known CVEs.
_MALICIOUS = {"malware", "typosquat", "installScripts", "install-scripts", "suspicious", "obfuscatedCode"}
_VULN = {"cve", "known-vulnerability", "vulnerability"}


def _iter_alerts(node):
    if isinstance(node, dict):
        if "type" in node and ("package" in node or "pkg" in node or "purl" in node):
            yield node
        for v in node.values():
            yield from _iter_alerts(v)
    elif isinstance(node, list):
        for v in node:
            yield from _iter_alerts(v)


def parse(path: str, tool: str = "socket") -> list[Finding]:
    data = json.loads(read_text(path))
    findings: list[Finding] = []
    for a in _iter_alerts(data):
        atype = str(a.get("type", ""))
        rule = "malicious-dependency" if atype in _MALICIOUS else (
            "vulnerable-dependency" if atype in _VULN else atype
        )
        findings.append(
            Finding(
                tool=tool,
                # Do NOT fabricate a path. When Socket reports no file, the scorer matches by
                # package name against the manifest instead (see score.py DEP_CATEGORIES).
                rule=rule,
                file=a.get("file"),
                severity=a.get("severity"),
                message=a.get("description", "") or a.get("title", ""),
                package=a.get("package") or a.get("pkg") or a.get("purl"),
                extra={"socket_type": atype},
            )
        )
    return findings
