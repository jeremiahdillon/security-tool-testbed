# AGENTS.md — guardrails for coding agents (Codex, OpenCode, Factory, and others)

**STOP and read this before doing anything in this repository.**

This is a **security-tool testbed**. It intentionally contains vulnerable code, fake secrets,
and references to vulnerable/malicious dependencies so that security and code-review tools have
something to detect. It is not a real application.

## DO NOT (hard rules — synced from `docs/safety.md`)

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

## What you *can* do

- Add new test cases or new tools by following `docs/extending.md` and `CONTRIBUTING.md`.
- Edit docs, the scoring harness (`scoring/`), CI workflows, and `ground-truth/` records.
- Read anything.

## Orientation

- `docs/architecture.md` — why the repo is shaped this way (design decisions).
- `docs/methodology.md` — how to run a scoring round.
- `docs/safety.md` — the full safety model and the canonical DO-NOT block.
- `docs/extending.md` — step-by-step: add a case / add a tool.
