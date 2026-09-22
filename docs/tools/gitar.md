# Gitar

**Operating model:** **pull-request review** by an AI agent (Gitar is owned by Sonar). Like
CodeRabbit, it posts prose PR comments and can propose fixes; there is no clean machine-readable
findings export, so it is scored **semi-manually**.

**Covers here:** the `code-review` logic-bug scenarios and, opportunistically, the JS SAST cases
when they appear in a PR diff.

> **Trial clock:** Gitar's free access is a ~14-day trial. Connect it **last**, only when the
> repo is pushed, the corpus is final, and the other tools are already producing output — then
> run a full round and capture Gitar's results within the window. See `docs/methodology.md`.

## Connect

Install the Gitar GitHub App on the repo. Deliver cases via the `land-case-prs` workflow (or
normal PRs) so Gitar has diffs to review.

## Score it (semi-manual)

Transcribe Gitar's per-case outcome into `results/<date>/gitar.json` (same shape as CodeRabbit):

```json
{"findings": [
  {"case_id": "codereview-offbyone-001", "detected": true, "type": "logic-bug",
   "file": "cases/code-review/js/pagination.js", "line": 13,
   "summary_matched": true, "note": "flagged the off-by-one"}
]}
```

Round manifest entry: `{format: gitar, tool: gitar, path: gitar.json}`. Use canonical taxonomy
`type` values. Un-detected rows are kept for explainability scoring but never count as
detections or false positives.
