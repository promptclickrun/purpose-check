# Purpose Check

**A portable judgment layer for tool-calling AI agents that can execute flawlessly and still build the wrong thing.**

Purpose Check is a single [`SKILL.md`](SKILL.md) file. No package manager. No proprietary bundle. No runtime lock-in.

Drop it into any harness that can load Markdown instructions, agent skills, system-prompt extensions, project rules, or reusable tool-calling workflows.

Current version: **1.3.0**

Author: **Colt Coan**

[View the interactive GitHub Page](https://promptclickrun.github.io/purpose-check/)

## Why this exists

Modern language models are unusually good at producing artifacts. They can write the code, format the report, generate the campaign, design the system, and finish the checklist. That capability creates a subtler failure mode: the model can satisfy the request while missing the point.

Common examples:

- A polished dashboard that nobody uses to make a decision.
- A reconciliation script that preserves two systems that should have been consolidated.
- A technically correct feature that optimizes the internal abstraction while leaving the human-facing failure miserable.
- A fast default chosen because it is common in training data, even though the context points somewhere else.
- A long build completed against an assumption the user would have corrected in thirty seconds.

The usual answer is more requirements gathering. That often makes agents annoying. They ask five generic questions, repeat context the user already supplied, and turn a simple task into a workshop.

Purpose Check takes a different approach. It matches the weight of the judgment to the stakes.

| Situation | Behavior |
| --- | --- |
| Clear, low-risk, reversible work | Check internally and proceed. |
| Minor ambiguity with a safe default | State the assumption briefly and keep moving. |
| Ambiguity that changes the deliverable | Ask one high-value question. |
| Likely request-to-goal mismatch | Flag it once and recommend the better fit. |
| Money, privacy, safety, authorization, legal constraints, or irreversible action | Confirm the consequential facts that are missing, stale, or uncertain. |

The result is an agent with better judgment that still knows when to shut up and work.

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

## Works with any agent harness

The repository uses the broadly adopted `SKILL.md` convention: YAML frontmatter followed by Markdown instructions. The useful part is the Markdown body. A harness can consume it in several ways:

- Discover it from a user-level or project-level skills directory.
- Load it as a reusable prompt or instruction module.
- Inject it into a system prompt when its description matches the task.
- Attach it to an agent profile, tool-calling workflow, or project rules file.
- Copy the body into a harness-specific skill editor.

If your system recognizes `SKILL.md`, install the file directly. If it uses another filename or schema, preserve the body and translate only the small frontmatter block.

## Install

### Prompt your agent

Paste this into any tool-calling agent with filesystem and network access:

```text
Install the Purpose Check skill from:
https://github.com/promptclickrun/purpose-check

Inspect the repository and read SKILL.md before installing it. Add the skill under the name `purpose-check` using the user-level or project-level skill location supported by this harness. Install the canonical SKILL.md directly. Do not convert it into a proprietary archive or package format.

If this harness does not support SKILL.md discovery, preserve the Markdown instruction body and adapt only the frontmatter or filename required by the harness.

After installation, verify:
1. the skill resolves as `purpose-check`;
2. the metadata reports version 1.3.0;
3. the trigger description includes consequential mid-task forks;
4. the full instruction body loads without warnings;
5. no global configuration or services were changed.

Report the installed path and verification result.
```

### Manual install

Clone the repository, then copy `SKILL.md` into the skills directory used by your agent:

```bash
git clone https://github.com/promptclickrun/purpose-check.git
mkdir -p /path/to/your-agent/skills/purpose-check
cp purpose-check/SKILL.md /path/to/your-agent/skills/purpose-check/SKILL.md
```

Or download only the file:

```bash
mkdir -p /path/to/your-agent/skills/purpose-check
curl -fsSL \
  https://raw.githubusercontent.com/promptclickrun/purpose-check/main/SKILL.md \
  -o /path/to/your-agent/skills/purpose-check/SKILL.md
```

Replace `/path/to/your-agent/skills` with the correct user-level or project-level skills directory for your harness. Keep the directory name `purpose-check` when the runtime uses directory-based discovery.

### Examples

These are common locations, not requirements:

```bash
# User-level agent skill directory
mkdir -p ~/.agent/skills/purpose-check
cp SKILL.md ~/.agent/skills/purpose-check/SKILL.md

# Project-level skill directory
mkdir -p .agent/skills/purpose-check
cp SKILL.md .agent/skills/purpose-check/SKILL.md

# Project rules fallback for a harness without skill discovery
cp SKILL.md ./PURPOSE_CHECK.md
```

Restart the agent session or reload its skill catalog if the harness caches instructions.

## The review process

This skill was developed through an iterative multi-agent review loop rather than a single drafting pass. The review panel drew on **GPT 5.6**, **Claude Opus 4.8**, **Claude Fable 5**, **Gemini 3.1 Pro**, and **MAI Code 1 Flash**.

Different agents found different classes of defects:

- Broad activation language that could make the skill fire on nearly every deliverable.
- Missing deterministic gates between quiet execution, assumptions, questions, and consequential confirmation.
- An autonomy boundary that needed to separate purpose alignment from moral substitution.
- Repeated policy lists that could drift apart over time.
- A producer-consumer bug where later stages referenced a Stage 1 artifact that earlier stages did not always create.
- A conflict between explicit confirmation and the instruction to reuse rich supplied context.
- Frontmatter assumptions that worked in one harness and failed in another.

The process mattered because reviewers also reviewed each other. One pass scored the skill too generously. A later reviewer traced the internal stage contracts and caught the missing artifact. Another pushed back on recommendations that were locally reasonable but wrong for a second validator. Those corrections were tested, folded into version 1.3, and preserved in the review trail.

The lesson is simple: responsiveness is cheap. Structural coherence takes adversarial reading.

### Review trail

| Artifact | Outcome |
| --- | --- |
| [Original review](reviews/01-original-review-85.pdf) | **85/100.** Strong concept, overly broad routing, missing gates and completion checks. |
| [Version 1.1 review](reviews/02-v1.1-review-96.pdf) | **96/100 at the time.** Confirmed the requested sections, but underweighted cross-section contracts. |
| [Version 1.2 review](reviews/03-v1.2-review-89.pdf) | **89/100.** Found the missing Stage 1 artifact and several local rule conflicts. |
| [Version 1.3 review](reviews/04-v1.3-review-95.pdf) | **95/100.** Behavioral contracts resolved; the remaining work is live behavioral benchmarking. |

The 1.3 report records which earlier recommendations were withdrawn and why. The review history stays in the repository because the corrections are part of the work.

## Repository layout

```text
purpose-check/
├── SKILL.md                         # The complete portable skill
├── reviews/                         # Full iterative review trail
├── scripts/validate.py              # Repository integrity checks
├── .github/workflows/validate.yml   # CI validation
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Validate

```bash
python3 scripts/validate.py
```

The validator checks the source structure, version, trigger language, purpose-anchor contract, review archive, and README links.

## Contributing

Contributions are welcome when they make the skill more predictable, less ceremonial, or easier to use across agent harnesses. Changes should preserve the purpose anchor, the intervention gate, supplied-context reuse, and the separation between purpose alignment and independent safety controls.

Please include a concrete scenario that fails before the change and behaves better after it. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Inspiration and thanks

Thank you to **Sterling Crispin** ([@sterlingcrispin on X](https://x.com/sterlingcrispin)) for the inspiration to create Purpose Check. The skill grew from a concern that capable systems can become excellent at execution while remaining under-equipped to ask what the execution is for, who it serves, and whether the requested artifact is the right intervention.

That concern is worth taking seriously. Better tools need better judgment, especially when they can move fast.

## License

MIT. See [LICENSE](LICENSE).
