"""Repository fact detection and tech stack checks."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

from ..core.constants import TECH_STACK_END, TECH_STACK_ENTRY_PATTERN, TECH_STACK_START
from ..core.issues import issue
from ..core.markdown import extract_marked_blocks
from ..core.models import Issue


def check_tech_stack_blocks(
    project_path: Path, markdown_files: Iterable[Path], issues: list[Issue]
) -> None:
    facts = detect_tech_stack_facts(project_path)
    for markdown_file in markdown_files:
        text = markdown_file.read_text(encoding="utf-8")
        for block in extract_marked_blocks(
            project_path,
            markdown_file,
            text,
            TECH_STACK_START,
            TECH_STACK_END,
            "markdown.tech_stack.unpaired",
            issues,
        ):
            for key, declared_value in parse_tech_stack_entries(block).items():
                expected_value = facts.get(key)
                if expected_value is None:
                    continue
                if not tech_stack_value_matches(declared_value, expected_value):
                    issues.append(
                        issue(
                            "error",
                            "tech_stack.mismatch",
                            project_path,
                            f"{key!r} declares {declared_value!r}, but repository facts indicate {expected_value!r}",
                            markdown_file,
                        )
                    )


def detect_tech_stack_facts(project_path: Path) -> dict[str, str]:
    facts: dict[str, str] = {}
    pyproject_path = project_path / "pyproject.toml"
    if pyproject_path.is_file():
        text = pyproject_path.read_text(encoding="utf-8")
        project_section = toml_section(text, "project")
        build_section = toml_section(text, "build-system")
        dependencies = {
            dependency_name(item)
            for item in toml_array_strings(project_section, "dependencies")
        }

        if project_section:
            facts["language"] = "Python"
        if "typer" in dependencies:
            facts["cli"] = "Typer"
        if "rich" in dependencies:
            facts["terminal output"] = "Rich"
        if "jinja2" in dependencies:
            facts["templates"] = "Jinja2"
        if "hatchling" in {
            dependency_name(item)
            for item in toml_array_strings(build_section, "requires")
        }:
            facts["build backend"] = "Hatchling"
        elif "hatchling" in toml_string(build_section, "build-backend").lower():
            facts["build backend"] = "Hatchling"

    package_json_path = project_path / "package.json"
    if package_json_path.is_file():
        facts.setdefault("language", "JavaScript")
        if (project_path / "pnpm-lock.yaml").is_file():
            facts["package manager"] = "pnpm"
        elif (project_path / "yarn.lock").is_file():
            facts["package manager"] = "yarn"
        elif (project_path / "package-lock.json").is_file():
            facts["package manager"] = "npm"

    if (project_path / "uv.lock").is_file():
        facts["package manager"] = "uv"

    detected_tests = detect_python_test_framework(project_path)
    if detected_tests:
        facts["tests"] = detected_tests

    return facts


def declared_python_tools(project_path: Path) -> set[str]:
    pyproject_path = project_path / "pyproject.toml"
    if not pyproject_path.is_file():
        return set()

    text = pyproject_path.read_text(encoding="utf-8")
    return {dependency_name(item) for item in re.findall(r'"([^"]+)"', text)}


def detect_python_test_framework(project_path: Path) -> str | None:
    test_files = list((project_path / "tests").glob("**/*.py"))
    for test_file in test_files:
        text = test_file.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?m)^\s*(import unittest|from unittest\b)", text):
            return "unittest"

    if (project_path / "pytest.ini").is_file() or (
        project_path / "conftest.py"
    ).is_file():
        return "pytest"
    for test_file in test_files:
        text = test_file.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"(?m)^\s*(import pytest|from pytest\b)", text):
            return "pytest"
    return None


def parse_tech_stack_entries(block: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in block.splitlines():
        match = TECH_STACK_ENTRY_PATTERN.match(line)
        if not match:
            continue
        key = normalize_tech_stack_key(match.group(1))
        value = match.group(2).strip().strip("`")
        entries[key] = value
    return entries


def normalize_tech_stack_key(key: str) -> str:
    return re.sub(r"\s+", " ", key.strip().lower().replace("-", " "))


def tech_stack_value_matches(declared_value: str, expected_value: str) -> bool:
    declared = normalize_tech_stack_value(declared_value)
    expected = normalize_tech_stack_value(expected_value)
    return expected in declared or declared in expected


def normalize_tech_stack_value(value: str) -> str:
    return re.sub(r"[^a-z0-9+#.]+", " ", value.lower()).strip()


def toml_section(text: str, section_name: str) -> str:
    pattern = re.compile(rf"(?ms)^\[{re.escape(section_name)}\]\s*(.*?)(?=^\[|\Z)")
    match = pattern.search(text)
    return match.group(1) if match else ""


def toml_string(section_text: str, key: str) -> str:
    match = re.search(rf'(?m)^{re.escape(key)}\s*=\s*"([^"]*)"', section_text)
    return match.group(1) if match else ""


def toml_array_strings(section_text: str, key: str) -> list[str]:
    match = re.search(rf"(?ms)^{re.escape(key)}\s*=\s*\[(.*?)\]", section_text)
    if not match:
        return []
    return re.findall(r'"([^"]+)"', match.group(1))


def dependency_name(requirement: str) -> str:
    name = re.split(r"[\s<>=!~;\[]", requirement.strip(), maxsplit=1)[0]
    return name.lower().replace("_", "-")
