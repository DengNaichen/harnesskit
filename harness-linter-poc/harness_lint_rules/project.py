"""Project-level checks."""

from __future__ import annotations

from pathlib import Path

from .issues import issue
from .models import Issue


def check_project_path(project_path: Path) -> Issue | None:
    if project_path.is_dir():
        return None

    return issue(
        "error",
        "project.not_directory",
        project_path,
        "project path is not a directory",
        project_path,
    )
