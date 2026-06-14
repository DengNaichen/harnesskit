from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mykit.init as init_module  # noqa: E402
from mykit.init import InitError, init_project, install_integration  # noqa: E402


SHARED_SKILLS = (
    ".agents/skills/code-change-verification/SKILL.md",
    ".agents/skills/implementation-strategy/SKILL.md",
    ".agents/skills/mykit-audit/SKILL.md",
    ".agents/skills/mykit-refresh/SKILL.md",
    ".agents/skills/mykit-explain/SKILL.md",
    ".agents/skills/pr-draft-summary/SKILL.md",
)


def test_init_with_codex_outputs_context_harness_assets(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project), integration="codex")

    assert (project / "AGENTS.md").is_file()
    assert (project / "candidate.md").is_file()
    assert (project / "CLAUDE.md").is_file()
    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")
    assert not (project / "skills").exists()
    for skill in SHARED_SKILLS:
        assert (project / skill).is_file(), skill

    config = read_config(project)
    assert config["schema_version"] == 1
    assert config["project_name"] == "demo"
    assert config["default_integration"] == "codex"
    assert config["installed_integrations"] == ["codex"]


def test_default_integration_is_codex(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    config = read_config(project)
    assert config["default_integration"] == "codex"
    assert (project / ".agents/skills/mykit-audit/SKILL.md").is_file()


def test_agent_guidance_outputs_do_not_leak_template_placeholders(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    agents = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert "{{" not in agents
    assert "}}" not in agents
    assert "{{#" not in agents
    assert ".agents/skills/" in agents
    assert "candidate.md" in agents
    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")

    candidate = (project / "candidate.md").read_text(encoding="utf-8")
    assert "{{" not in candidate
    assert "}}" not in candidate
    assert "待沉淀" in candidate


def test_shared_skill_outputs_do_not_leak_template_placeholders(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    for skill in SHARED_SKILLS:
        text = (project / skill).read_text(encoding="utf-8")
        assert "{{" not in text, skill
        assert "}}" not in text, skill
        assert "{%" not in text, skill
        assert "%}" not in text, skill
        assert "CATEGORY_SIGNALS" not in text, skill
        assert "GITHUB_REPO_URL" not in text, skill
        assert "PROJECT_SPECIFIC_COMPATIBILITY_RULES" not in text, skill


def test_generated_placeholder_sections_include_checklists(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    expected_checklist_counts = {
        "AGENTS.md": 9,
        "candidate.md": 1,
        ".agents/skills/code-change-verification/SKILL.md": 1,
        ".agents/skills/implementation-strategy/SKILL.md": 1,
        ".agents/skills/mykit-audit/SKILL.md": 1,
        ".agents/skills/mykit-explain/SKILL.md": 1,
        ".agents/skills/mykit-refresh/SKILL.md": 1,
        ".agents/skills/pr-draft-summary/SKILL.md": 2,
    }
    for relative_path, expected_count in expected_checklist_counts.items():
        text = (project / relative_path).read_text(encoding="utf-8")
        assert text.count("<!-- mykit:todo-checklist:start -->") == expected_count, relative_path
        assert text.count("<!-- mykit:todo-checklist:end -->") == expected_count, relative_path


def test_agent_guidance_outputs_claude_symlink_from_dereferenced_template(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    template_root = tmp_path / "templates"
    template_root.mkdir()
    (template_root / "AGENTS.md").write_text("# Guide\n", encoding="utf-8")
    (template_root / "CLAUDE.md").write_text("# Guide\n", encoding="utf-8")
    (template_root / "skills").mkdir()
    project = tmp_path / "demo"

    monkeypatch.setattr(init_module, "_locate_templates", lambda: template_root)
    init_project(str(project))

    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")


def test_unsupported_integration_raises(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    with pytest.raises(InitError, match="unsupported integration"):
        init_project(str(project), integration="claude")


def test_existing_files_are_skipped_without_force(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    project.mkdir()
    agents = project / "AGENTS.md"
    agents.write_text("custom agents\n", encoding="utf-8")

    result = init_project(str(project), integration="codex")

    assert agents.read_text(encoding="utf-8") == "custom agents\n"
    assert agents in result.skipped


def test_existing_shared_skills_are_skipped_without_force(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    skill = project / ".agents" / "skills" / "mykit-audit" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("custom skill\n", encoding="utf-8")

    result = init_project(str(project), integration="codex")

    assert skill.read_text(encoding="utf-8") == "custom skill\n"
    assert skill in result.skipped


def test_force_overwrites_existing_template_files(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    project.mkdir()
    agents = project / "AGENTS.md"
    agents.write_text("custom agents\n", encoding="utf-8")

    result = init_project(str(project), integration="codex", force=True)

    assert agents.read_text(encoding="utf-8") != "custom agents\n"
    assert agents in result.created


def test_force_overwrites_existing_shared_skills(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    skill = project / ".agents" / "skills" / "mykit-audit" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("custom skill\n", encoding="utf-8")

    result = init_project(str(project), integration="codex", force=True)

    assert skill.read_text(encoding="utf-8") != "custom skill\n"
    assert skill in result.created


def test_install_integration_repairs_missing_codex_skills(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    init_project(str(project), integration="codex")
    shutil.rmtree(project / ".agents" / "skills" / "mykit-audit")

    result = install_integration(project, "codex")

    assert (project / ".agents/skills/mykit-audit/SKILL.md").is_file()
    assert project / ".agents/skills/mykit-audit/SKILL.md" in result.created
    config = read_config(project)
    assert config["installed_integrations"] == ["codex"]


def test_install_integration_requires_initialized_project(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    project.mkdir()

    with pytest.raises(InitError, match="mykit init --here"):
        install_integration(project, "codex")


def read_config(project: Path) -> dict[str, object]:
    return json.loads((project / ".mykit" / "config.json").read_text(encoding="utf-8"))
