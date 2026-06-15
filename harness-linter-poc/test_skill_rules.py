from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import assert_issue, make_project


def test_missing_codex_skill_fails(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".agents/skills/scan-stack/SKILL.md").unlink()

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "codex.skill.missing")


def test_skill_frontmatter_is_required(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / ".agents/skills/scan-stack/SKILL.md").write_text(
        "# no frontmatter\n", encoding="utf-8"
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "skill.frontmatter.missing")


def test_skill_references_must_exist(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text(
        "Use $missing-skill before changes.\n", encoding="utf-8"
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "skill.reference.missing")
