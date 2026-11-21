# trustwright research pass (2026-11-21)

Short web pass (searches plus one paper fetch) for a private plugin that tracks how AI agents and harnesses behave per product and version. Neighbours it must not duplicate: quirkwright (Windows host quirks), context-health (context size), evergreen-worth (skill value).

Each source has a status: **[checked]** means seen in search results or fetched today. **[known]** means a standard URL from prior knowledge that was not re-fetched today, so check it before relying on it.

## 1. Existing tools

| Tool | What it does | Overlap with trustwright | Source |
|---|---|---|---|
| doublecheck (github/awesome-copilot) | Three layers: extract the claims, search the web for each, then an adversarial pass for hallucination patterns. Labels each claim VERIFIED (with link), PLAUSIBLE or FABRICATION RISK. Runs persistent or one-shot. Its own page says the same model checks its own output. | Answer verification. The closest existing piece to reuse. | https://awesome-copilot.github.com/plugin/doublecheck/ [checked] |
| recover-from-false-positive (88plug) | Repairs Claude Code session JSONL after a "cyber safeguards / Usage Policy" hard stop. Removes the triggering turn and re-links parentUuid so `claude --resume` works. | Handles a false-positive safety stop, but repairs instead of logging. Gives a signature to detect stops. | https://claudepluginhub.com/plugins/88plug-recover-from-false-positive [checked]; repo github.com/88plug/recover-from-false-positive |
| hallucination-detector (bitflight-devops) | Claude Code marketplace plugin. Detects hallucinations. Not checked whether it keeps a log. | Detection only. | https://awesome.ecosyste.ms/projects/github.com%2Fbitflight-devops%2Fhallucination-detector [checked] |
| anti-hallucination-skill (clawhub) | Prompt-style skill to reduce fabrication. | Behaviour nudge only, no record. | https://implexa.ai/s/clawhub/anti-hallucination-skill [checked] |
| Gotcha (arsovskidev) | Hooks write a receipt from the raw tool log, separately from the model's own prose summary. | Pattern to reuse: compare what the agent claims with what the tool log shows. | https://arsovskidev.github.io/gotcha/ [checked] |
| vercel plugin-audit | Audits plugins from Claude Code JSONL transcripts. | Shows how to mine transcripts. Not about trust. | https://skills.sh/vercel-labs/vercel-plugin/plugin-audit [checked] |
| cc-safe-setup hook catalogue | Lists Claude Code hooks by event and whether each can refuse. | Background for hook-based capture. | https://leanpub.com/read/claude-code-safety-field-manual/a-catalogue-of-every-hook-in-cc-safe-setup-which-event-each-runs-on-and-whether-it-can-refuse-chapter-10 [checked] |
| claudeissues.com | Mirror of Claude Code GitHub issues, e.g. #54992 (skill ignored, hallucination escalating across correction rounds). | Source of community behaviour reports. | https://claudeissues.com/issue/54992-bug-report-claude-code-repeatedly-violates-loaded-workflow-skill-escalates-hallu [checked] |
| dev.to Claude Code quality logs | One user re-ran prompts others reported as broken and compared logs. | Shows the method for a per-version behaviour log. | https://dev.to/jtorchia/claude-code-quality-reports-i-ran-the-same-prompts-that-broke-everyone-and-heres-what-my-logs-2ehg [checked] |

No tool was found that keeps a per-product, per-version behaviour log or a false-positive safety-stop register across harnesses.

## 2. Over-refusal benchmarks (taxonomy for the register)

- **XSTest** (Rottger et al., 2023): 250 safe prompts that look unsafe, plus 200 contrast prompts that are unsafe. Ten safe prompt types: homonyms, figurative language, safe targets, safe contexts, definitions, real discrimination against nonsense groups, nonsense discrimination against real groups, historical events, privacy (public figures), privacy (fictional). Considered saturated for frontier models. https://arxiv.org/abs/2308.01263 [known]
- **OR-Bench** (Cui et al.): 80k seemingly toxic prompts, a ~1k hard subset and 600 toxic controls. Ten categories (Table 2): deception, harassment, harmful, hate, illegal, privacy, self-harm, sexual, unethical, violence. https://arxiv.org/abs/2405.20947 [checked, fetched]
- **PHTest** (pseudo-harmful prompts): sources disagree on the size (2,027 or 3,260). Cited in the FalseReject comparison. [checked, via FalseReject]
- **FalseReject** (2025): adversarial benign prompts with structured-reasoning responses. Gives rejection rates per model on XSTest, PHTest and OR-Bench, e.g. Claude 3.5 Sonnet 13.2 / 25.6 / 8.5. https://arxiv.org/abs/2505.08054 [checked]
- **Persona prompts and false refusal** (2025): the stated persona changes refusal rates. https://arxiv.org/abs/2509.08075 [checked]
- **Caveat:** a provider-side input classifier can cause much of a measured refusal rate (OR-Bench-Hard). In the register, record whether the stop came from a classifier or from the model.

Proposed register taxonomy: the OR-Bench topic category, plus the XSTest trigger type (why it looked unsafe: homonym, figurative, safe context, fiction, security or cyber work, and so on), plus the stop source (classifier hard stop, model refusal, hedged partial, or an agent that declines a tool action).

## 3. Hallucination and calibration evals, and verification techniques

- **SimpleQA** (OpenAI, 2024): short-form factuality, graded correct, incorrect or not attempted. That three-way grading fits a "did it abstain" field. https://openai.com/index/introducing-simpleqa/ [known]
- **SimpleQA Verified** (Google DeepMind, 2025): 1,000 cleaned prompts with deduplicated and reconciled ground truth. https://arxiv.org/abs/2509.07968 [checked]
- **HalluLens** (Meta FAIR, 2025): separates extrinsic hallucination (dynamically generated test sets) from intrinsic hallucination, and separates hallucination from factuality. That split is useful for pattern labels. https://arxiv.org/abs/2504.17550 [checked]
- **Chain-of-Verification (CoVe)** (Dhuliawala et al., 2023): draft an answer, plan verification questions, answer them independently without the draft in view, then revise. https://arxiv.org/abs/2309.11495 [known]
- **Self-consistency** (Wang et al., 2022): sample several reasoning paths and take the majority. A disagreement between samples is a cheap warning sign. https://arxiv.org/abs/2203.11171 [known]
- **SelfCheckGPT** (Manakul et al., 2023): checks consistency across samples without outside resources. https://arxiv.org/abs/2303.08896 [known]
- **Citation and claim checks:** doublecheck's extract, search and label pipeline (section 1). For code agents, the matching check is evidence outside the transcript: run the test, read the file, check the git diff (the Gotcha pattern).

Checklist seeds for trustwright: (1) Is every factual claim linked to a source or a tool output from this session? (2) Has every claimed file, test or command result been confirmed from the tool log? (3) For version or API facts, has the date been checked against the changelog? (4) For a high-stakes answer, run CoVe-style independent re-asks. (5) Did the agent say "done" without running anything? That is a known agent pattern.

## 4. Where vendors publish per-version behaviour changes

| Product | Source | Status |
|---|---|---|
| Claude Code | https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md ; `claude --version`; GitHub issues | [known] |
| Claude models | https://www.anthropic.com/system-cards (system cards cover over-refusal, sycophancy, reward hacking); https://docs.anthropic.com/en/release-notes/overview | [known] |
| claude.ai apps | https://support.anthropic.com (release notes) | [known] |
| Codex CLI | https://github.com/openai/codex/releases ; https://developers.openai.com/codex/changelog | [known] |
| OpenAI models | https://openai.com/index/ (system cards); https://help.openai.com/en/articles/9624314-model-release-notes | [known] |
| GitHub Copilot | https://github.blog/changelog/ (label: copilot) | [known] |
| Cursor | https://cursor.com/changelog | [known] |
| Gemini CLI | https://github.com/google-gemini/gemini-cli/releases ; Gemini model cards at https://deepmind.google/models/ | [known] |

These are mostly feature notes. Behaviour changes such as more or fewer refusals, or laziness, rarely appear in them. System cards give model-level refusal and hallucination numbers but not harness-level ones. The behaviour log therefore has to be first-hand: date, product, version, model, task, what happened and evidence. Vendor notes are only cross-references.

## Gap

No existing tool:
1. keeps a durable **per-product, per-version behaviour log** across Claude Code, Codex, Copilot, Cursor, Gemini CLI and claude.ai;
2. keeps a **false-positive safety-stop register** (task, date, model, harness, stop source, category) that the user can search later. recover-from-false-positive only repairs the session file;
3. links observed **hallucination or overcaution patterns** to versions, so "this got worse in 2.x" can be shown with evidence;
4. pairs a doublecheck-style claim check with **tool-log evidence checks** for coding agents, kept as checklists to run before accepting an answer.

Reuse: the OR-Bench and XSTest taxonomy, doublecheck's labels, CoVe and self-consistency as escalation steps, the Gotcha receipt-from-log pattern, and the 88plug stop signature for automatic detection.
