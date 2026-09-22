# Methodology — running a comparison round

A "round" is one snapshot of every tool's output scored against the ground truth. Rounds are
dated and committed under `results/<YYYY-MM-DD>/` so tool improvement/regression is visible over
time.

## Prerequisites

- `sfw pip3 install -r scoring/requirements.txt` (PyYAML only).
- One or more tools connected (see `docs/tools/`). You can start with just CodeQL.

## Steps

1. **Create the round directory.**
   ```bash
   mkdir -p results/$(date +%F)/raw
   cp results/TEMPLATE.md results/$(date +%F)/notes.md
   ```

2. **Collect each tool's output** into the round directory (formats in `docs/tools/`):
   - CodeQL → `codeql.sarif` (SARIF)
   - Sonar → `sonar.json` (issues API export) or SARIF
   - Socket → `socket.json`
   - Endor → `endor.json`
   - CodeRabbit → `coderabbit.json` (transcribed by hand — see below)

3. **Write the round manifest** `results/<date>/inputs.yaml`:
   ```yaml
   inputs:
     - {format: sarif,  tool: codeql, path: codeql.sarif}
     - {format: sonar,  tool: sonar,  path: sonar.json}
     - {format: socket, tool: socket, path: socket.json}
     - {format: endor,  tool: endor,  path: endor.json}
     - {format: coderabbit, tool: coderabbit, path: coderabbit.json}
   ```
   Include only the tools you actually ran.

4. **Score.**
   ```bash
   python3 scoring/score.py --round results/$(date +%F)
   ```
   This writes `report.md` (summary table + detection matrix + misses + findings to triage) and
   prints it.

5. **Triage & record.** For each "unmatched finding to triage", decide in `notes.md` whether it
   is a genuine false positive or a real extra bug (which may deserve a new case). Note any
   CodeRabbit explainability observations.

6. **Commit** the round directory.

## Scoring CodeRabbit

CodeRabbit posts prose PR comments; there is no clean export. After a review, transcribe its
outcome per case into `coderabbit.json`:

```json
{"findings": [
  {"case_id": "sast-js-sqli-001", "detected": true, "type": "sql-injection",
   "file": "cases/sast/js/taskflow/routes/tasks.js", "line": 11,
   "summary_matched": true, "note": "flagged the concatenated query"}
]}
```

`summary_matched` grades **explainability**: did CodeRabbit's PR summary match the case's
`expected_summary`? Record a one-line justification in `notes.md`.

## Delivering cases as PRs (for CodeRabbit / Socket)

CodeRabbit and Socket react to pull requests. Use the `land-case-prs` workflow (manual
dispatch) to open a PR that introduces a case or batch, let the tools review it, collect their
output, then proceed with scoring. Full-repo tools (Sonar, Endor) can scan the merged `main`.
