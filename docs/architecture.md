# Architecture & design decisions

Short ADR-style records of *why* the repo is shaped the way it is, so the decisions aren't
relitigated by a future contributor (human or agent).

## ADR-1: Ground truth lives outside the source tree

**Decision.** All answers live in `ground-truth/<id>.yaml`, never beside the code in `cases/`.

**Why.** Rule-based tools (Sonar, CodeQL, Endor, Socket) are unaffected by nearby prose, but
CodeRabbit is an LLM that reads repo context. A co-located `meta.yaml` saying "SQLi at line 42"
would let it parrot the answer instead of finding the flaw — contaminating the explainability
test. Separation keeps the reviewed surface answer-free. For the strongest isolation you can
move `ground-truth/` to a separate branch; the default (separate top-level dir) is enough as
long as PR diffs never include `ground-truth/`.

## ADR-2: Cover stories with no tells

**Decision.** Each flaw is embedded in a coherent mini-app; source contains no `// vulnerable`
comments, no giveaway filenames, no CWE ids.

**Why.** If a case is an obvious demo, tools (especially CodeRabbit) shortcut with "this is a
security test" and the result doesn't reflect real-world performance. A CI grep enforces that
tell-tale strings appear only under `ground-truth/`.

## ADR-3: Inert by design; nothing is ever installed/built/run

**Decision.** Real CVE-pinned versions and real malicious/typosquat *names* are fine as text,
but no lockfiles are committed, a per-directory `.npmrc` (in every dir with a `package.json`)
disables install scripts, each bad manifest is isolated, and CI never installs. Supply-chain
names are chosen to be removed/non-resolving.

**Why.** The only path to real harm is executing something — above all, a dependency install
that runs arbitrary install scripts. Blocking that path in layers (instruction → repo config →
CI check → Socket Firewall) makes the public repo safe to sync locally. See `docs/safety.md`.

## ADR-4: Taxonomy as data, not code

**Decision.** `taxonomy.yaml` maps canonical types ↔ CWE ↔ each tool's rule names. The harness
reads it; matching logic is generic.

**Why.** Tools name the same finding differently. Keeping the reconciliation in data means
adding a tool or a finding type is an edit to one YAML file, not a code change — essential for a
living project.

## ADR-5: Cases are delivered via PRs, and full-repo scans run on merge

**Decision.** A workflow opens PRs that introduce cases; full-repo tools scan the merged state.

**Why.** CodeRabbit and Socket are fundamentally PR-driven (CodeRabbit reviews diffs; Socket's
headline alerts fire when a PR *adds* a risky dependency). Sonar and Endor scan the whole
project (Endor's reachability needs it). To exercise every tool's real mode, cases must exist
both as diffs (PRs) and in the merged tree.

## ADR-6: CodeRabbit is scored semi-manually

**Decision.** CodeRabbit findings are transcribed into a small JSON per round; everything else
is parsed automatically (SARIF/JSON adapters).

**Why.** CodeRabbit emits prose PR comments with no clean machine export. A thin manual step
(did it flag the case? did its summary match `expected_summary`?) lets it be scored
consistently alongside the automated tools. See `results/TEMPLATE.md`.

## Scoring model (summary)

For each planted issue and each tool in its `expected_tools`, a **hit** requires a finding from
that tool whose **type matches** (via `taxonomy.yaml` alias, the taxonomy CWE, or the planted
entry's own CWE — all CWE comparisons are normalized so `CWE-089` == `CWE-89`) **and** whose
**location matches**:

- **Code categories** (sast, secrets, code-review, iac-ci): same file, within ±`LINE_TOL`
  (5) lines. A finding with no file never matches (prevents cross-case mis-attribution).
- **Dependency categories** (dependencies, supply-chain, license): matched by **exact package
  name** against the specific dependency declared on the planted line (so `crossenv` is not
  confused with `cross-env`), with purls (`pkg:npm/name@ver`) parsed to the bare name. Tools
  that instead report the manifest `file:line` fall back to location matching.

**Greedy one-to-one** matching prevents a single finding from satisfying two planted issues.
Unmatched findings that point into `cases/` are surfaced as "unmatched findings to triage"
(candidate false positives — some may be genuine extra bugs; note that FP counting is scoped to
`cases/` on purpose, so noise elsewhere is not penalized). Metrics: **precision** (n/a when a
tool reported nothing scoreable — never a misleading 1.00), **recall**, **F1**, and a `bonus`
count for correct detections outside a tool's expected set. **Explainability** (CodeRabbit) is
scored separately: its per-case summary is compared against the case's `expected_summary`.
Implementation: `scoring/score.py`.
