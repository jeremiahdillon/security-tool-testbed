# Case template

This folder holds a copyable **ground-truth example** (`ground-truth.example.yaml`). There is no
source example here on purpose — source lives under `cases/`, and this template folder must stay
free of planted flaws.

To author a new case (full steps: [`../../docs/extending.md`](../../docs/extending.md) → "Add a case"):

1. Put realistic source under `cases/<category>/...` — embed the flaw in a coherent app.
   **No tells**: no `// vulnerable` comments, no giveaway filenames, no CWE ids. (The
   `guardrail_check.py` giveaway scan enforces this.)
2. Copy `ground-truth.example.yaml` to `ground-truth/<id>.yaml` and fill it in against
   `../ground-truth.schema.yaml`. `<id>` must equal the filename stem.
3. Run: `python3 scoring/score.py --validate && python3 scoring/guardrail_check.py`.
