"""Shared types for tool-output adapters.

Every adapter turns a tool's native output file into a list of `Finding` objects. The scorer
then matches findings to the ground truth using the canonical taxonomy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Finding:
    """One normalized finding emitted by a tool."""

    tool: str                      # tool key: sonar, codeql, socket, endor, coderabbit, ...
    rule: str = ""                 # native rule id / category (used against taxonomy aliases)
    cwe: str | None = None         # e.g. "CWE-89" if the tool reported one
    file: str | None = None        # repo-relative path if applicable
    line: int | None = None        # 1-indexed line if applicable
    severity: str | None = None    # tool's severity, verbatim
    message: str = ""              # human-readable message
    package: str | None = None     # for dependency/supply-chain findings
    extra: dict = field(default_factory=dict)

    def norm_file(self) -> str | None:
        if not self.file:
            return None
        # Normalize leading ./ and absolute-ish prefixes to repo-relative.
        p = self.file.replace("\\", "/").lstrip("./")
        # Trim anything before a `cases/` segment so absolute CI paths still match.
        idx = p.find("cases/")
        return p[idx:] if idx != -1 else p


def read_text(path: str | Path) -> str:
    return Path(path).read_text(encoding="utf-8")
