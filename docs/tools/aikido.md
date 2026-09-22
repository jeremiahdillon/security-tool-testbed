# Aikido Security

**Operating model:** full-project scans (SAST, SCA, secrets, IaC, container) via the GitHub App,
plus PR checks. Broad AppSec platform with a free tier.

**Covers here:** the widest surface after Endor — SAST cases, the secret matrix, dependency
CVEs, supply-chain, license, and IaC/CI misconfigurations.

## Connect

Install the Aikido GitHub App on the repo (free tier). No trial clock, so it can be connected in
the first onboarding wave alongside CodeRabbit/Sonar/Socket.

## Export findings for a round

Aikido can export **SARIF**, so no dedicated adapter is needed — use the SARIF adapter and
attribute it to the `aikido` tool key:

```
# export/download Aikido's SARIF for the repo, then:
```

Round manifest entry: `{format: sarif, tool: aikido, path: aikido.sarif}`.

## Notes

- SAST findings carry CWE tags, so they match via `taxonomy.yaml`'s CWE keys automatically.
- Secrets/SCA/IaC findings match via the `aikido` aliases added under `hardcoded-secret`,
  `vulnerable-dependency`, `malicious-dependency`, `license-risk`, and `iac-misconfig` in
  `taxonomy.yaml`; extend those aliases when you see unmatched Aikido rule names in a report.
- If you prefer Aikido's JSON API over SARIF, add a small `scoring/adapters/aikido.py` following
  Playbook B in `docs/extending.md`.
