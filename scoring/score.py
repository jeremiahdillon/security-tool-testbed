#!/usr/bin/env python3
"""Scoring harness for the security-tool testbed.

Modes
-----
  score.py --validate
      Validate every ground-truth/*.yaml against the schema and confirm each planted
      file:line exists in the repo. Used by pre-commit and CI.

  score.py --self-test
      Run the full pipeline against the committed fixtures (scoring/fixtures/) and assert the
      resulting matrix is correct. Proves the harness works before any real tool is wired up.

  score.py --round results/<date>
      Score a real round. The round directory must contain an `inputs.yaml`:
          inputs:
            - {format: sarif,  tool: codeql, path: codeql.sarif}
            - {format: sonar,  tool: sonar,  path: sonar.json}
            - {format: socket, tool: socket, path: socket.json}
            - {format: endor,  tool: endor,  path: endor.json}
            - {format: coderabbit, tool: coderabbit, path: coderabbit.json}
      Paths are relative to the round directory. Writes report.md into the round directory and
      prints a summary table.

See docs/methodology.md and docs/extending.md.
"""
from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapters import Finding, parse as parse_adapter  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
LINE_TOL = 5  # lines of slack when matching a finding to a planted issue
VALID_CATEGORIES = {
    "sast", "secrets", "dependencies", "supply-chain", "code-review", "license", "iac-ci",
}
VALID_SEVERITY = {"info", "low", "medium", "high", "critical"}


# --------------------------------------------------------------------------- taxonomy
class Taxonomy:
    def __init__(self, path: Path):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        self.types = data.get("types", {})

    def cwe_for(self, type_key: str) -> str | None:
        return (self.types.get(type_key) or {}).get("cwe")

    def known_type(self, type_key: str) -> bool:
        return type_key in self.types

    def matches(self, type_key: str, finding: Finding) -> bool:
        """Does a tool finding correspond to the canonical `type_key`?"""
        spec = self.types.get(type_key)
        if not spec:
            return False
        # 1) adapter already normalized rule to the canonical key (e.g. socket).
        if finding.rule and finding.rule.lower() == type_key.lower():
            return True
        # 2) CWE match.
        want_cwe = spec.get("cwe")
        if want_cwe and finding.cwe and finding.cwe.upper() == str(want_cwe).upper():
            return True
        # 3) per-tool alias match.
        aliases = (spec.get("aliases") or {}).get(finding.tool, []) or []
        rule = (finding.rule or "").lower()
        for alias in aliases:
            a = str(alias).lower()
            if a == "*":
                return True
            if a.endswith("*") and rule.startswith(a[:-1]):
                return True
            if a == rule:
                return True
        return False


# --------------------------------------------------------------------------- ground truth
@dataclass
class Planted:
    type: str
    cwe: str | None
    severity: str
    file: str
    line: int
    expected_tools: list[str]
    detail: str = ""
    case_id: str = ""
    category: str = ""


@dataclass
class Case:
    id: str
    category: str
    language: str
    title: str
    expected_summary: str = ""
    notes: str = ""
    planted: list[Planted] = field(default_factory=list)


def load_cases(gt_dir: Path) -> list[Case]:
    cases: list[Case] = []
    for f in sorted(gt_dir.glob("*.yaml")):
        data = yaml.safe_load(f.read_text(encoding="utf-8"))
        planted = [
            Planted(
                type=p["type"],
                cwe=p.get("cwe"),
                severity=p.get("severity", ""),
                file=p["file"],
                line=int(p["line"]),
                expected_tools=list(p.get("expected_tools", [])),
                detail=p.get("detail", ""),
                case_id=data["id"],
                category=data.get("category", ""),
            )
            for p in data.get("planted", [])
        ]
        cases.append(
            Case(
                id=data["id"],
                category=data.get("category", ""),
                language=data.get("language", ""),
                title=data.get("title", ""),
                expected_summary=data.get("expected_summary", ""),
                notes=data.get("notes", ""),
                planted=planted,
            )
        )
    return cases


# --------------------------------------------------------------------------- validation
def validate(gt_dir: Path, root: Path, tax: Taxonomy) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    files = sorted(gt_dir.glob("*.yaml"))
    if not files:
        return [f"no ground-truth records found in {gt_dir}"]
    for f in files:
        try:
            data = yaml.safe_load(f.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errors.append(f"{f.name}: invalid YAML: {e}")
            continue
        cid = data.get("id")
        if not cid:
            errors.append(f"{f.name}: missing 'id'")
        else:
            if cid != f.stem:
                errors.append(f"{f.name}: id '{cid}' does not match filename stem '{f.stem}'")
            if cid in seen_ids:
                errors.append(f"{f.name}: duplicate id '{cid}'")
            seen_ids.add(cid)
        if data.get("category") not in VALID_CATEGORIES:
            errors.append(f"{f.name}: category '{data.get('category')}' not in {sorted(VALID_CATEGORIES)}")
        planted = data.get("planted") or []
        if not planted:
            errors.append(f"{f.name}: needs at least one planted finding")
        for i, p in enumerate(planted):
            where = f"{f.name} planted[{i}]"
            if not tax.known_type(p.get("type", "")):
                errors.append(f"{where}: unknown type '{p.get('type')}' (add it to taxonomy.yaml)")
            if p.get("severity") not in VALID_SEVERITY:
                errors.append(f"{where}: severity '{p.get('severity')}' not in {sorted(VALID_SEVERITY)}")
            if not p.get("expected_tools"):
                errors.append(f"{where}: expected_tools is empty")
            # file:line existence
            fp = root / p.get("file", "")
            if not fp.is_file():
                errors.append(f"{where}: file '{p.get('file')}' does not exist")
            else:
                nlines = len(fp.read_text(encoding="utf-8", errors="replace").splitlines())
                line = p.get("line")
                if not isinstance(line, int) or line < 1 or line > nlines:
                    errors.append(f"{where}: line {line} out of range (file has {nlines} lines)")
    return errors


# --------------------------------------------------------------------------- scoring
@dataclass
class ToolScore:
    tp: int = 0
    fn: int = 0
    fp: int = 0
    bonus: int = 0  # detected but not in expected_tools
    missed: list[str] = field(default_factory=list)
    false_positives: list[str] = field(default_factory=list)

    def precision(self) -> float:
        d = self.tp + self.fp
        return self.tp / d if d else 1.0

    def recall(self) -> float:
        d = self.tp + self.fn
        return self.tp / d if d else 1.0

    def f1(self) -> float:
        p, r = self.precision(), self.recall()
        return 2 * p * r / (p + r) if (p + r) else 0.0


def _finding_matches_planted(f: Finding, p: Planted, tax: Taxonomy) -> bool:
    if not tax.matches(p.type, f):
        return False
    ff = f.norm_file()
    if ff and ff != p.file:
        return False
    if f.line is not None and abs(f.line - p.line) > LINE_TOL:
        return False
    return True


def score_round(cases: list[Case], findings_by_tool: dict[str, list[Finding]], tax: Taxonomy):
    planted_all = [p for c in cases for p in c.planted]
    tools = set(findings_by_tool)
    scores: dict[str, ToolScore] = {t: ToolScore() for t in tools}
    # Detection matrix: case_id -> planted idx -> {tool: bool}
    detail_rows = []

    # Greedy matching so one finding satisfies at most one planted issue.
    consumed: dict[str, set[int]] = {t: set() for t in tools}

    for p in planted_all:
        row = {"case": p.case_id, "type": p.type, "loc": f"{p.file}:{p.line}", "tools": {}}
        for t in tools:
            hit_idx = None
            for i, f in enumerate(findings_by_tool[t]):
                if i in consumed[t]:
                    continue
                if _finding_matches_planted(f, p, tax):
                    hit_idx = i
                    break
            detected = hit_idx is not None
            if detected:
                consumed[t].add(hit_idx)
            expected = t in p.expected_tools
            row["tools"][t] = ("hit" if detected else "miss") if expected else (
                "bonus" if detected else "-"
            )
            if expected:
                if detected:
                    scores[t].tp += 1
                else:
                    scores[t].fn += 1
                    scores[t].missed.append(f"{p.case_id} ({p.type} @ {p.file}:{p.line})")
            elif detected:
                scores[t].bonus += 1
        detail_rows.append(row)

    # False positives: unconsumed findings that point into cases/ files.
    for t in tools:
        for i, f in enumerate(findings_by_tool[t]):
            if i in consumed[t]:
                continue
            ff = f.norm_file() or ""
            if ff.startswith("cases/"):
                scores[t].fp += 1
                scores[t].false_positives.append(f"{f.rule or f.message[:40]} @ {ff}:{f.line}")

    return scores, detail_rows


# --------------------------------------------------------------------------- round I/O
def load_round(round_dir: Path) -> dict[str, list[Finding]]:
    manifest = round_dir / "inputs.yaml"
    if not manifest.is_file():
        raise SystemExit(f"round manifest not found: {manifest}")
    spec = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    findings_by_tool: dict[str, list[Finding]] = {}
    for entry in spec.get("inputs", []):
        fmt, tool, rel = entry["format"], entry.get("tool", entry["format"]), entry["path"]
        path = round_dir / rel
        fs = parse_adapter(fmt, str(path), tool=tool)
        findings_by_tool.setdefault(tool, []).extend(fs)
    return findings_by_tool


def render_report(cases, scores, detail_rows) -> str:
    tools = sorted(scores)
    out = ["# Round report", ""]
    out.append("## Summary")
    out.append("")
    out.append("| tool | precision | recall | F1 | TP | FN | FP | bonus |")
    out.append("|---|---|---|---|---|---|---|---|")
    for t in tools:
        s = scores[t]
        out.append(
            f"| {t} | {s.precision():.2f} | {s.recall():.2f} | {s.f1():.2f} | "
            f"{s.tp} | {s.fn} | {s.fp} | {s.bonus} |"
        )
    out.append("")
    out.append("## Detection matrix")
    out.append("")
    out.append("| case | type | location | " + " | ".join(tools) + " |")
    out.append("|---|---|---|" + "|".join(["---"] * len(tools)) + "|")
    for r in detail_rows:
        cells = " | ".join(r["tools"].get(t, "-") for t in tools)
        out.append(f"| {r['case']} | {r['type']} | {r['loc']} | {cells} |")
    out.append("")
    # Misses / FPs detail
    for t in tools:
        s = scores[t]
        if s.missed:
            out.append(f"### {t}: missed ({len(s.missed)})")
            out += [f"- {m}" for m in s.missed]
            out.append("")
        if s.false_positives:
            out.append(f"### {t}: unmatched findings to triage ({len(s.false_positives)})")
            out += [f"- {m}" for m in s.false_positives]
            out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------- self-test
def self_test() -> int:
    fx = REPO / "scoring" / "fixtures"
    tax = Taxonomy(fx / "taxonomy.yaml") if (fx / "taxonomy.yaml").exists() else Taxonomy(REPO / "taxonomy.yaml")
    cases = load_cases(fx / "ground-truth")
    verrs = validate(fx / "ground-truth", fx, tax)
    if verrs:
        print("SELF-TEST FAILED (fixture validation):")
        for e in verrs:
            print("  -", e)
        return 1
    findings = load_round(fx / "round")
    scores, rows = score_round(cases, findings, tax)
    # Expected: codeql detects the SQLi (hit); sonar misses it (expected but miss);
    # socket detects the malicious dep; and there is exactly one FP for codeql.
    ok = True
    checks = {
        ("codeql", "tp", 1),
        ("codeql", "fp", 1),
        ("sonar", "fn", 1),
        ("socket", "tp", 1),
    }
    for tool, attr, want in checks:
        got = getattr(scores.get(tool, ToolScore()), attr)
        status = "ok" if got == want else "MISMATCH"
        if got != want:
            ok = False
        print(f"  {tool}.{attr}: got {got}, want {want} [{status}]")
    print(render_report(cases, scores, rows))
    print("\nSELF-TEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


# --------------------------------------------------------------------------- main
def main() -> int:
    ap = argparse.ArgumentParser(description="Score the security-tool testbed.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--validate", action="store_true", help="validate ground-truth records")
    g.add_argument("--self-test", action="store_true", help="run pipeline against fixtures")
    g.add_argument("--round", metavar="DIR", help="score a round directory")
    args = ap.parse_args()

    tax = Taxonomy(REPO / "taxonomy.yaml")

    if args.validate:
        errs = validate(REPO / "ground-truth", REPO, tax)
        if errs:
            print("Ground-truth validation FAILED:")
            for e in errs:
                print("  -", e)
            return 1
        print("Ground-truth validation passed.")
        return 0

    if args.self_test:
        return self_test()

    round_dir = Path(args.round)
    cases = load_cases(REPO / "ground-truth")
    findings = load_round(round_dir)
    scores, rows = score_round(cases, findings, tax)
    report = render_report(cases, scores, rows)
    (round_dir / "report.md").write_text(report, encoding="utf-8")
    print(report)
    print(f"\nWrote {round_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
