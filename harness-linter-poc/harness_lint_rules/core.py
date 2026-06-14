"""Core harness file and integration checks."""

from __future__ import annotations

from pathlib import Path

from .constants import CODEX_SKILLS
from .issues import issue
from .models import Issue


def check_core_files(project_path: Path, issues: list[Issue]) -> None:
    for required_path in ("AGENTS.md", "CLAUDE.md"):
        path = project_path / required_path
        if not path.exists():
            issues.append(
                issue(
                    "error",
                    "core.missing",
                    project_path,
                    "required harness file is missing",
                    path,
                )
            )
        elif path.is_file() and path.stat().st_size == 0:
            issues.append(
                issue(
                    "error",
                    "core.empty",
                    project_path,
                    "required harness file is empty",
                    path,
                )
            )


def check_claude_pointer(project_path: Path, issues: list[Issue]) -> None:
    claude_path = project_path / "CLAUDE.md"
    agents_path = project_path / "AGENTS.md"
    if not claude_path.exists() or not agents_path.exists():
        return

    if claude_path.is_symlink():
        try:
            if claude_path.resolve(strict=True) != agents_path.resolve(strict=True):
                issues.append(
                    issue(
                        "warning",
                        "claude.pointer",
                        project_path,
                        "CLAUDE.md symlink should point to AGENTS.md",
                        claude_path,
                    )
                )
        except FileNotFoundError:
            issues.append(
                issue(
                    "error",
                    "claude.broken_symlink",
                    project_path,
                    "CLAUDE.md symlink target is missing",
                    claude_path,
                )
            )
        return

    if claude_path.is_file() and "AGENTS.md" not in claude_path.read_text(
        encoding="utf-8"
    ):
        issues.append(
            issue(
                "warning",
                "claude.pointer",
                project_path,
                "CLAUDE.md should point readers to AGENTS.md",
                claude_path,
            )
        )


def check_installed_integrations(
    project_path: Path, config: dict[str, object] | None, issues: list[Issue]
) -> None:
    installed = config.get("installed_integrations", []) if config else []
    if not isinstance(installed, list):
        return

    if "codex" in installed:
        for relative_path in CODEX_SKILLS:
            path = project_path / relative_path
            if not path.is_file():
                issues.append(
                    issue(
                        "error",
                        "codex.skill.missing",
                        project_path,
                        "required Codex skill is missing",
                        path,
                    )
                )
            elif path.stat().st_size == 0:
                issues.append(
                    issue(
                        "error",
                        "codex.skill.empty",
                        project_path,
                        "required Codex skill is empty",
                        path,
                    )
                )
