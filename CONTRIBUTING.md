# Contributing

This is a security-tool testbed. Before anything, read [`docs/safety.md`](docs/safety.md) and
the DO-NOT block in [`CLAUDE.md`](CLAUDE.md)/[`AGENTS.md`](AGENTS.md). **Never install, build,
or run the corpus.**

## Add a case or a tool

Follow the step-by-step playbooks in [`docs/extending.md`](docs/extending.md):
- **Add a case (new flaw/vuln type)** — Playbook A.
- **Add a tool** — Playbook B.

## Golden rules

1. **No tells in `cases/`.** Realistic code only — no `// vulnerable` comments, no giveaway
   filenames, no CWE ids. Answers go in `ground-truth/`.
2. **Everything inert.** No lockfiles. No committed `node_modules`/`.venv`/`target`. Bad
   dependency names should be removed/non-resolving where possible.
3. **Keep the DO-NOT block in sync.** It is duplicated verbatim across `docs/safety.md`,
   `CLAUDE.md`, `AGENTS.md`, `.cursor/rules/testbed.mdc`, `.github/copilot-instructions.md`.
   The canonical copy is in `docs/safety.md`.

## Before you commit / open a PR

```bash
python3 scoring/guardrail_check.py    # DO-NOT sync + no install artifacts + no giveaways in cases/
python3 scoring/leak_check.py         # no REAL secret leaks (planted fakes only)
python3 scoring/score.py --validate   # ground-truth schema + file:line + known tools
python3 scoring/score.py --self-test  # harness still works
```
(The no-giveaways scan now lives inside `guardrail_check.py` as the single shared check — no
separate grep to keep in sync.)
(Install the pre-commit hooks with `pre-commit install` to run the first two automatically.)

## Keeping the CodeRabbit test clean

A single PR that adds both a case (`cases/`) and its answer (`ground-truth/`) would let an LLM
reviewer read the answer while reviewing the diff. For a clean CodeRabbit explainability test,
introduce the case to reviewers via the `land-case-prs` workflow (it copies only the case, never
`ground-truth/`), or commit the `ground-truth/` record in a separate PR. CI does not block a
combined PR — this is a convention, not an enforced rule.

## Authoring supply-chain cases

If the Socket MCP server is available, confirm each planted package name is recognized by
Socket's intelligence before committing — see [`docs/tools/socket.md`](docs/tools/socket.md).
