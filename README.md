# trustwright

![trustwright banner](.github/images/banner.jpg)

A record of how AI agents and their harnesses actually behave, product by product and version by version, and checklists that stop a wrong answer from being accepted. A Claude Code plugin with one skill and a standard-library script.

Vendor changelogs rarely say "the model now refuses more" or "it started claiming test runs it never made". trustwright keeps your own dated, first-hand entries so you can tell.

## What you get

- **The skill** ([SKILL.md](skills/trustwright/SKILL.md)): log a behaviour, register a false-positive stop, compare versions, verify before accepting.
- **`trust.py`** (Python 3.9+, no dependencies):
  - `log`: one behaviour observation (product, version, model, kind, evidence).
  - `stop`: a false-positive stop or refusal (harness, version, model, task, source, category, verbatim message, workaround).
  - `show` and `diff`: entries per product, and what appeared or disappeared between two versions.
  - `scan <session.jsonl>`: candidate stops in a Claude Code transcript, skipping your own typed text.
  - `check --type fact|code|numbers|citation|action [--high-stakes]`: a verification checklist.
- **References**: stop and over-refusal taxonomy (OR-Bench, XSTest), verification methods, vendor sources.

Data lives in private JSONL under `TRUSTWRIGHT_HOME` (default `~/.trustwright`). Keep it out of public repos.

## Install

```
/plugin marketplace add m4bwav/trustwright
/plugin install trustwright@trustwright
```

## Tests

`python -m unittest discover -s tests` from the repo root. Eval cases and baselines: [TESTS.md](skills/trustwright/TESTS.md).

## Wiki

Wiki: link to follow once the wiki is published.

## Licence

MIT. See [LICENSE](LICENSE) and [SECURITY.md](SECURITY.md).
