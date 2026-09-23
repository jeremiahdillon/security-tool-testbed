# Safety model — read this before touching anything

This repository is a **deliberate security-tool testbed**. It **intentionally** contains
vulnerable code, fake credentials, and manifests that reference vulnerable and
malicious/typosquat dependencies. The material exists so that code-review and security tools
(Sonar, CodeRabbit, Socket, Endor Labs, and others) have something to find, and so their
findings can be scored against a known ground truth.

Nothing here is a real incident. Everything is designed to be **inert as text** — it only
becomes dangerous if something *executes* it.

## The DO-NOT block (canonical source of truth)

<!-- DO-NOT:BEGIN -->
- This repo **intentionally** contains vulnerable code, fake secrets, and references to
  malicious/vulnerable dependencies. It is a **security-tool testbed**, not a real project.
- **Never** install dependencies, build, or run the apps or Dockerfiles in this repo.
- **Never** fix, refactor, sanitize, or remove the planted flaws — they are the fixtures.
  `ground-truth/` references their exact `file:line`.
- All secrets are **fake** and non-functional. Do not use, rotate, or report them as real
  incidents.
- Answers live in `/ground-truth`. **Never** copy them into `cases/` — that would contaminate
  the LLM-reviewer (CodeRabbit) explainability test.
- To reason about a dependency, read the manifest **as text**. Do not install it to inspect.
<!-- DO-NOT:END -->

> The block above is the single source of truth. The same block is mirrored verbatim into
> `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/testbed.mdc`, and `.github/copilot-instructions.md`.
> A CI check fails if they drift out of sync.

## Why this is low-risk

Everything is inert unless executed. The only path to real harm is **installing dependencies**
in one of the manifest directories, because package install scripts run arbitrary code. That
path is blocked in layers:

1. **Instruction** — the DO-NOT block, in every agent-instruction file.
2. **Repo config** — an `.npmrc` with `ignore-scripts=true` sits in **every directory that has a
   `package.json`** (not just the repo root — npm reads `.npmrc` from the project root where the
   command runs, and does not inherit an ancestor's). Do not delete these per-directory
   `.npmrc` files. No lockfiles are committed, and each bad manifest lives in its own isolated
   subdirectory (no root workspace links them).
3. **CI check** — a job fails the build if a lockfile or install artifact is committed.
4. **Runtime net** — Socket Firewall (`sfw`), if installed locally, refuses a flagged package
   before download even if the layers above are bypassed.

Supply-chain cases reference **already-removed / non-resolving** package names, so even an
accidental install fails harmlessly at registry resolution rather than fetching a live payload.

## GitHub push protection

GitHub secret scanning / push protection may block a push that contains fake secrets matching
real provider patterns. This is expected. Because this repo is an intentional decoy, it is
acceptable to **disable push protection for this repository** (Settings → Code security), or to
allowlist the specific detections. Do not swap in real values to get around it.

## Validating that no REAL secret ever leaks

All planted credentials are fabricated and non-functional, but that claim must be *verifiable*,
especially before pushing to a public remote. Layers:

1. **`python scoring/leak_check.py`** (in pre-commit and CI). Fails if any provider credential
   pattern appears **outside** the planted dirs (`cases/`, `scoring/fixtures/`), if a
   credential-style filename is committed, or — locally — if any planted value collides with a
   real secret in this machine's stores (`~/.aws`, `~/.ssh`, env, …; match/no-match only, real
   contents never printed).
2. **An independent scanner**, e.g. `detect-secrets scan --all-files`, to confirm detections
   land only in the planted files.
3. **Live verification before first push** (proves the fakes are dead):
   ```bash
   trufflehog filesystem . --json --no-update | \
     python3 -c "import sys,json; \
       v=sum(json.loads(l).get('Verified',False) for l in sys.stdin if l.strip() and 'DetectorName' in l); \
       print('VERIFIED (live) secrets:', v)"
   # expect: 0
   ```
   Any non-zero result means a real credential is present — stop and remove it.
4. **GitHub push protection** is the final, independent gate. Push with it **on** first; if it
   only flags the intended planted files, allowlist those specific detections (or disable it for
   this decoy repo). If it flags anything unexpected, stop.

## Opsec (public repo)

Keep the repo free of environment-specific details (local paths, usernames, hostnames, accounts,
personal tooling, review process, tier/budget). Describe the testbed generically. See the
"Opsec — keep it public-safe" section in `CONTRIBUTING.md` for the checklist and the pre-publish
grep.

## Rules for the apps

Do not `npm start`, `flask run`, `mvn`/`gradle`, `docker build`, or otherwise execute anything
here. If you need to see behavior, reason about the source statically.
