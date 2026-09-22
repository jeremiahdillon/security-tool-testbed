"""Gitar adapter.

Gitar (owned by Sonar) is an AI PR reviewer/agent: like CodeRabbit, it posts prose PR comments
with no clean machine-readable findings export, so it is scored **semi-manually** using the same
transcribed-JSON shape as the coderabbit adapter. Transcribe Gitar's per-case outcome into a
JSON file and point the round manifest at it with `{format: gitar, tool: gitar, path: gitar.json}`:

    {"findings": [
       {"case_id": "codereview-offbyone-001", "detected": true, "type": "logic-bug",
        "file": "cases/code-review/js/pagination.js", "line": 13,
        "summary_matched": true, "note": "flagged the off-by-one"}
    ]}

`type` should be the canonical taxonomy type (so it matches by rule==type). `summary_matched`
feeds the explainability table. Un-detected rows are kept (they can't score as detections or
false positives) so explainability is not biased to detections.
"""
from __future__ import annotations

from . import coderabbit


def parse(path: str, tool: str = "gitar") -> list:
    # Identical transcription format to CodeRabbit; just attribute to the given tool key.
    return coderabbit.parse(path, tool=tool)
