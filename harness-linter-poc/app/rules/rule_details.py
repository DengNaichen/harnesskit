"""RULES.md and rule details linkage checks."""

from __future__ import annotations

from pathlib import Path

from core.constants import RULE_DETAIL_GLOB, RULE_ID_PATTERN, RULE_SUMMARY_MAX_LENGTH
from core.issues import issue
from core.models import Issue


REQUIRED_DETAIL_SECTIONS = ("## Rule", "## Details")


def check_rule_details(project_path: Path, issues: list[Issue]) -> None:
    rules_path = project_path / "RULES.md"
    if not rules_path.is_file():
        return

    rules_text = rules_path.read_text(encoding="utf-8")
    rule_ids = set(RULE_ID_PATTERN.findall(rules_text))
    if not rule_ids:
        return

    for rule_id in sorted(rule_ids):
        detail_path = project_path / ".harnesskit" / "rules" / f"{rule_id}.md"
        if not detail_path.is_file():
            issues.append(
                issue(
                    "error",
                    "rule.detail.missing",
                    project_path,
                    "RULES.md rule is missing a matching detail file",
                    rules_path,
                    found=rule_id,
                    expected=f".harnesskit/rules/{rule_id}.md",
                )
            )
            continue

        detail_text = detail_path.read_text(encoding="utf-8")
        first_line = detail_text.splitlines()[0].strip() if detail_text else ""
        if first_line != f"# {rule_id}":
            issues.append(
                issue(
                    "error",
                    "rule.detail.heading",
                    project_path,
                    "rule detail heading must match its RULE id",
                    detail_path,
                    found=first_line or "(empty file)",
                    expected=f"# {rule_id}",
                )
            )
        for required_section in REQUIRED_DETAIL_SECTIONS:
            if required_section not in detail_text:
                issues.append(
                    issue(
                        "error",
                        "rule.detail.section_missing",
                        project_path,
                        "rule detail file is missing a required section",
                        detail_path,
                        found=rule_id,
                        expected=required_section,
                    )
                )

    for detail_path in sorted(project_path.glob(RULE_DETAIL_GLOB)):
        detail_id = detail_path.stem
        if detail_id not in rule_ids:
            issues.append(
                issue(
                    "warning",
                    "rule.detail.orphan",
                    project_path,
                    "rule detail file has no matching RULES.md entry",
                    detail_path,
                    found=detail_id,
                    expected="every .harnesskit/rules/RULE-*.md file should be referenced from RULES.md",
                )
            )

    check_rule_summary_length(project_path, rules_path, rules_text, issues)


def check_rule_summary_length(
    project_path: Path, rules_path: Path, rules_text: str, issues: list[Issue]
) -> None:
    for line_number, line in enumerate(rules_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped.startswith("- RULE-"):
            continue
        if len(stripped) <= RULE_SUMMARY_MAX_LENGTH:
            continue
        issues.append(
            issue(
                "warning",
                "rule.summary.long",
                project_path,
                "RULES.md rule summary should stay short and executable",
                rules_path,
                line=line_number,
                found=stripped,
                expected=f"one-line rule summary no longer than {RULE_SUMMARY_MAX_LENGTH} characters",
            )
        )
