---
name: fill-rules
description: Fill or refresh short RULES.md entries and .harnesskit/rules/RULE-*.md details from .harnesskit/facts.md and verified repository evidence. Use after scan-facts when updating executable rules, rule details, validation context, and runner bindings.
---

# Fill Rules

Use this skill to update [RULES.md](../../../RULES.md) as the short constraint index and [.harnesskit/rules/](../../../.harnesskit/rules/) `RULE-*.md` files as the details layer.

## Workflow

1. Read [.harnesskit/facts.md](../../../.harnesskit/facts.md), current [RULES.md](../../../RULES.md), [.harnesskit/rules/](../../../.harnesskit/rules/), validation scripts, manifests, hook/CI config, and agent guidance.
2. Only promote an item into a Rule when it is repository-local or explicitly adopted, stable across tasks, has a clear violation shape, and is supported by evidence.
3. Keep category headings as organization only; never treat a category such as general engineering, AI coding, stack, architecture, or domain as proof that a rule should be enabled.
4. Keep each [RULES.md](../../../RULES.md) rule as one short constraint sentence with a link to its details file.
5. Store rationale, evidence, validation context, runner bindings, caveats, and examples inside the `## Details` section of the matching details file in [.harnesskit/rules/](../../../.harnesskit/rules/); do not require a separate `## Validation` heading.
6. Mark unsupported or unverified rules as `[NEEDS CLARIFICATION: ...]`, `N/A`, `未配置`, or `不适用` instead of enabling them from examples.
7. Distinguish the rule, the validation/check, and the runner in details files; do not claim a check blocks changes without runner evidence.
8. Preserve existing customer-authored rules and structure unless the user explicitly asks for a migration.

## Output

Update [RULES.md](../../../RULES.md) and [.harnesskit/rules/](../../../.harnesskit/rules/) `RULE-*.md` files only. If [AGENTS.md](../../../AGENTS.md), [ARCHITECTURE.md](../../../ARCHITECTURE.md), or skills need matching changes, invoke the corresponding fill skill.

## Boundaries

- Do not invent commands, CI, branch protection, coverage thresholds, typecheck, docs build, or PR requirements.
- Do not turn generic engineering advice, task steps, tool tutorials, temporary plans, or unverified guesses into Rules.
- Put workflows in skills or [AGENTS.md](../../../AGENTS.md); put directory maps in [ARCHITECTURE.md](../../../ARCHITECTURE.md); put product background in README or docs.
- Do not mark partial review judgments as deterministic validation coverage.
- Do not treat [.harnesskit/facts.md](../../../.harnesskit/facts.md) as a replacement for checking the actual runner config.
- Do not restructure an existing non-template [RULES.md](../../../RULES.md) unless the user explicitly asks for a migration.
