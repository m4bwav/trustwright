# trustwright

![trustwright banner](.github/images/banner.jpg)

A record of how AI agents and their harnesses actually behave, product by product and version by version, and checklists that stop a wrong answer from being accepted. A Claude Code plugin with one skill and a standard-library script.

Vendor changelogs rarely say "the model now refuses more" or "it started claiming test runs it never made". trustwright keeps your own dated, first-hand entries so you can tell.

## What you get

- **The skill** ([SKILL.md](skills/trustwright/SKILL.md)): log a behaviour, register a false-positive stop, compare versions, verify before accepting.
- **`trust.py`** (Python 3.9+, no dependencies):
  - `log`: one behaviour observation (product, version, model, kind, evidence).
  - `stop`: a false-positive stop or refusal (harness, version, model, task, source, category, verbatim message, workaround).
  - `show` and `diff`: entries per product (`show --product` also lists stops whose harness has that name), and what appeared (`new`), stayed (`same`) or was not seen again (`gone?`) between two versions. Versions compare part by part as numbers, so `2.1.10` is after `2.1.9`; text versions such as `unknown` sort after numbers.
  - `scan <session.jsonl>`: candidate stops in a Claude Code transcript (at most one per line), skipping your own typed text. Candidates only: confirm each before recording it with `stop`.
  - `check --type fact|code|numbers|citation|action [--high-stakes]`: a verification checklist.
- **References**: stop and over-refusal taxonomy (OR-Bench, XSTest), verification methods, vendor sources.

Data lives in private JSONL under `TRUSTWRIGHT_HOME` (default `~/.trustwright`): `behaviour.jsonl` and `stops.jsonl`, one JSON object per line, appended and never rewritten. Keep it out of public repos.

Run the script from the plugin root: `python scripts/trust.py <command> --help` lists every option; `--kind`, `--source` and `--category` accept only the listed names.

## Install

```
/plugin marketplace add m4bwav/trustwright
/plugin install trustwright@trustwright
```

## Tests

`python -m unittest discover -s tests` (or `python -m pytest`) from the repo root. Eval cases and baselines: [TESTS.md](skills/trustwright/TESTS.md).

## Wiki

https://github.com/m4bwav/trustwright/wiki: commands with real output, the data format, recipes, FAQ and upgrading.

## Licence

MIT. See [LICENSE](LICENSE) and [SECURITY.md](SECURITY.md).
