#!/usr/bin/env python3
"""trustwright: first-hand log of how agents and harnesses behave, per product and version.

Commands: log, stop, show, diff, scan, check. Data is JSONL under TRUSTWRIGHT_HOME
(default ~/.trustwright). Standard library only.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

KINDS = ["permission", "mode", "instruction", "tool-use", "refusal", "hallucination", "overcaution", "other"]
SOURCES = ["provider-classifier", "model-refusal", "harness-permission", "other"]
# OR-Bench style categories plus XSTest trigger types (see references/taxonomy.md).
CATEGORIES = ["deception", "harassment", "harmful", "hate", "illegal", "privacy", "self-harm", "sexual",
              "unethical", "violence", "homonym", "figurative", "safe-target", "safe-context", "definition",
              "historical", "public-privacy", "fictional-privacy", "security-research", "other"]

STOP_PATTERNS = [
    ("provider-classifier", re.compile(r"(?i)(violate|against) (our|the|anthropic's) usage polic")),
    ("provider-classifier", re.compile(r"(?i)API Error:.{0,80}(usage policy|content filter|safety)")),
    ("harness-permission", re.compile(r"(?i)(permission (to use \w+ )?(was )?denied|the user doesn't want to proceed|tool use was rejected)")),
    ("model-refusal", re.compile(r"(?i)\bI (can't|cannot|won't|am not able to) (help|assist|provide|do that|comply)")),
]

CHECKS = {
    "fact": ["Name the source for each claim; open it, do not cite from memory.",
             "Check dates: is the fact still current for the version or year asked?",
             "Look for a claim with no tool call behind it in the log (stated, never fetched)."],
    "code": ["Run it, or run its tests; 'should work' is not a result.",
             "Check every API, flag and package named exists in the installed version.",
             "Diff what changed against what the answer says changed."],
    "numbers": ["Recompute each number from its inputs with a script.",
                "Check units and orders of magnitude.",
                "Match each number to the tool output it came from."],
    "citation": ["Open every URL; confirm it loads and says what is claimed.",
                 "Check titles, authors and years against the page, not the answer.",
                 "Flag any citation that appears in no tool result (likely invented)."],
    "action": ["Find the tool call that did the claimed action in the log.",
               "Check the evidence outside the transcript (file on disk, commit, PR, HTTP status).",
               "A report of 'done' with no matching call is a hallucinated action."],
}
HIGH_STAKES = ["Ask the question again in a fresh context and compare (self-consistency).",
               "Write verification questions for each claim and answer them independently (chain-of-verification).",
               "Have a second model or person review before acting."]


def home():
    p = Path(os.environ.get("TRUSTWRIGHT_HOME", Path.home() / ".trustwright"))
    p.mkdir(parents=True, exist_ok=True)
    return p


def append(name, rec):
    with open(home() / name, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load(name):
    p = home() / name
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def today():
    return dt.date.today().isoformat()


def cmd_log(a):
    rec = {"date": a.date or today(), "product": a.product, "version": a.version, "model": a.model,
           "kind": a.kind, "observation": a.observation, "evidence": a.evidence}
    append("behaviour.jsonl", rec)
    print(json.dumps(rec))
    return 0


def cmd_stop(a):
    rec = {"date": a.date or today(), "harness": a.harness, "version": a.version, "model": a.model,
           "task": a.task, "source": a.source, "category": a.category, "message": a.message,
           "workaround": a.workaround}
    append("stops.jsonl", rec)
    print(json.dumps(rec))
    return 0


def vkey(v):
    return [int(x) if x.isdigit() else x for x in re.split(r"[.\-]", v or "")]


def cmd_show(a):
    beh = [r for r in load("behaviour.jsonl") if not a.product or r["product"] == a.product]
    stops = [r for r in load("stops.jsonl") if not a.product or r["harness"] == a.product]
    if a.json:
        print(json.dumps({"behaviour": beh, "stops": stops}, indent=1))
        return 0
    for r in sorted(beh, key=lambda r: (r["product"], vkey(r["version"]), r["date"])):
        print(f"{r['product']} {r['version']} [{r['kind']}] {r['date']} {r['model'] or ''}: {r['observation']}")
    for r in stops:
        print(f"STOP {r['harness']} {r['version']} {r['date']} {r['source']}/{r['category']}: {r['task']}")
    if not beh and not stops:
        print("no entries")
    return 0


def cmd_diff(a):
    rows = [r for r in load("behaviour.jsonl") if r["product"] == a.product]
    lo, hi = vkey(a.from_v), vkey(a.to_v)
    old = {r["observation"] for r in rows if vkey(r["version"]) <= lo}
    new = [r for r in rows if lo < vkey(r["version"]) <= hi]
    print(f"{a.product}: {len(new)} observations after {a.from_v} up to {a.to_v}")
    for r in sorted(new, key=lambda r: vkey(r["version"])):
        mark = "same" if r["observation"] in old else "new"
        print(f"  {r['version']} [{r['kind']}] ({mark}) {r['observation']}")
    return 0


def texts(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from texts(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from texts(v)


def scan(path):
    hits = []
    for n, line in enumerate(Path(path).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        try:
            obj = json.loads(line)
        except ValueError:
            obj = line
        role = obj.get("type") if isinstance(obj, dict) else None
        if role == "user" and isinstance(obj.get("message", {}).get("content"), str):
            continue  # skip the person's own typed prompts
        for t in texts(obj):
            for source, rx in STOP_PATTERNS:
                m = rx.search(t)
                if m:
                    s = max(0, m.start() - 60)
                    hits.append({"line": n, "source": source, "excerpt": t[s:m.end() + 60].replace("\n", " ")})
                    break
            else:
                continue
            break
    return hits


def cmd_scan(a):
    hits = scan(a.transcript)
    if a.json:
        print(json.dumps(hits, indent=1))
    else:
        for h in hits:
            print(f"line {h['line']} {h['source']}: {h['excerpt']}")
        print(f"{len(hits)} candidate stops; record real false positives with `trust.py stop`.")
    return 0


def cmd_check(a):
    kinds = a.type or ["fact"]
    for k in kinds:
        print(f"## {k}")
        for i, c in enumerate(CHECKS[k], 1):
            print(f"{i}. {c}")
    if a.high_stakes:
        print("## high stakes")
        for i, c in enumerate(HIGH_STAKES, 1):
            print(f"{i}. {c}")
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="trust.py", description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("log", help="record a behaviour observation")
    s.add_argument("--product", required=True); s.add_argument("--version", required=True)
    s.add_argument("--model", default=""); s.add_argument("--kind", choices=KINDS, required=True)
    s.add_argument("--observation", required=True); s.add_argument("--evidence", default="")
    s.add_argument("--date"); s.set_defaults(f=cmd_log)
    s = sub.add_parser("stop", help="record a false-positive stop")
    s.add_argument("--harness", required=True); s.add_argument("--version", required=True)
    s.add_argument("--model", default=""); s.add_argument("--task", required=True)
    s.add_argument("--source", choices=SOURCES, required=True)
    s.add_argument("--category", choices=CATEGORIES, default="other")
    s.add_argument("--message", default=""); s.add_argument("--workaround", default="")
    s.add_argument("--date"); s.set_defaults(f=cmd_stop)
    s = sub.add_parser("show", help="list entries"); s.add_argument("--product")
    s.add_argument("--json", action="store_true"); s.set_defaults(f=cmd_show)
    s = sub.add_parser("diff", help="behaviour between two versions"); s.add_argument("--product", required=True)
    s.add_argument("--from", dest="from_v", required=True); s.add_argument("--to", dest="to_v", required=True)
    s.set_defaults(f=cmd_diff)
    s = sub.add_parser("scan", help="find stop signatures in a session transcript")
    s.add_argument("transcript"); s.add_argument("--json", action="store_true"); s.set_defaults(f=cmd_scan)
    s = sub.add_parser("check", help="verification checklist for an answer")
    s.add_argument("--type", action="append", choices=list(CHECKS))
    s.add_argument("--high-stakes", action="store_true"); s.set_defaults(f=cmd_check)
    a = p.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
