# Sonar (SonarQube / SonarCloud)

**Operating model:** full-project analysis on branches, plus pull-request decoration of the
diff. Fundamentally whole-repo.

**Covers here:** SAST (SQLi, command injection, SSRF, path traversal, weak crypto, insecure
deserialization, XXE), hardcoded secrets, some dependency and IaC findings.

## Connect

- SonarCloud: sign in with GitHub, import this repo (it's public), and add the project.
- CI: the workflow `.github/workflows/sonar.yml` runs the scan. Set repo secret `SONAR_TOKEN`
  (and `SONAR_HOST_URL` if self-hosted). Adjust `sonar-project.properties` if needed.

## Export findings for a round

Web API (issues) — recommended, parsed by the `sonar` adapter:
```bash
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/issues/search?componentKeys=$PROJECT_KEY&resolved=false&ps=500" \
  > results/<date>/sonar.json
```
Round manifest entry: `{format: sonar, tool: sonar, path: sonar.json}`.

Alternatively export SARIF and use `{format: sarif, tool: sonar, path: sonar.sarif}`.

## Notes

- Sonar's rule ids (e.g. `javascript:S3649`) are mapped in `taxonomy.yaml`. Add any missing
  ids there when you see unmatched findings in a report.
- Security "hotspots" are separate from "issues"; the adapter also reads a `hotspots` array if
  present.
