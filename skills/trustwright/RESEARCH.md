# Research: trustwright

Unit: [SKILL.md](SKILL.md). Full first pass: ai-docs/research/2026-11-21-research-pass.md in the repo.

## Current understanding (2026-11-21)
- No public tool keeps a first-hand, per-version log of agent behaviour or a register of false-positive stops; neighbours repair (recover-from-false-positive), detect (hallucination-detector) or verify one answer (doublecheck).
- Claude Code's provider-classifier stop ends the turn with an "API Error ... Usage Policy" line and no model text; model refusals are written by the model; harness permission denials come back as tool results.
- Over-refusal taxonomies: OR-Bench (topic categories), XSTest (trigger types). Verification: chain-of-verification, self-consistency, claim-versus-tool-log receipts (Gotcha).

## Open questions
- Do other harnesses (Codex, Copilot CLI, Gemini CLI) leave a stable stop signature in their session files?

## Search plan
- subject: Claude Code, Codex, Copilot, Cursor, Gemini CLI changelogs; stop and refusal wording changes.
- tooling: `path:SKILL.md hallucination`, `path:SKILL.md refusal`; plugin directories for verification skills.
- practice: dated posts on false-positive stops and agents claiming unrun actions.
- testing: over-refusal and hallucination benchmarks (XSTest, OR-Bench, FalseReject, SimpleQA Verified, HalluLens).

## Log
- R-20261121-1 · subject+tooling · research pass, see the repo note · m: n/a (created)
