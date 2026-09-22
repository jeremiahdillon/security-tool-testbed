"""Adapter registry.

Each adapter exposes `parse(path, tool=...) -> list[Finding]`. The scorer picks an adapter by
format (how to parse) and attributes findings to a tool key (who found them).

Formats: sarif, sonar, socket, endor, coderabbit.
Tool keys are free-form (sonar, codeql, semgrep, socket, endor, coderabbit, gitleaks, ...).
"""
from __future__ import annotations

from . import coderabbit, endor, sarif, socket, sonar
from .common import Finding

_FORMATS = {
    "sarif": sarif.parse,
    "sonar": sonar.parse,
    "socket": socket.parse,
    "endor": endor.parse,
    "coderabbit": coderabbit.parse,
}


def parse(fmt: str, path: str, tool: str | None = None) -> list[Finding]:
    if fmt not in _FORMATS:
        raise ValueError(f"unknown format '{fmt}'. known: {', '.join(sorted(_FORMATS))}")
    return _FORMATS[fmt](path, tool=tool or fmt)


def known_formats() -> list[str]:
    return sorted(_FORMATS)


__all__ = ["parse", "known_formats", "Finding"]
