# Extending the testbed

Two playbooks. Both are self-contained — a future contributor needs nothing outside this repo.

---

## Playbook A — Add a case (a new flaw or vuln type)

1. **Place the source under `cases/`**, embedded in a realistic app. Reuse an existing cover
   app (`cases/sast/js/taskflow`, `cases/sast/python/reportsvc`, `cases/sast/java/docsvc`,
   `cases/billing-worker`) or add a new one.
   - **No tells.** No comments like `// vulnerable`, no filenames like `sql_injection.js`, no
     CWE ids in source. It must read like ordinary application code.

2. **Pick the canonical type.** If it already exists in `taxonomy.yaml`, use that `type` key.
   If it's a new class of finding, add an entry to `taxonomy.yaml` (key, `cwe`, and per-tool
   `aliases` so findings map correctly).

3. **Write the ground-truth record** `ground-truth/<id>.yaml` (copy
   `templates/case/ground-truth.example.yaml`; spec in `templates/ground-truth.schema.yaml`):
   - `id` must equal the filename stem; convention `<category>-<lang>-<short>-NNN`.
   - one `planted` entry per flaw with exact `file`, `line`, `severity`, and `expected_tools`.
   - add `expected_summary` for anything you want to grade CodeRabbit's explainability on.

4. **Validate.**
   ```bash
   python3 scoring/score.py --validate      # schema + file:line existence
   python3 scoring/guardrail_check.py       # DO-NOT sync + no install artifacts
   grep -rniE 'vulnerab|insecure|injection|CWE-' cases/   # must return nothing
   ```

5. **Land it.** Commit; for CodeRabbit/Socket coverage, introduce it via a PR (the
   `land-case-prs` workflow, or just open a normal PR).

---

## Playbook B — Add a tool

1. **Write an adapter** `scoring/adapters/<tool>.py` exposing
   `parse(path, tool="<tool>") -> list[Finding]` (see `scoring/adapters/common.py` for the
   `Finding` shape). If the tool exports **SARIF**, you may not need a new adapter — just use
   `format: sarif` with `tool: <name>` in the round manifest.

2. **Register the format** in `scoring/adapters/__init__.py` (`_FORMATS` dict) if you added a
   new parser.

3. **Teach the taxonomy.** For each type the tool can report, add its rule ids/categories under
   that type's `aliases.<tool>` in `taxonomy.yaml`. A `"*"` alias means "any rule from this tool
   counts" (useful for dedicated secret scanners); a trailing `*` is a prefix match. Findings
   that carry a CWE match automatically via the shared `cwe` key.

4. **Set expectations.** Add the tool key to `expected_tools` on the ground-truth entries it
   should catch.

5. **Document it.** Add `docs/tools/<tool>.md`: how to connect (GitHub App vs CI vs CLI), its
   operating model (full-repo vs PR), the exact command to export findings, and where the output
   lands in a round.

6. **Verify** with a tiny hand-made output file and a scratch round, or extend
   `scoring/fixtures/` and `score.py --self-test`.
