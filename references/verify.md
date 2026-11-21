# Verifying an answer

`python scripts/trust.py check --type <t>` prints the short list. The method behind it:

## Evidence outside the prose
The agent's summary is a claim, not evidence. Cross-check it against the raw record (the receipt-from-log idea of Gotcha, https://arsovskidev.github.io/gotcha/):
- Claimed file edits: read the file or `git diff`.
- Claimed test passes: the test command and its output are in the tool log, after the last edit.
- Claimed command results: the command ran and its output says what the answer says.
- "Done" with no tool call behind it: fabricated. Log it.

## Facts and citations
- Each factual claim links to a source or to a tool output from this session.
- Open each cited URL and check it says what is claimed. A real URL with a wrong claim is the common failure.
- Version, API and flag facts: check against the changelog or the installed tool's `--help`.
- Label each claim as doublecheck does (https://awesome-copilot.github.com/plugin/doublecheck/): verified (with link), plausible, fabrication risk. A model checking itself shares its own blind spots; prefer a tool or a person for the deciding check.

## Numbers
Recompute with a script, check units and orders of magnitude, and trace each input to its source.

## High stakes: escalate
- Chain-of-Verification (https://arxiv.org/abs/2309.11495): draft, plan verification questions, answer them independently without the draft in view, revise.
- Self-consistency (https://arxiv.org/abs/2203.11171): sample several answers; disagreement is a warning.
- SelfCheckGPT (https://arxiv.org/abs/2303.08896): consistency across samples without outside resources.
- Abstaining beats guessing: SimpleQA grades correct, incorrect or not attempted (https://openai.com/index/introducing-simpleqa/).
