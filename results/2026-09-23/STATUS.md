# Resume snapshot — security-tool-testbed

_Last updated: 2026-09-26. Authoritative in-repo handoff for resuming work. See also
`results/2026-09-23/notes.md` (round detail) and `results/2026-09-23/report.md` (generated matrix)._

## Where things stand

The **2026-09-23 baseline round is complete**: all 7 connected tools collected, scored,
committed, and pushed to `main`. Repo is clean and up to date with `origin/main`.

### Final scorecard (7 tools)

| tool | precision | recall | F1 | TP | FN | FP | bonus |
|---|---|---|---|---|---|---|---|
| gitar | 1.00 | 1.00 | 1.00 | 8 | 0 | 0 | 7 |
| dependabot | 0.92 | 1.00 | 0.96 | 12 | 0 | 1 | 1 |
| coderabbit | 1.00 | 0.78 | 0.88 | 7 | 2 | 0 | 3 |
| socket | 1.00 | 0.75 | 0.86 | 12 | 4 | 0 | 0 |
| codeql | 0.73 | 0.73 | 0.73 | 8 | 3 | 3 | 0 |
| aikido | 1.00 | 0.57 | 0.72 | 26 | 20 | 0 | 0 |
| sonar | 0.62 | 0.43 | 0.51 | 18 | 24 | 11 | 0 |

Regenerate anytime: `python3 scoring/score.py --round results/2026-09-23`.

## How each tool's data was collected (reproducible)

All via `gh`/API or dashboard export; no `security_events` scope needed (public repo, `repo`
scope suffices). Files live in `results/2026-09-23/`.

- **codeql** — `gh api -H "Accept: application/sarif+json" repos/<repo>/code-scanning/analyses/<id>`,
  latest analysis per language → `codeql-{js,py,java}.sarif`.
- **sonar** — SonarCloud public API (no token):
  `curl "https://sonarcloud.io/api/issues/search?componentKeys=jeremiahdillon_security-tool-testbed&resolved=false&ps=500"` → `sonar.json`.
- **dependabot** — `gh api --paginate repos/<repo>/dependabot/alerts?per_page=100` (cursor
  pagination; `?page=N` errors) → `dependabot.json` (173 alerts).
- **coderabbit / gitar** — semi-manual transcription of PR reviews → `coderabbit.json`, `gitar.json`.
- **socket** — free-tier dashboard **CSV** export → converted to `socket.json` (adapter shape).
- **aikido** — free tier has **no SARIF/JSON export**; transcribed from the dashboard PDF →
  `aikido.json` (canonical types). Raw CSV/PDF were NOT committed (only derived JSON).

## Tooling / environment state (persists on this machine)

- `gh` CLI installed at `~/.npm-global/bin/gh` (release binary — Homebrew's Cellar is owned by
  `jeremiahdillon`, not `agentserver`, so `brew install` fails). Authed as **jeremiahdillon**,
  creds in `agentserver`'s `~/.config/gh` (so the agent's shell sees them). Scopes:
  `repo, workflow, read:org, gist`.
- Git remote uses SSH alias `git@github-openclaw:` (plain `git@github.com` fails; key auths as
  jeremiahdillon). Commits use noreply email; commit timestamps kept ≥5pm Pacific (opsec).
- Repo setting **"Allow GitHub Actions to create and approve PRs" is OFF** → the `Land case PR`
  workflow pushes the branch but can't open the PR; open PRs via `gh pr create` from the pushed
  branch (or enable the setting). Push protection is ON but does not block review-sandbox branches
  copying secret-bearing cases (the fake secrets already exist on `main`, so not "new").

## Harness changes made this round (committed)

- New `scoring/adapters/dependabot.py` (dedupe per package+manifest; Maven `group:artifact` →
  `pkg:maven/...` purl so the matcher gets the artifactId).
- New `scoring/adapters/aikido.py` (semi-manual; reads `{findings:[{type,file,package}]}` with
  **canonical** types so `rule == type` matches directly).
- `taxonomy.yaml`: added Sonar security-repo aliases (`jssecurity:`/`pythonsecurity:`/
  `javasecurity:`) — Sonar files security findings under a different rule repo than quality rules;
  added `dependabot: ["*"]` to `malicious-dependency`.
- `score.py`: `load_round` tolerates an all-commented `inputs.yaml`.

## Methodology caveat (important when reading the board)

Automated tools (codeql, sonar, dependabot) get **mechanical FP counting** (every unmatched
finding in `cases/` is an FP). Semi-manual tools (coderabbit, gitar, aikido, socket-via-CSV) are
transcribed as detections-of-planted-issues only; their extra real findings are logged in
`notes.md` triage, **not** as FPs — which is why they read 0 FP. Compare precision with that in mind.

## Key evaluation findings

- **CodeRabbit** missed both hardcoded secrets in `taskflow/lib/config.js`; **Gitar** caught them.
- **Socket** free CSV surfaced dependency CVEs but classified `event-stream` as a CVE (not
  malware), `loadsh` as "deprecated", omitted `crossenv` (removed from npm), and emitted no GPL
  license alert — so it "missed" the supply-chain/malicious + license cases by type.
- **Aikido** = broadest single tool (26 TP across SAST/secrets/IaC/deps) but missed JS SSRF,
  Python path-traversal + weak-crypto, the `pr-build.yml` workflow case, license, the typosquats,
  the gcp-service-account secret, and requests/Jinja2/urllib3.
- **No-auth IDOR** in `taskflow/index.js` was flagged by CodeRabbit, Gitar, Aikido, and Sonar
  (S5689) — a strong candidate to promote into a planted case.

## Out of scope this round

- **Endor Labs** — tenant-gated, no self-serve free tier ("No authorized tenant found").
- **GitHub secret scanning** — deliberately skipped as a scored tool.

## Suggested next steps (nothing in progress)

1. Promote recurring extra findings into planted cases — esp. the no-auth **IDOR** (index.js),
   and `users.tsv` public exposure (app.py:43). Follow `docs/extending.md` Playbook A.
2. Run a **second round** later to watch tool drift over time.
3. Wire up **Endor** if a tenant is ever provisioned; add GitHub secret scanning if desired.
