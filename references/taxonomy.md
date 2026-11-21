# Stop and pattern taxonomy

## Stop source (`--source`)
- `provider-classifier`: a hard stop from a safety classifier around the model. Claude Code shows an API error naming the Usage Policy and the turn has no model text. The session file can be repaired with recover-from-false-positive (https://github.com/88plug/recover-from-false-positive); log first, then repair.
- `model-refusal`: the model itself declines or answers only part ("I can't help with...").
- `harness-permission`: the harness blocks a tool call (permission rule, sandbox, auto-mode classifier). Not a model judgement.
- `other`: hedged partial answers, an agent silently skipping a tool action.

Much of a measured over-refusal rate can come from the classifier rather than the model (OR-Bench-Hard caveat), so always record the source.

## Topic category (OR-Bench, https://arxiv.org/abs/2405.20947)
deception, harassment, harmful, hate, illegal, privacy, self-harm, sexual, unethical, violence.

## Trigger type (why a safe prompt looked unsafe; XSTest, https://arxiv.org/abs/2308.01263)
homonym ("kill a process"), figurative, safe-target, safe-context (fiction, a game, a test), definition, historical, public-privacy (public figures), fictional-privacy, plus `security-research` (own systems, CTFs, defensive tooling), the most common trigger in coding agents.

## Behaviour kinds (`--kind`)
permission, mode, instruction (ignored or misapplied instruction or skill), tool-use (wrong tool, skipped tool, claimed tool call), refusal, hallucination (invented file, API, flag, result, citation), overcaution (asks for permission it has, hedges a plain answer), other.

Hallucination labels after HalluLens (https://arxiv.org/abs/2504.17550): extrinsic (contradicts the world or the source) versus intrinsic (contradicts its own input or earlier output).
