# Purpose Check

**A judgment layer for AI agents that can execute flawlessly and still build the wrong thing.**

Purpose Check helps an agent pause at the moments that matter: before it commits to the wrong deliverable, when an assumption can change the outcome, at consequential forks, and before it hands back work that drifted away from the person it was supposed to help.

It is deliberately quiet on routine work. A clear, reversible task should move. A consequential ambiguity should get one useful question. A likely mismatch between the request and the goal should be surfaced once, with a better option attached.

Current version: **1.3.0**

## Why this exists

Modern language models are unusually good at producing artifacts. They can write the code, format the report, generate the campaign, design the system, and finish the checklist. That capability creates a subtler failure mode: the model can satisfy the request while missing the point.

Common examples:

- A polished dashboard that nobody uses to make a decision.
- A reconciliation script that preserves two systems that should have been consolidated.
- A technically correct feature that optimizes the internal abstraction while leaving the human-facing failure miserable.
- A fast default chosen because it is common in training data, even though the context points somewhere else.
- A long build completed against an assumption the user would have corrected in thirty seconds.

The usual answer is to add more requirements gathering. That often makes agents annoying. They ask five generic questions, repeat context the user already supplied, and turn a simple task into a workshop.

Purpose Check takes a different approach. It asks the agent to match the weight of its judgment to the stakes.

| Situation | Behavior |
| --- | --- |
| Clear, low-risk, reversible work | Check internally and proceed. |
| Minor ambiguity with a safe default | State the assumption briefly and keep moving. |
| Ambiguity that changes the deliverable | Ask one high-value question. |
| Likely request-to-goal mismatch | Flag it once and recommend the better fit. |
| Money, privacy, safety, authorization, legal constraints, or irreversible action | Confirm the consequential facts that are missing, stale, or uncertain. |

The result is an agent that develops better instincts without performing a philosophy seminar in the chat.

## What the skill changes

Purpose Check gives an agent four linked stages:

1. **Should this exist?** Identify the audience, the intended improvement, and whether the request is the problem or a symptom.
2. **What does done mean?** Define an end state a non-expert could verify.
3. **What happens at the forks?** Compare meaningful choices against a one-sentence purpose anchor.
4. **Did the finished work hold up?** Check for drift, misplaced quality effort, and unresolved consequential assumptions.

The purpose anchor is the structural spine: who this is for and what gets better for them. Short work can keep it internal. Longer work can write it into working notes. Every later judgment returns to the same anchor.

## What it does not do

Purpose Check does not give an agent permission to moralize, invent a better objective for the user, or override an informed permissible choice. It does not replace safety, consent, authorization, privacy, legal, or domain-specific controls.

It also does not require visible ceremony. Routine work should still feel routine.

## The review process

This skill was developed through an iterative multi-agent review loop rather than a single drafting pass. The review panel drew on **GPT 5.6**, **Claude Opus 4.8**, **Claude Fable 5**, **Gemini 3.1 Pro**, and **MAI Code 1 Flash**.

Different agents found different classes of defects:

- Broad activation language that could make the skill fire on nearly every deliverable.
- Missing deterministic gates between quiet execution, assumptions, questions, and consequential confirmation.
- An autonomy boundary that needed to separate purpose alignment from moral substitution.
- Repeated policy lists that could drift apart over time.
- A producer-consumer bug where later stages referenced a Stage 1 artifact that earlier stages did not always create.
- A conflict between explicit confirmation and the instruction to reuse rich supplied context.
- Cross-platform frontmatter rules that differ between Hermes, Anthropic's packager, and the open Agent Skills reference validator.

The process mattered because reviewers also reviewed each other. One pass scored the skill too generously. A later reviewer traced the internal stage contracts and caught the missing artifact. Another pushed back on recommendations that were locally reasonable but wrong for Anthropic's validator. That correction was tested against the actual validator source, folded into version 1.3, and preserved in the review trail.

The lesson is simple: responsiveness is cheap. Structural coherence takes adversarial reading.

### Review trail

| Artifact | Outcome |
| --- | --- |
| [Original review](reviews/01-original-review-85.pdf) | **85/100.** Strong concept, overly broad routing, missing gates and completion checks. |
| [Version 1.1 review](reviews/02-v1.1-review-96.pdf) | **96/100 at the time.** Confirmed the requested sections, but underweighted cross-section contracts. |
| [Version 1.2 review](reviews/03-v1.2-review-89.pdf) | **89/100.** Found the missing Stage 1 artifact and several local rule conflicts. |
| [Version 1.3 review](reviews/04-v1.3-review-95.pdf) | **95/100.** Behavioral contracts resolved; target-specific packaging remains the final portability task. |

The 1.3 report explicitly records which earlier recommendations were withdrawn and why. The review history stays in the repository because the corrections are part of the work.

## Install

### Prompt your agent

Paste this into an agent with filesystem and network access:

```text
Install the Purpose Check agent skill from:
https://github.com/promptclickrun/purpose-check

Before installing, inspect the repository and SKILL.md. Install version 1.3.0 under the skill name `purpose-check` using the correct user-level skills directory for your runtime. Preserve the SKILL.md body exactly. If your runtime enforces the open Agent Skills specification, use `variants/agent-skills/SKILL.md`; otherwise use the root `SKILL.md`.

After installation, verify:
1. the installed skill resolves as `purpose-check`;
2. the metadata reports version 1.3.0;
3. the description includes consequential mid-task forks;
4. the runtime can load the full body without warnings.

Do not modify global configuration or restart services. Report the installed path and verification result.
```

### Manual install: Hermes Agent

```bash
git clone https://github.com/promptclickrun/purpose-check.git
mkdir -p ~/.hermes/skills/productivity/purpose-check
cp purpose-check/SKILL.md ~/.hermes/skills/productivity/purpose-check/SKILL.md

# Verify
hermes skills list | grep purpose-check
```

Start a new session or run `/reload-skills` where supported.

Hermes can also install a raw `SKILL.md` URL:

```bash
hermes skills install \
  https://raw.githubusercontent.com/promptclickrun/purpose-check/main/SKILL.md \
  --name purpose-check
```

### Claude Code

```bash
git clone https://github.com/promptclickrun/purpose-check.git
mkdir -p ~/.claude/skills/purpose-check
cp purpose-check/SKILL.md ~/.claude/skills/purpose-check/SKILL.md
```

Restart the Claude Code session so it rebuilds the skill catalog.

### Open Agent Skills compatible runtimes

Use the strict variant. It flattens metadata values and packages the directory under the required `purpose-check` name.

```bash
git clone https://github.com/promptclickrun/purpose-check.git
mkdir -p ~/.agents/skills/purpose-check
cp purpose-check/variants/agent-skills/SKILL.md \
  ~/.agents/skills/purpose-check/SKILL.md
```

Your runtime may use a different user-level skills directory. Keep the installed directory name exactly `purpose-check`.

### Install from the packaged artifact

The repository includes two build artifacts:

- [`dist/purpose-check-v1.3.0.skill`](dist/purpose-check-v1.3.0.skill), canonical Anthropic/Hermes package
- [`dist/purpose-check-v1.3.0-agent-skills.skill`](dist/purpose-check-v1.3.0-agent-skills.skill), strict string-metadata Agent Skills package

A `.skill` file is a ZIP archive. If your runtime has no package importer, unzip it into the appropriate user-level skills directory.

## Repository layout

```text
purpose-check/
├── SKILL.md                         # Canonical Anthropic/Hermes source
├── variants/
│   └── agent-skills/SKILL.md        # Strict open-spec build
├── dist/                            # Versioned installable packages
├── reviews/                         # Full iterative review trail
├── scripts/
│   ├── build.py                     # Rebuild variants and packages
│   └── validate.py                  # Local integrity checks
├── .github/workflows/validate.yml   # CI validation
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Build and validate

```bash
python3 scripts/build.py
python3 scripts/validate.py
```

The build script keeps one behavioral body and emits target-specific frontmatter. This avoids forcing incompatible package conventions into one source file.

## Contributing

Contributions are welcome when they make the skill more predictable, less ceremonial, or easier to validate. Changes should preserve the purpose anchor, the intervention gate, supplied-context reuse, and the separation between purpose alignment and independent safety controls.

Please include a concrete scenario that fails before the change and behaves better after it. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Inspiration and thanks

Thank you to **Sterling Crispin** ([@sterlingcrispin on X](https://x.com/sterlingcrispin)) for the inspiration to create Purpose Check. The skill grew from a concern that capable systems can become excellent at execution while remaining under-equipped to ask what the execution is for, who it serves, and whether the requested artifact is the right intervention.

That concern is worth taking seriously. Better tools need better judgment, especially when they can move fast.

## License

MIT. See [LICENSE](LICENSE).
