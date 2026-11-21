# Changelog

## 0.1.1 (2026-11-21)
- Fix: `show` and `diff` crashed with a TypeError when a version had a text part (`unknown`, which the skill tells you to write, or `2.1.0-beta`). Number parts now sort before text parts.
- Fix: `diff` now lists observations not seen after the `--from` version (`gone?`), as the README and skill promised; 0.1.0 listed only new and repeated ones.
- README: data files, `--help`, how versions compare, `scan` candidates, wiki link.

## 0.1.0 (2026-11-21)
- First release: trustwright hub skill, references (taxonomy, verify, sources), `scripts/trust.py` (log, stop, show, diff, scan, check), unit tests, evergreen unit with an eval suite and baselines.
