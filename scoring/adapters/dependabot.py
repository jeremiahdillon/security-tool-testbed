"""Dependabot adapter.

Parses the JSON returned by the GitHub REST API
`GET /repos/{owner}/{repo}/dependabot/alerts` (fetch with `gh api --paginate` — the endpoint
uses cursor pagination, so `?page=N` is rejected; `gh --paginate` follows the Link header).

Each alert names a vulnerable dependency and the manifest it was declared in. Dependabot emits
*many* alerts per package (one per advisory), so we dedupe to one finding per
(package, manifest): the harness matches dependency findings by package name against the
declared entry on the planted line, and duplicate advisories for the same package would
otherwise look like false positives.

Maven package names arrive as `group:artifact`; we rewrite them to a purl
(`pkg:maven/group/artifact`) so the harness's `_bare_package` reduces them to the artifactId,
which is what `_dep_name_at` reads from `<artifactId>` in a pom.xml. npm/pip names pass through
(comparison is case-insensitive, so `Django` == `django`).
"""
from __future__ import annotations

import json

from .common import Finding, read_text


def _package_field(name: str, ecosystem: str) -> str:
    eco = (ecosystem or "").lower()
    if eco == "maven" and ":" in name:
        group, _, artifact = name.partition(":")
        return f"pkg:maven/{group}/{artifact}"
    return name


def parse(path: str, tool: str = "dependabot") -> list[Finding]:
    data = json.loads(read_text(path))
    if isinstance(data, dict):  # tolerate a single-object or error payload
        data = data.get("alerts") or []
    findings: list[Finding] = []
    seen: set[tuple[str, str]] = set()
    for alert in data:
        dep = (alert.get("dependency") or {})
        pkg = (dep.get("package") or {})
        name = pkg.get("name")
        if not name:
            continue
        manifest = dep.get("manifest_path") or ""
        key = (name.lower(), manifest)
        if key in seen:
            continue
        seen.add(key)
        adv = alert.get("security_advisory") or {}
        cwes = adv.get("cwes") or []
        cwe = cwes[0].get("cwe_id") if cwes and isinstance(cwes[0], dict) else None
        findings.append(
            Finding(
                tool=tool,
                rule=adv.get("ghsa_id") or "dependabot-alert",
                cwe=cwe,
                file=manifest,
                line=None,
                package=_package_field(name, pkg.get("ecosystem", "")),
                severity=(adv.get("severity") or (alert.get("security_vulnerability") or {}).get("severity")),
                message=adv.get("summary", ""),
            )
        )
    return findings
