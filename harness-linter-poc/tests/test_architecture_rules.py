from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import assert_issue, make_project, write_architecture_doc


def test_architecture_map_direct_children_must_be_declared(
    tmp_path: Path,
) -> None:
    project = make_project(tmp_path)
    source_dir = project / "src/demo"
    source_dir.mkdir(parents=True)
    (source_dir / "__init__.py").write_text("", encoding="utf-8")
    (source_dir / "core.py").write_text("VALUE = 1\n", encoding="utf-8")
    write_architecture_doc(
        project,
        """
        - [`src/demo/`](src/demo/) <!-- harnesskit:coverage=direct-children -->
        - [`src/demo/__init__.py`](src/demo/__init__.py)
        """,
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "architecture.coverage_missing")
    issue = next(
        item for item in report.issues if item.code == "architecture.coverage_missing"
    )
    assert issue.path == "ARCHITECTURE.md"
    assert issue.found == "src/demo/core.py"
    assert (
        issue.expected
        == "add a Markdown link to `src/demo/core.py` in ARCHITECTURE.md or list it in the coverage hint ignore attribute"
    )


def test_architecture_map_direct_children_can_be_ignored(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    source_dir = project / "src/demo"
    source_dir.mkdir(parents=True)
    (source_dir / "__init__.py").write_text("", encoding="utf-8")
    (source_dir / "generated.py").write_text("VALUE = 1\n", encoding="utf-8")
    write_architecture_doc(
        project,
        """
        - [`src/demo/`](src/demo/) <!-- harnesskit:coverage=direct-children ignore=src/demo/generated.py -->
        - [`src/demo/__init__.py`](src/demo/__init__.py)
        """,
    )

    report = lint_project(project)

    assert not any(
        item.code == "architecture.coverage_missing" for item in report.issues
    ), report.issues


def test_architecture_map_paths_must_exist(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    write_architecture_doc(
        project,
        """
        - [`src/missing/`](src/missing/) <!-- harnesskit:coverage=direct-children -->
        """,
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "architecture.path_missing")


def test_architecture_coverage_hint_must_be_well_formed(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    source_dir = project / "src/demo"
    source_dir.mkdir(parents=True)
    write_architecture_doc(
        project,
        """
        - [`src/demo/`](src/demo/) !-- harnesskit:coverage=direct-children -->
        """,
    )

    report = lint_project(project)

    assert not report.passed
    assert_issue(report, "architecture.coverage_hint_invalid")
    issue = next(
        item
        for item in report.issues
        if item.code == "architecture.coverage_hint_invalid"
    )
    assert issue.path == "ARCHITECTURE.md"
    assert issue.found == (
        "- [`src/demo/`](src/demo/) !-- harnesskit:coverage=direct-children -->"
    )
    assert issue.expected


def test_architecture_placeholder_descriptions_warn(tmp_path: Path) -> None:
    project = make_project(tmp_path)
    write_architecture_doc(
        project,
        """
        - [`AGENTS.md`](AGENTS.md): TODO: placeholder responsibility.
        """,
    )

    report = lint_project(project)

    assert report.passed, report.issues
    assert_issue(report, "architecture.placeholder_description")
    issue = next(
        item
        for item in report.issues
        if item.code == "architecture.placeholder_description"
    )
    assert issue.severity == "warning"
    assert issue.path == "ARCHITECTURE.md"
    assert (
        issue.found == "- [`AGENTS.md`](AGENTS.md): TODO: placeholder responsibility."
    )
