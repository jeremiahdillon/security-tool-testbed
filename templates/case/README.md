# Case template

Copy this directory's siblings when authoring a new case. Two rules that make or break the
testbed:

1. **The source you place under `cases/` must contain NO tells.** No comments like
   `// vulnerable`, no filenames like `sql_injection.js`, no CWE ids. It must read like ordinary
   application code so an LLM reviewer has to find the flaw on its own.
2. **All answers go in `ground-truth/<id>.yaml`** (copy `ground-truth.example.yaml`), never
   beside the code.

Steps: see `docs/extending.md` → "Add a case".
