# Endor Labs

**Operating model:** full-project analysis (SCA with reachability, SAST, secrets, CI/CD
posture), run in CI on branches, plus PR checks. Reachability analysis needs the whole project.

**Covers here:** the broadest surface — dependency CVEs (with reachability), supply-chain,
SAST, secrets, license, and IaC/CI posture.

## Connect

Install the Endor Labs GitHub App, or run `endorctl` in CI with a namespace/API key. For SCA,
Endor resolves dependencies from the manifests without installing them.

## Export findings for a round

```bash
# example — adjust to your endorctl version/flags
endorctl scan --output-type json > results/<date>/endor.json
```
Round manifest entry: `{format: endor, tool: endor, path: endor.json}`. The adapter reads a
`findings` (or `results`) array; it also captures a `reachable` flag into `extra` so you can
compare reachable vs. total in your notes.

## Notes

- Map Endor's finding categories to canonical types under `aliases.endor` in `taxonomy.yaml`.
- Reachability is an Endor differentiator worth calling out in `results/<date>/notes.md`: for
  the dependency cases, note which CVEs Endor marks reachable vs. merely present.
