# Round notes — 2026-09-23 (baseline)

**Tools scored:** coderabbit, gitar (PR-driven); codeql, sonar, dependabot (full-repo)
**Still to collect (manual dashboard export):** socket, aikido
**Corpus commit:** `4300782eb14ab9d092c12a1d20f3907c3f571b64`

This is the first scored round. The goal is a baseline scorecard: does each connected
tool find the ~48 planted findings, and what does it report that isn't planted (FPs)?

## Scorecard

| tool | precision | recall | F1 | TP | FN | FP | bonus |
|---|---|---|---|---|---|---|---|
| gitar | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 7 |
| dependabot | 0.92 | 1.00 | 0.96 | 12 | 0 | 1 | 1 |
| coderabbit | 1.00 | 0.78 | 0.88 | 7 | 2 | 0 | 3 |
| codeql | 0.73 | 0.73 | 0.73 | 8 | 3 | 3 | 0 |
| sonar | 0.62 | 0.43 | 0.51 | 18 | 24 | 11 | 0 |

Read recall *within each tool's remit*: dependabot/socket are SCA (deps only); codeql/sonar are
SAST (+ some IaC/secrets); coderabbit/gitar are AI reviewers. A tool is only charged FN for a
finding that lists it in `expected_tools`.

- **codeql** 8/11: caught all JS SAST + Python SAST; the 3 FN are Java (XXE, deserialization —
  build-mode:none limits Java taint tracking) and it's not configured for IaC/secrets here. Its
  3 FP are `js/missing-rate-limiting` (a real default query, not a planted vuln).
- **sonar** 18/42 expected: strong on secrets (billing-worker matrix), JS/Python SAST, and
  Docker IaC; misses = Java SAST (no compilation in Automatic Analysis), most SCA (not its
  focus), and the GitHub Actions workflow case. FPs are duplicate detections on already-matched
  lines + a "missing lock file" nag (S8564) that fires *because* we intentionally omit lockfiles.
- **dependabot** 12/12 dep CVEs; 1 FP = mysql-connector's CVE flagged in the license case (real,
  just off-topic for that case); event-stream = bonus.

### Harness changes made while scoring this round (committed)
- Added **Sonar security-repo rule aliases** to `taxonomy.yaml` (`jssecurity:`/`pythonsecurity:`/
  `javasecurity:` — Sonar files security findings under a different rule repo than the quality
  rules we'd mapped). This converted ~5 Sonar SAST detections from miss+FP to TP.
- Added a **Dependabot adapter** (`scoring/adapters/dependabot.py`): parses the alerts API JSON,
  dedupes to one finding per package+manifest, rewrites Maven `group:artifact` to a purl so the
  matcher reduces it to the artifactId. Added `dependabot: ["*"]` alias to malicious-dependency.
- Fixed `load_round` to tolerate an all-commented `inputs.yaml`.

- **Gitar** detected its full expected surface: both code-review logic bugs + all 6 JS SAST
  planted findings (SQLi, cmd-injection, path-traversal, SSRF, 2× hardcoded-secret). 7 bonus =
  the supply-chain (3) and deps-js (4) dependency issues, where Gitar is not an expected_tool.
- **CodeRabbit** recall 0.78: the only 2 misses are both hardcoded secrets in
  `taskflow/lib/config.js` (lines 11, 15). It reviewed the file and summarized its intent
  correctly but did not flag the committed signingKey / session.secret fallback. 3 bonus =
  path-traversal, SSRF, and a supply-chain typosquat.
- **Zero false positives** for both (every unmatched finding was a legit extra bug, not noise —
  see triage below).

### Delivery (PRs, all closed-not-merged)
- PR #1 `cases/code-review/js` · #2 `cases/supply-chain` · #3 `cases/dependencies/js`
- PR #4 `cases/sast/python` · #5 `cases/sast/js/taskflow`

### Methodology notes
- **Socket PR alerts were "Skipped — no net changes to dependencies"** on #2/#3: the canonical
  cases already exist on `main`, so a review-sandbox copy introduces no *new* dependency for
  Socket's diff-based alerts. Socket's detections live in its full-project **Project Report /
  SBOM**, so Socket is scored like the other full-repo tools (from `main`), not via PRs.
- PR delivery therefore only benefits the LLM reviewers (CodeRabbit, Gitar) and PR-decorating
  SAST (CodeQL decorated the diffs inline on #4/#5).
- The `Land case PR` workflow pushes the branch fine but cannot open the PR ("GitHub Actions is
  not permitted to create or approve pull requests" is off); PRs were opened via `gh` from the
  pushed branches. Enable that repo setting to make the workflow one-click.

---

## How to collect each tool's export

Drop each file into this directory and uncomment its line in `inputs.yaml`. All formats
are already supported by the harness (`scoring/adapters/`). Then run:

```bash
python3 scoring/score.py --round results/2026-09-23
```

### codeql  →  `codeql.sarif`   (format: sarif)
- Full-repo SAST, runs in CI (`.github/workflows/codeql.yml`) on every push to `main`.
- Get the SARIF from the latest CodeQL Actions run: **Actions → CodeQL → run → Artifacts**,
  or GitHub API: `gh api repos/jeremiahdillon/security-tool-testbed/code-scanning/analyses`
  then download the analysis SARIF. Save as `codeql.sarif`.
- Covers JS/TS, Python, Java SAST. Does *not* scan the Dockerfile/Actions IaC cases.

### sonar  →  `sonar.json`   (format: sonar)
- SonarCloud Automatic Analysis (no token). Export open issues via the web API:
  `https://sonarcloud.io/api/issues/search?projects=<projectKey>&resolved=false&ps=500`
  Save the JSON response as `sonar.json`.

### aikido  →  `aikido.sarif`   (format: sarif, tool: aikido)
- Aikido (Pro trial). Export findings as SARIF from the Aikido dashboard (Issues → Export),
  or via its GitHub checks. Broad coverage (SAST/SCA/secrets/IaC). SAST matches by CWE;
  SCA/secret/IaC via the `aikido` aliases in `taxonomy.yaml`.

### socket  →  `socket.json`   (format: socket)
- PR-driven. Socket comments on the **Land case PR** (below) with new-dependency alerts.
- Export the report JSON from the Socket dashboard for that PR, or the Socket GitHub App
  check output. Matched by package name against the manifests.

### coderabbit  →  `coderabbit.json`   (format: coderabbit, semi-manual)
- AI review, PR-driven. Transcribe its PR comments into `coderabbit.json`
  (shape in `docs/tools/coderabbit.md`): one row per case with `detected`, `type`,
  `file`, `line`, `summary_matched` (for explainability), and a short `note`.
- Keep un-detected rows too — they're used for explainability scoring, never counted
  as detections/FPs.

### gitar  →  `gitar.json`   (format: gitar, semi-manual)
- AI review (Sonar-owned), PR-driven, ~14-day trial clock. Transcribe like CodeRabbit
  (shape in `docs/tools/gitar.md`).
- ⚠️ **DO NOT apply or merge any Gitar fix.** It has write access and can patch the
  planted vulns, mutating the fixtures. Use its review comments only.

### dependabot  (no adapter — record manually here)
- Alerts only (no auto-updates). Read from **Security → Dependabot alerts**. List which
  planted dependency CVEs it flagged in the triage table below; it isn't auto-scored yet.

---

## Delivering the PR-driven tools (CodeRabbit, Socket, Gitar)

These react to a diff, not files already on `main`. Use the **Land case PR** workflow:
**Actions → "Land case PR" → Run workflow**, pointing it at a case path under `cases/`
(e.g. a supply-chain or code-review case) to open a review-sandbox PR. Let CodeRabbit,
Socket, and Gitar review it, capture their output, then **close the PR without merging**
(never merge a case PR — it would land duplicate fixtures / let a fixer patch them).

---

## Automated report
See `report.md` (generated by `scoring/score.py --round results/2026-09-23`).

## Triage of unmatched / extra findings
The harness reports 0 FP for both tools. Both also surfaced legit-but-unplanted issues in the
cover apps; these are NOT in the transcription JSONs (so they don't count as FP) but are worth
recording — they're real bugs, and candidates for promotion to new planted cases.

| tool | extra finding | verdict | action |
|---|---|---|---|
| coderabbit | tasks.js IDOR (CWE-639) | real-extra-bug | consider new case `sast-js-idor` |
| coderabbit | webhooks.js DoS ×3 (CWE-400/248, no timeout) | real-extra-bug | note; low priority |
| coderabbit | app.py authorization bypass (CWE-862) | real-extra-bug | consider new case |
| coderabbit | app.py:43 sensitive-data-exposure + TSV injection | real-extra-bug | note |
| gitar | index.js no-auth IDOR | real-extra-bug | consider new case `sast-js-idor` |
| gitar | webhooks.js:10 missing request timeout | real-extra-bug | note; low priority |
| gitar | app.py:43 users.tsv stored in public reports dir | real-extra-bug | consider new case |

## CodeRabbit / Gitar explainability
| case | tool | summary_matched | note |
|---|---|---|---|
| codereview-offbyone-001 | coderabbit/gitar | yes | both described "recent pageSize items" window |
| codereview-asyncbug-001 | coderabbit/gitar | yes | both described "email each owner their report" |
| sast-js-hardcoded-secret-001 | coderabbit | yes (but missed the secret) | understood config intent; did not flag the planted credential |

## Dependabot alerts (manual)
| package | CVE / advisory | flagged? | planted case |
|---|---|---|---|
|  |  |  |  |

## Observations / regressions
- Baseline — no prior round to compare.
- Both LLM reviewers are high-precision here (0 FP on planted scoring) and find extra real bugs.
- Gitar's key differentiator this round: caught the hardcoded secret CodeRabbit missed, and
  flagged every dependency CVE/typosquat by name+CVE (bonus) despite being an AI PR reviewer.
- CodeRabbit's one weakness: secret detection in a config file (missed both). Worth re-testing
  against a dedicated secrets case and confirming with its non-CHILL profile if evaluated later.

## Follow-ups
- Collect full-repo exports and add to this same round: codeql.sarif, sonar.json, aikido.sarif,
  socket (SBOM/project report), dependabot alerts — then re-run the harness for the full board.
- Consider promoting the extra findings above into new planted cases (esp. no-auth IDOR).
- Decide whether to enable "Allow GitHub Actions to create and approve pull requests" so
  `Land case PR` is one-click.
