"""SonarQube / SonarCloud adapter.

Accepts the JSON returned by the Sonar web API `api/issues/search` (and the similar
`api/hotspots/search` shape). If you instead export SARIF from Sonar, use the sarif adapter
with `--tool sonar`.

Example fetch (documented in docs/tools/sonar.md):
  curl -u $SONAR_TOKEN: \
    "$SONAR_URL/api/issues/search?componentKeys=$KEY&resolved=false&ps=500" > sonar.json
"""
from __future__ import annotations

import json

from .common import Finding, read_text


def _strip_component(component: str) -> str:
    # Sonar component keys look like "projectKey:path/to/file". Keep the path.
    return component.split(":", 1)[1] if ":" in component else component


def parse(path: str, tool: str = "sonar") -> list[Finding]:
    data = json.loads(read_text(path))
    findings: list[Finding] = []
    for issue in data.get("issues", []) or data.get("hotspots", []):
        cwe = None
        # Sonar tags sometimes include "cwe" but not the number; leave to taxonomy alias match.
        findings.append(
            Finding(
                tool=tool,
                rule=issue.get("rule") or issue.get("ruleKey", ""),
                cwe=cwe,
                file=_strip_component(issue.get("component", "")),
                line=issue.get("line"),
                severity=issue.get("severity") or issue.get("vulnerabilityProbability"),
                message=issue.get("message", ""),
            )
        )
    return findings
