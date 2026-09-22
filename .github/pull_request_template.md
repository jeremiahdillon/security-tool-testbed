<!--
This is a security-tool testbed. PRs typically either (a) add/modify a test case, or
(b) are transient "review sandbox" PRs used to trigger PR-driven tools (do not merge those).
-->

## Type of change
- [ ] New/updated test case (source under `cases/` + record in `ground-truth/`)
- [ ] New/updated tool adapter or docs
- [ ] Harness / taxonomy / CI change
- [ ] Transient review-sandbox PR (do NOT merge)

## Checklist (for case/tool changes)
- [ ] Source under `cases/` contains **no tells** (no `// vulnerable`, giveaway names, or CWE ids)
- [ ] Answers are in `ground-truth/<id>.yaml` only
- [ ] `python3 scoring/score.py --validate` passes
- [ ] `python3 scoring/guardrail_check.py` passes
- [ ] `python3 scoring/score.py --self-test` passes
- [ ] No lockfiles / install artifacts added

## Notes
<!-- what this changes and why -->
