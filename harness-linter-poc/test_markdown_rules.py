from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import assert_issue, make_project


def test_local_markdown_link_must_exist(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text("[missing](docs/missing.md)\n", encoding="utf-8")

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.link.missing")


def test_todo_checklist_markers_must_be_paired(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text(
        "<!-- harnesskit:todo-checklist:start -->\nopen checklist\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.todo_checklist.unpaired")
