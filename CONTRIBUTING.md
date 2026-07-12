# Contributing

Purpose Check is small on purpose. Contributions should sharpen behavior, close a demonstrated gap, or improve portability without turning the skill into a ritual.

## Before proposing a change

Open an issue or include this information in the pull request:

1. The scenario that currently behaves badly.
2. The exact instruction or structural conflict causing it.
3. The proposed rule change.
4. The expected behavior after the change.
5. Which packaging targets you validated.

## Design rules

- Keep one canonical statement for each governing rule.
- Reuse supplied context before asking a question.
- Preserve quiet execution for clear, reversible work.
- Keep the purpose anchor stable across Stages 2 through 4.
- Treat permission, consent, legal constraints, privacy, and safety as independent controls.
- Avoid capabilities a Markdown skill cannot enforce, such as authenticating the speaker.
- Prefer observable behavior and completion criteria over advisory prose.
- Do not add philosophy terminology unless it changes agent behavior.

## Development

```bash
python3 scripts/validate.py
```

The repository ships one canonical `SKILL.md`. Keep it portable. Harness-specific installation guidance belongs in documentation, while the behavioral source remains unchanged.

## Pull requests

Keep pull requests focused. Include a short test matrix covering:

- clear reversible work
- minor ambiguity with a safe default
- deliverable-changing ambiguity
- a likely request-to-goal mismatch
- consequential work with complete context
- consequential work with missing or stale context
- a material mid-task fork

If the change affects triggering or conversation behavior, include before-and-after transcripts or benchmark results.

## Review standard

A change is ready when:

- every later-stage term has a clear producer;
- no local instruction contradicts a canonical rule;
- routine tasks remain quiet;
- all target packages validate;
- generated artifacts match the committed source;
- documentation links resolve.
