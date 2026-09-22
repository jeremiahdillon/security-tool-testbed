---
name: Add a tool
about: Track onboarding a new code-review / security tool into the testbed
title: "Add tool: <tool name>"
labels: [tool]
---

Follow Playbook B in [`docs/extending.md`](../../docs/extending.md).

## Tool
- Name / vendor:
- Category: SAST / SCA / supply-chain / secrets / license / IaC / AI-review
- Operating model: full-repo scan / PR-by-PR / both
- How it connects: GitHub App / CI action / CLI

## Onboarding checklist
- [ ] Adapter added (`scoring/adapters/<tool>.py`) or confirmed it exports SARIF
- [ ] Format registered in `scoring/adapters/__init__.py` (if new)
- [ ] Taxonomy aliases added under each relevant type in `taxonomy.yaml`
- [ ] `expected_tools` updated on the ground-truth entries it should catch
- [ ] `docs/tools/<tool>.md` written (connect steps + export command + operating model)
- [ ] Verified against a sample output (scratch round or fixture)

## Export command
```
<the exact command that produces this tool's findings JSON/SARIF>
```
