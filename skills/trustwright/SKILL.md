---
name: trustwright
description: "Record and check how AI agents and harnesses behave per product and version (Claude Code, Codex, Copilot, Cursor, Gemini CLI, claude.ai): log a behaviour observation, register a false-positive safety stop or refusal (task, date, model, harness, stop source, category), scan a session transcript for stops, compare behaviour between versions, and run a verification checklist before accepting an answer. Use on 'log this refusal', 'that was a false positive stop', 'did this get worse in the new version', 'Claude Code keeps doing X since the update', 'is this answer right, check it', 'did it really run the tests', 'record that the agent hallucinated'. Not for Windows host quirks (quirkwright), context size (context-health) or whether a skill is worth its tokens (evergreen-worth)."
license: MIT
metadata:
  version: 0.1.1
---

# trustwright

Outcome: claims about agent behaviour backed by dated first-hand entries, and no answer accepted on the agent's word alone.

`TRUST` means `python scripts/trust.py` from the plugin root (run it, do not read it). Standard library only. Data is private JSONL under `TRUSTWRIGHT_HOME` (default `~/.trustwright`): `behaviour.jsonl` and `stops.jsonl`. Never commit it to a public repo.

## 1. Log a behaviour

When an agent does something notable (ignores an instruction, changes permission or mode behaviour, invents a file or API, claims a run it never made, refuses or hedges more than before):

1. Get the exact version (`claude --version`, `codex --version`, the app's About box) and the model. Never guess a version; write `unknown`.
2. `TRUST log --product claude-code --version 2.1.3 --model <id> --kind <permission|mode|instruction|tool-use|refusal|hallucination|overcaution|other> --observation "<one line>" --evidence "<transcript path, issue URL, commit>"`.
3. One observation per entry. Evidence is something another person could open; "I saw it" is not evidence.

## 2. Register a false-positive stop

A stop is a false positive when the task was legitimate and a person reading it would not object.

1. Find the source: a provider classifier hard stop (Claude Code's "Usage Policy" stop ends the turn with no model text), a model refusal (the model writes the refusal), or a harness permission block. Load [taxonomy](../../references/taxonomy.md) for categories; `--category` accepts only the names listed in `TRUST stop --help`.
2. `TRUST stop --harness claude-code --version <v> --model <id> --task "<what was asked, no secrets>" --source <provider-classifier|model-refusal|harness-permission|other> --category <topic or trigger type> --message "<verbatim>" --workaround "<what got it through, if anything>"`.
3. For a past session: `TRUST scan <session.jsonl>` proposes entries (it skips the person's own typed text). Confirm each before recording.
4. A workaround is rephrasing with the real context (purpose, ownership, safe target). Never record or use a jailbreak.

## 3. Compare versions

`TRUST show --product <p>` lists entries; `TRUST diff --product <p> --from <v1> --to <v2>` shows what appeared and disappeared. "It got worse" needs entries on both versions for the same kind of task; with only one side, say so. Vendor notes are cross-references only ([sources](../../references/sources.md)); they rarely record behaviour changes.

## 4. Verify before accepting

1. `TRUST check --type <fact|code|numbers|citation|action>` prints the checklist; add `--high-stakes` for money, health, legal, deletes or releases. Load [verify](../../references/verify.md) for the method.
2. Work the list against evidence outside the agent's prose: the tool log, the file on disk, the test output, the git diff, the source page. "Done" with no matching tool call is a fabricated claim; log it as `hallucination`.
3. High stakes: re-ask the key questions independently without the draft in view (chain-of-verification), or sample twice and treat disagreement as a warning.
4. Report each claim as verified (with the evidence), unverified, or wrong. Never upgrade unverified to verified.

## Rules

- First-hand only: an entry records something seen in this person's sessions, dated, with the version.
- No secrets, tokens or private names in `--task` or `--message`; paraphrase the sensitive part.
- A pattern ("invents package names on Codex 0.4x") needs at least two dated entries before it is stated as one.
- Asked how the agent judges copyright or recognises audio, images or people: load [media-judgement](../../references/media-judgement.md). There is no hidden detector; say what was actually checked.

## Maintenance

Sources are in [sources](../../references/sources.md). Refresh when a listed harness ships a major version or a stop signature changes. Evergreen unit: [MAINTENANCE.md](MAINTENANCE.md) (state in `evergreen.json`, tests in [TESTS.md](TESTS.md)).
