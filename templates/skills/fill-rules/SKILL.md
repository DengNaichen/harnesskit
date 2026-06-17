---
name: fill-rules
description: Fill or refresh short RULES.md entries and .harnesskit/rules/RULE-*.md details from .harnesskit/facts.md and verified repository evidence. Use after scan-facts when updating executable rules, rule details, validation context, and runner bindings.
---

# Fill Rules

Use this skill to update [RULES.md](../../../RULES.md) as the short constraint index and [.harnesskit/rules/](../../../.harnesskit/rules/) `RULE-*.md` files as the details layer.

## Workflow

1. Read [.harnesskit/facts.md](../../../.harnesskit/facts.md), current [RULES.md](../../../RULES.md), [.harnesskit/rules/](../../../.harnesskit/rules/), validation scripts, manifests, hook/CI config, and agent guidance.
2. Only promote an item into a Rule when it is repository-local or explicitly adopted, stable across tasks, has a clear violation shape, and is supported by evidence.
3. Before writing [RULES.md](../../../RULES.md) or [.harnesskit/rules/](../../../.harnesskit/rules/) `RULE-*.md` files, present candidate rule changes to the user as a single-choice MCQ. If the current Codex surface supports a native single-choice UI, use it; otherwise, render the choices as text and wait for the user's letter or correction.
   - A. Confirm all candidate rule changes and write them.
   - B. Correct one or more candidate rules before writing.
   - C. Skip writing rule changes for now.
   - D. Write only high-confidence repository rules and keep the rest as `[NEEDS CLARIFICATION: ...]`.
   If the user corrects a rule, category, validation binding, or runner status, treat the correction as user-confirmed evidence and record it as such.
4. Keep category headings as organization only; never treat a category such as general engineering, AI coding, stack, architecture, or domain as proof that a rule should be enabled.
5. Keep each [RULES.md](../../../RULES.md) rule as one short constraint sentence with a link to its details file.
6. Store rationale, evidence, validation context, runner bindings, caveats, and examples inside the `## Details` section of the matching details file in [.harnesskit/rules/](../../../.harnesskit/rules/); do not require a separate `## Validation` heading.
7. Mark unsupported or unverified rules as `[NEEDS CLARIFICATION: ...]`, `N/A`, `未配置`, or `不适用` instead of enabling them from examples.
8. Distinguish the rule, the validation/check, and the runner in details files; do not claim a check blocks changes without runner evidence.
9. Preserve existing customer-authored rules and structure unless the user explicitly asks for a migration.

## User Confirmation Protocol

Use a concise MCQ confirmation prompt like:

```text
I found these candidate Rule changes. Please confirm before I write `RULES.md` and `.harnesskit/rules/RULE-*.md`.

1. Add / update rule: RULE-...
   Constraint: ...
   Category: ...
   Evidence: ...
   Validation: ...
   Runner / binding: ...

2. Keep unresolved: ...
   Reason: ...

Choose one:
A. Confirm all candidate rule changes and write them.
B. Correct one or more candidate rules before writing.
C. Skip writing rule changes for now.
D. Write only high-confidence repository rules and keep the rest as `[NEEDS CLARIFICATION: ...]`.
```

If a native single-choice UI is available in the current Codex surface, present the four choices with that UI. If not, use the textual MCQ above. Then pause for the user's response. Do not silently promote facts, generic engineering advice, template examples, or inferred commands into durable Rules without user confirmation.

## Output

Update [RULES.md](../../../RULES.md) and [.harnesskit/rules/](../../../.harnesskit/rules/) `RULE-*.md` files only. If [AGENTS.md](../../../AGENTS.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md), or skills need matching changes, invoke the corresponding fill skill.

## Boundaries

- Do not invent commands, CI, branch protection, coverage thresholds, typecheck, docs build, or PR requirements.
- Do not turn generic engineering advice, task steps, tool tutorials, temporary plans, or unverified guesses into Rules.
- Put workflows in skills or [AGENTS.md](../../../AGENTS.md); put directory maps in [ARCHITECTURE.md](../../../ARCHITECTURE.md); put product background in README or docs.
- Do not mark partial review judgments as deterministic validation coverage.
- Do not treat [.harnesskit/facts.md](../../../.harnesskit/facts.md) as a replacement for checking the actual runner config.
- Do not restructure an existing non-template [RULES.md](../../../RULES.md) unless the user explicitly asks for a migration.
