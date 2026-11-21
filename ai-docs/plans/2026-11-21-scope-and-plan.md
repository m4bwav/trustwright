# trustwright scope and plan (2026-11-21)

Private plugin (agent's ruling, flagged: not an everscout beat, since vendor changelogs rarely record behaviour; the log must be first-hand). One hub skill `trustwright`, references on demand, stdlib `scripts/trust.py`.

## Data (private, under TRUSTWRIGHT_HOME, default ~/.trustwright; JSONL)
- `behaviour.jsonl`: product, version, model, date, observation, evidence link, kind (permission, mode, instruction-following, tool use, refusal, hallucination).
- `stops.jsonl`: false-positive stop register: task, date, model, harness, version, stop source (provider classifier, model refusal, harness permission), category (OR-Bench 10 / XSTest trigger types), verbatim message, workaround.

## trust.py
- `log` / `stop`: append an entry (validates fields).
- `scan TRANSCRIPT`: find hard-stop signatures (Claude Code "Usage Policy" stop, refusal phrases) in a session JSONL and propose stop entries.
- `show` / `diff --product X --from V1 --to V2`: behaviour per version.
- `check ANSWER`: prints the verification checklist for the answer type (fact, code, numbers, citations), with tool-log cross-check steps (Gotcha idea) and escalation (chain-of-verification, self-consistency) for high stakes.
- Tests: unittest with fixture transcripts, no live calls.

## References
taxonomy.md (OR-Bench/XSTest categories, stop sources), verify.md (checklists; doublecheck route when installed), sources.md (vendor changelogs and system cards as cross-references).

## Order
1. trust.py log/stop/show + tests. 2. scan + check. 3. SKILL.md + references. 4. evergreen unit, evals with baseline. 5. README with banner, marketplace install, release. Public question on an askwright page near release.
