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
python3 scoring/guardrail_check.py                       # DO-NOT sync + no install artifacts
python3 scoring/leak_check.py                            # no REAL secret leaks (fakes only)
python3 scoring/score.py --validate                      # ground-truth schema + file:line
grep -rniE 'vulnerab|insecure|injection|CWE-' cases/     # must return nothing
python3 scoring/score.py --self-test                     # harness still works
```
(Install the pre-commit hooks with `pre-commit install` to run the first two automatically.)

## Authoring supply-chain cases

If the Socket MCP server is available, confirm each planted package name is recognized by
Socket's intelligence before committing — see [`docs/tools/socket.md`](docs/tools/socket.md).
