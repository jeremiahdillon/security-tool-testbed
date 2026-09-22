# Socket

**Operating model:** **pull-request alerts** (fires when a PR adds/changes a risky dependency)
plus a full-project dependency view. Server-side — Socket reads manifests, it does not install.

**Covers here:** supply-chain (typosquats, malicious packages), dependency CVEs, and license
signals. Socket does not do code SAST or secret scanning.

## Connect

Install the Socket GitHub App on this repo. New-dependency alerts appear on PRs that add them,
so deliver `cases/dependencies/*` and `cases/supply-chain/*` via PRs (`land-case-prs`).

## Export findings for a round

Use the Socket CLI or API to emit JSON, then point the `socket` adapter at it:
```bash
# example — adjust to your Socket CLI version
socket report create cases/supply-chain/package.json --json > results/<date>/socket.json
```
Round manifest entry: `{format: socket, tool: socket, path: socket.json}`. The adapter walks
the JSON for alert objects and maps `type` (malware/typosquat/installScripts → malicious;
cve → vulnerable) via `taxonomy.yaml`.

## Socket Firewall (`sfw`) — runtime enforcement + optional prevention test

- **Enforcement backstop.** If `sfw` is installed locally it blocks a flagged package *before*
  download, so even an accidental `npm install`/`pip install` in a bad-manifest dir is stopped.
  In this environment, package installs must be run through `sfw` (e.g. `sfw pip3 install ...`).
- **Optional, manual-only prevention test.** To test Socket's *prevention* layer (distinct from
  detection), deliberately attempt an install in a throwaway/quarantined copy of a
  supply-chain manifest behind `sfw` and confirm it refuses. Because `sfw` checks intel before
  fetching, this exercises the block path even for removed packages — no live payload runs.
  **Never wire this into default CI.**

## Socket MCP — case authoring aid

If the Socket MCP server is available, query it while authoring supply-chain cases to confirm
each planted package name is actually recognized by Socket's intelligence — i.e. that the case
is a real positive the tool should flag.
