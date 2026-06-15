from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import assert_issue, make_project


def write_rules(project: Path, body: str) -> None:
    (project / "RULES.md").write_text(body, encoding="utf-8")


def write_detail(project: Path, rule_id: str, body: str | None = None) -> Path:
    rules_dir = project / ".harnesskit" / "rules"
    rules_dir.mkdir(parents=True, exist_ok=True)
    path = rules_dir / f"{rule_id}.md"
    path.write_text(
        body
        or f"""# {rule_id}

## Rule

Do the thing.

## Details

The reason.
""",
        encoding="utf-8",
    )
    return path


def test_rules_entries_require_matching_detail_file(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    write_rules(project, "- RULE-ENG-001: Do the thing.\n")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "rule.detail.missing")


def test_rule_detail_heading_must_match_rule_id(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    write_rules(project, "- RULE-ENG-001: Do the thing.\n")
    write_detail(
        project, "RULE-ENG-001", "# RULE-ENG-999\n\n## Rule\n\nA\n\n## Details\n\nB\n"
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "rule.detail.heading")


def test_rule_detail_required_sections(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    write_rules(project, "- RULE-ENG-001: Do the thing.\n")
    write_detail(project, "RULE-ENG-001", "# RULE-ENG-001\n\n## Rule\n\nA\n")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "rule.detail.section_missing")


def test_orphan_rule_detail_warns(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    write_rules(project, "- RULE-ENG-001: Do the thing.\n")
    write_detail(project, "RULE-ENG-001")
    write_detail(project, "RULE-ENG-999")

    report = lint_project(project)

    assert report.passed
    assert_issue(report, "rule.detail.orphan")


def test_long_rule_summary_warns(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    long_summary = "x" * 220
    write_rules(project, f"- RULE-ENG-001: {long_summary}\n")
    write_detail(project, "RULE-ENG-001")

    report = lint_project(project)

    assert report.passed
    assert_issue(report, "rule.summary.long")
