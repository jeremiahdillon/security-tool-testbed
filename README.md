# security-tool-testbed

A living corpus for evaluating and comparing **code-review and security tools** — Sonar,
CodeRabbit, Socket, Endor Labs, CodeQL, and others. It contains deliberately-flawed code and
metadata so each tool has something to find, plus a machine-readable **ground truth** and a
**scoring harness** so you can measure precision / recall / false positives and re-score as the
tools evolve.

> ## ⚠️ SAFETY — READ FIRST
> This repository **intentionally** contains vulnerable code, **fake** secrets, and manifests
> that reference vulnerable/malicious dependencies. It is a **testbed**, not a real project.
> **Never install dependencies, build, or run anything here.** Everything is inert as text;
> harm only comes from executing it. Full model: [`docs/safety.md`](docs/safety.md).
> Guardrails for coding agents: [`CLAUDE.md`](CLAUDE.md), [`AGENTS.md`](AGENTS.md).

## What it tests

| Category | Where | Exercises |
|---|---|---|
| SAST / code quality | `cases/sast/{js,python,java}` | SQLi, command injection, SSRF, path traversal, weak crypto, insecure deserialization, XXE, hardcoded secrets |
| Secrets detection | `cases/billing-worker/config/` | AWS, GCP, Azure, Stripe, Twilio, GitHub, Slack, Google Maps, OpenAI, Anthropic, OpenRouter, PEM key |
| Dependency CVEs (SCA) | `cases/dependencies/{js,python,java}` | manifests pinned to known-vulnerable versions (Log4Shell, etc.) |
| Supply chain | `cases/supply-chain` | typosquats & historically-malicious packages — **referenced, never installed** |
| AI code review | `cases/code-review` | subtle logic bugs (off-by-one, missing await, swallowed errors) — delivered via PRs |
| License compliance | `cases/license` | GPL dependency in an MIT project |
| IaC / CI posture | `cases/iac-ci` | insecure Dockerfile, dangerous GitHub Actions workflow |

## How it's organized

- **`cases/`** — source only. Realistic mini-apps with **no tells** (no "vulnerable" comments,
  no giveaway filenames) so an LLM reviewer has to find flaws on its own.
- **`ground-truth/`** — all answers, one YAML per case, kept **out of** `cases/` so a
  PR-reviewing LLM can't read them. Maps each planted flaw to `file:line`, severity, and which
  tools should catch it.
- **`taxonomy.yaml`** — canonical vuln-type ↔ CWE ↔ per-tool naming, read by the harness.
- **`scoring/`** — the harness (`score.py`) + per-tool adapters.
- **`results/`** — dated results of each comparison round (the living log).
- **`docs/`** — start here: [`architecture.md`](docs/architecture.md) (why),
  [`onboarding.md`](docs/onboarding.md) (connect the tools — the runbook),
  [`methodology.md`](docs/methodology.md) (how to run a round),
  [`extending.md`](docs/extending.md) (add a case / add a tool),
  [`tools/`](docs/tools) (per-tool setup).

## Quick start

```bash
# 1. Harness deps (the ONLY place installs are allowed — no test-corpus packages here).
python3 -m pip install -r scoring/requirements.txt   # PyYAML only; the only installs this repo needs

# 2. Prove the harness works (hermetic fixtures, no real tools needed).
python3 scoring/score.py --self-test

# 3. Validate the ground truth and guardrails.
python3 scoring/score.py --validate
python3 scoring/guardrail_check.py
```

To run a real comparison round, connect one or more tools and follow
[`docs/methodology.md`](docs/methodology.md). You don't need all tools — CodeQL is free and
gives an immediate baseline.

## License

MIT — see [`LICENSE`](LICENSE).
