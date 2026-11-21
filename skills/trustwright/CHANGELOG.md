# Changelog: trustwright skill

- C-20261121-1 · created: hub skill, references, trust.py. because: new unit.
- C-20261121-2 · step 2 names `TRUST stop --help` for valid categories. because: skill-on eval stop-register first tried a free-text category (L-001).
- C-20261121-3 · 0.1.1: trust.py version keys no longer mix int and str (`unknown` crashed show and diff); diff lists `gone?` observations. because: found while writing the wiki; regression tests in tests/test_trust.py.
