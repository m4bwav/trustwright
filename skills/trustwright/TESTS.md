# Tests: trustwright

Cases: [evals/evals.json](evals/evals.json); scratch homes under `<TMP>/tw-evals/<case-id>/home` via TRUSTWRIGHT_HOME. Script tests: `python -m unittest discover -s tests` (or `pytest`) from the repo root. A case passes on evidence outside the transcript.

Entry shape: `### T-YYYYMMDD-n · date · harness · env · passed/total`. Newest first.

## Runs

### T-20261121-1 · 2026-11-21 · claude-code, one subagent per run · baseline and skill-on, 1 run each · skill-on 2/2, baseline 1/2
- stop-register: baseline fail on evidence (an ad hoc markdown table with the fields; no machine-readable register, no stop-source taxonomy, nothing `show` or `diff` can read). Skill-on pass: stops.jsonl entry, source provider-classifier, category security-research, verbatim message; one rejected category on the first try (L-001).
- claimed-tests: baseline pass (the bare model spotted the missing test call and said do not merge). Skill-on pass, plus `trust.py check --type action` and a hallucination entry logged. The skill adds the record, not the verdict.
- Not run (owed in the next normal suite): scan-session, log-hallucination, version-diff-one-side, three decoys.
- Unit tests: 6/6 pass.
- led to: L-001, C-20261121-2
