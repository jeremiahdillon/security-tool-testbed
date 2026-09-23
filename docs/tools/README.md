# Tool coverage status

`expected_tools` in the ground truth names every tool that *should* catch a given finding —
including tools that don't yet have a scoring adapter. The harness only scores a tool that is
present in a round's `inputs.yaml`; an expected tool with no adapter is simply not scored (it is
never counted as a "miss" against the tool). This table tracks what's wired up.

| Tool key | Category | Adapter | Setup doc | Notes |
|---|---|---|---|---|
| `codeql` | SAST | ✅ SARIF | (built-in workflow) | Free baseline for JS/TS, Python, Java. Not configured to scan the Dockerfile/Actions IaC cases here — those are covered by Sonar/Aikido. |
| `sonar` | SAST + some SCA | ✅ `sonar` / SARIF | `sonar.md` | Automatic Analysis (no token) is the simplest mode; CI via `SONAR_TOKEN` optional. |
| `socket` | SCA + supply-chain | ✅ `socket` | `socket.md` | PR-driven; matched by package name. |
| `endor` | SCA + SAST + secrets + IaC | ⚠️ `endor` (blocked) | `endor.md` | **Tenant-gated — no self-serve free tier.** Scanning needs a provisioned Endor tenant; the `agenthq` GitHub app is a separate read-only Copilot plugin, not the scanner. |
| `coderabbit` | AI review | ✅ `coderabbit` (semi-manual) | `coderabbit.md` | Explainability graded via `summary_matched`. |
| `gitar` | AI review (Sonar-owned) | ✅ `gitar` (semi-manual) | `gitar.md` | **~14-day trial.** ⚠️ Can auto-*fix* (write access) — never apply/merge its fixes (would patch fixtures). |
| `aikido` | SAST + SCA + secrets + IaC | ✅ SARIF (`--tool aikido`) | `aikido.md` | Free tier; broad coverage. SAST matches by CWE; SCA/secret/IaC via `aikido` aliases. |
| `gitleaks` | Secrets | ❌ planned | — | SARIF-capable; can be added via the sarif adapter with `tool: gitleaks`. |
| `trufflehog` | Secrets | ❌ planned | — | Used already for pre-push verification (see `../safety.md`); JSON adapter TODO. |
| `github` | Secrets (GitHub secret scanning) | ❌ planned | — | Alerts via API; no adapter yet. |
| `dependabot` | SCA | ❌ planned | — | Alerts via API; no adapter yet. |

To add any of the ❌ tools, follow Playbook B in [`../extending.md`](../extending.md).
