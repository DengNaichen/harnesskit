from __future__ import annotations

from pathlib import Path

from harness_lint import lint_project
from testing_helpers import make_project


def test_valid_harness_passes(tmp_path: Path) -> None:
    project = make_project(tmp_path)

    report = lint_project(project)

    assert report.passed, report.issues
    assert report.issues == []
