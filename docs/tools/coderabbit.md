# CodeRabbit

**Operating model:** **pull-request review.** CodeRabbit reviews diffs and posts prose comments
plus a PR summary. Its value (and the explainability test) only fires on PRs — cases sitting on
`main` are not reviewed.

**Covers here:** the `code-review` scenarios (off-by-one, missing await, swallowed errors) and,
opportunistically, the SAST cases when they appear in a diff.

## Connect

Install the CodeRabbit GitHub App on this repo. It reviews new PRs automatically.

## Deliver cases to it

Use the `land-case-prs` workflow (or open PRs manually) so each case appears as a diff. To test
explainability cleanly, keep `ground-truth/` out of the PR diff (it lives in a separate
top-level dir; do not include it in the same PR as the case).

## Score it (semi-manual)

CodeRabbit has no clean machine export, so transcribe its outcome per case into
`results/<date>/coderabbit.json`:
```json
{"findings": [
  {"case_id": "codereview-asyncbug-001", "detected": true, "type": "logic-bug",
   "file": "cases/code-review/js/notifier.js", "line": 8,
   "summary_matched": true, "note": "caught missing await + swallowed errors"}
]}
```
- `detected` → counts toward recall for the `coderabbit` tool key.
- `summary_matched` → grades explainability against the case's `expected_summary`.

Round manifest entry: `{format: coderabbit, tool: coderabbit, path: coderabbit.json}`.
If you omit the file, CodeRabbit simply won't appear in the report (shown as "not scored"
rather than "missed").
