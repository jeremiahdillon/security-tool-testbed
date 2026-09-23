# Tool onboarding runbook

How to connect the code-review / security tools to this repository and start comparing them.
Per-tool depth lives in [`docs/tools/`](tools/); this page is the **sequence** and the **why**.

## Principles

- **No-clock tools first, trials last.** Connect everything with a free-forever tier, run a
  baseline round, and only then connect any time-limited trials (e.g. **Gitar** is ~14 days) so
  the clock isn't spent on setup.
- **Standard scanning only.** Each tool below has a free, OSS, or trial tier sufficient for
  evaluation; no paid features are required.
- **Don't let anything "fix" the fixtures.** The planted vulnerabilities, secrets, and
  vulnerable/malicious dependencies are the test material. Enable *detection*; do **not** enable
  auto-remediation / auto-update PRs (see Dependabot below). Never merge a PR that "fixes" a case.
- **PR-driven vs full-repo.** Some tools only react to pull requests; feed them via the
  `land-case-prs` workflow (see [Feeding PR-driven tools](#feeding-pr-driven-tools)).

## Connection checklist

| Tool | Type | Clock | Connect via | Status |
|---|---|---|---|---|
| CodeQL | SAST | none | committed workflow (auto) | ☐ |
| GitHub secret scanning + push protection | secrets | none | repo/account settings | ☐ |
| Dependabot **alerts** | SCA | none | repo settings (alerts only) | ☐ |
| CodeRabbit | AI review (PR) | none | GitHub App | ☐ |
| Socket | supply-chain/SCA (PR) | none | GitHub App | ☐ |
| Aikido | SAST+SCA+secrets+IaC | none | GitHub App | ☐ |
| SonarCloud | SAST (+PR) | none | workflow + `SONAR_TOKEN` | ☐ |
| **Gitar** | AI review (PR) | **~14-day trial** | GitHub App | ☐ (last) |
| **Endor Labs** | SCA+reachability+SAST | trial-dependent | GitHub App / endorctl | ☐ (last) |

---

## 1. CodeQL  (committed workflow)

Runs from `.github/workflows/codeql.yml` (JS/TS, Python, Java, `build-mode: none` — it never
builds the corpus). Results appear under **Security → Code scanning** as SARIF. For a round,
download the SARIF and use `{format: sarif, tool: codeql, path: codeql.sarif}`.

## 2. GitHub secret scanning + push protection  (native)

- **Secret scanning alerts:** Settings → **Code security** → enable *Secret scanning*. Alerts
  will populate for the planted credentials in `cases/billing-worker/config/*` and
  `cases/sast/js/taskflow/lib/config.js` — that's expected; GitHub's detector is one of the tools.
- **Push protection:** keep it **on** at account and repo level. It only scans *new* commits, so
  existing history won't re-trigger; a future PR that introduces a new secret will be blocked
  (itself a useful test). Note: publishing this corpus initially requires allowing the planted
  secrets (they are fabricated) or temporarily disabling push protection for that first push.
- To score it, transcribe the alerts (there's no SARIF export) using the `coderabbit`-style JSON
  with `tool: github`, or record coverage manually.

## 3. Dependabot  (native — ALERTS ONLY)

**What Dependabot is.** A GitHub-native dependency tool with three separate features:

1. **Dependabot alerts** — flags dependencies with known vulnerabilities (CVEs) from the GitHub
   Advisory Database, using the repo's dependency graph. *Detection only, no code changes.*
2. **Dependabot security updates** — automatically opens PRs to bump vulnerable deps to fixed
   versions.
3. **Dependabot version updates** — scheduled PRs to keep deps current, configured by a
   `.github/dependabot.yml` file.

**For this testbed, enable #1 only.** #2 and #3 would open PRs that *upgrade the planted
vulnerable versions to patched ones* — i.e. they'd try to "fix" the exact fixtures we're testing
detection against, and mutate `cases/` manifests. That's why this repo intentionally has **no
`.github/dependabot.yml`**.

**Enable alerts:** Settings → **Code security** → turn on *Dependency graph* (usually on for
public repos) and *Dependabot alerts*. Leave *Dependabot security updates* **off**.

- Where results show: **Security → Dependabot** tab. Expect alerts for `cases/dependencies/**`
  (lodash 4.17.20, log4j-core 2.14.1, etc.).
- To score it: transcribe alerts to JSON with `tool: dependabot` (no SARIF export), matched by
  package against the manifest.
- To observe Dependabot's update behavior, do it on a throwaway branch and **close** (never
  merge) the PRs — don't let them change the corpus on `main`.

## 4. CodeRabbit  (GitHub App — PR-driven)

Install the CodeRabbit app on the repo. It reviews pull requests; feed it cases via
`land-case-prs`. Score semi-manually (transcribe to `coderabbit.json`, including
`summary_matched` for explainability). Details: [`docs/tools/coderabbit.md`](tools/coderabbit.md).

## 5. Socket  (GitHub App — PR-driven)

Install the Socket app. Its headline alerts fire when a PR *adds* a risky dependency, so deliver
`cases/dependencies/*` and `cases/supply-chain/*` via `land-case-prs`. Socket Firewall (`sfw`),
if used locally, is the install-time backstop. Details: [`docs/tools/socket.md`](tools/socket.md).

## 6. Aikido  (GitHub App — broad)

Install the Aikido app (free tier). Broad coverage (SAST/SCA/secrets/IaC). Export SARIF for a
round: `{format: sarif, tool: aikido, path: aikido.sarif}`. Details:
[`docs/tools/aikido.md`](tools/aikido.md).

## 7. SonarCloud

Two modes; pick one:

- **Automatic Analysis (recommended, no token):** sign in to SonarCloud with GitHub, install the
  SonarCloud app, import this (public) repo, and choose *Automatic Analysis*. It scans on every
  push with no CI job or token. This is the mode this repo uses.
- **CI-based (optional):** add repo secret **`SONAR_TOKEN`**, set `projectKey`/`organization` in
  `sonar-project.properties`, and the token-gated `.github/workflows/sonar.yml` runs the scan.
  Turn *Automatic Analysis* off in the project if you use this (the two can't both run).

To pull Sonar's findings into a scoring round, export issues via the web API (a read-only user
token) — see [`docs/tools/sonar.md`](tools/sonar.md).

## 8. Gitar  (GitHub App — TRIAL, connect LAST)

~14-day trial. **Connect only when the corpus is final and the no-clock tools are producing
output.** Then install, run a full round, and capture Gitar's results within the window.
Semi-manual scoring (transcribe to `gitar.json`). Details: [`docs/tools/gitar.md`](tools/gitar.md).

## 9. Endor Labs  (GitHub App / endorctl — connect LAST if trial)

Endor's CLI is `endorctl`. If access is via a time-limited trial, connect it in the same late
wave as Gitar. Full-project scans (SCA + reachability + SAST + secrets); note reachable-vs-present
in the round notes. Details: [`docs/tools/endor.md`](tools/endor.md).

---

## Feeding PR-driven tools

CodeRabbit, Socket, and Gitar only react to pull requests. Because the whole corpus is already on
`main`, use the **`land-case-prs`** workflow (Actions → *Land case PR* → Run workflow) to open a
transient PR that copies a case into `review-sandbox/` for the tools to review. These PRs are
**not merged** — close them after collecting output. (For a *pristine* review of a brand-new case,
introduce it via a normal PR *before* it hits `main`.)

## Running a comparison round

Once ≥1 tool is connected, follow [`docs/methodology.md`](methodology.md): snapshot each tool's
output into `results/<date>/`, write `inputs.yaml`, run
`python3 scoring/score.py --round results/<date>`, triage, and commit. Start a baseline round with
CodeQL + whatever else is connected before starting the trials.

## Suggested order of operations

1. Enable GitHub secret scanning + Dependabot **alerts** (native, instant).
2. Install CodeRabbit, Socket, Aikido apps.
3. Set up SonarCloud (`SONAR_TOKEN` + project config).
4. Run a **baseline round**.
5. Connect **Gitar** (+ Endor if trial), run a round, capture within the trial window.
