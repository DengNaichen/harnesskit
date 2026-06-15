from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import (
    add_python_stack,
    append_tech_stack_block,
    append_verification_block,
    assert_issue,
    make_project,
)


def test_tech_stack_block_matches_repo_facts(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    append_verification_block(
        project / "AGENTS.md",
        {"Package build": "uv build"},
    )
    append_tech_stack_block(
        project / "AGENTS.md",
        {
            "Language": "Python 3.11+",
            "Package manager": "uv",
            "CLI": "Typer",
            "Terminal output": "Rich",
            "Templates": "Jinja2",
            "Build backend": "Hatchling",
            "Tests": "pytest",
        },
    )

    report = lint_project(project)

    assert report.passed, report.issues


def test_tech_stack_block_must_match_repo_facts(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    add_python_stack(project)
    append_tech_stack_block(
        project / "AGENTS.md",
        {
            "Package manager": "npm",
            "Tests": "unittest",
        },
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "tech_stack.mismatch")


def test_tech_stack_markers_must_be_paired(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    (project / "AGENTS.md").write_text(
        "<!-- harnesskit:tech-stack:start -->\n- Package manager: uv\n",
        encoding="utf-8",
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "markdown.tech_stack.unpaired")
