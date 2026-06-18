from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import harnesskit.init as init_module  # noqa: E402
from harnesskit.init import InitError, init_project, install_integration  # noqa: E402


SHARED_SKILLS = (
    ".agents/skills/code-change-verification/SKILL.md",
    ".agents/skills/code-change-verification/agents/openai.yaml",
    ".agents/skills/code-change-verification/scripts/run_validation.py",
    ".agents/skills/fill-agents/SKILL.md",
    ".agents/skills/fill-agents/agents/openai.yaml",
    ".agents/skills/fill-architecture/SKILL.md",
    ".agents/skills/fill-architecture/agents/openai.yaml",
    ".agents/skills/fill-practices/SKILL.md",
    ".agents/skills/fill-practices/agents/openai.yaml",
    ".agents/skills/fill-rules/SKILL.md",
    ".agents/skills/fill-rules/agents/openai.yaml",
    ".agents/skills/fill-skills/SKILL.md",
    ".agents/skills/fill-skills/agents/openai.yaml",
    ".agents/skills/harness-init/SKILL.md",
    ".agents/skills/harness-init/agents/openai.yaml",
    ".agents/skills/implementation-strategy/SKILL.md",
    ".agents/skills/implementation-strategy/agents/openai.yaml",
    ".agents/skills/pr-draft-summary/SKILL.md",
    ".agents/skills/pr-draft-summary/agents/openai.yaml",
    ".agents/skills/scan-facts/SKILL.md",
    ".agents/skills/scan-facts/agents/openai.yaml",
)

PRACTICE_DOCS = (
    "docs/practices/CODING.md",
    "docs/practices/PRODUCT_SENSE.md",
    "docs/practices/RELIABILITY.md",
    "docs/practices/SECURITY.md",
)


def test_init_with_codex_outputs_context_harness_assets(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project), integration="codex")

    assert (project / "AGENTS.md").is_file()
    assert (project / "ARCHITECTURE.md").is_file()
    assert (project / "RULES.md").is_file()
    assert (project / "Makefile").is_file()
    assert (project / ".harnesskit/facts.md").is_file()
    for practice_doc in PRACTICE_DOCS:
        assert (project / practice_doc).is_file(), practice_doc
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


def test_init_with_claude_outputs_claude_companion_without_codex_assets(
    tmp_path: Path,
) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project), integration="claude")

    assert (project / "AGENTS.md").is_file()
    assert (project / "ARCHITECTURE.md").is_file()
    assert (project / "RULES.md").is_file()
    assert (project / ".harnesskit/facts.md").is_file()
    for practice_doc in PRACTICE_DOCS:
        assert (project / practice_doc).is_file(), practice_doc
    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")
    assert not (project / ".agents").exists()
    assert not (project / "Makefile").exists()

    config = read_config(project)
    assert config["schema_version"] == 1
    assert config["project_name"] == "demo"
    assert config["default_integration"] == "claude"
    assert config["installed_integrations"] == ["claude"]


def test_init_outputs_validation_runner_and_receipt_ignore(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project), integration="codex")

    makefile = (project / "Makefile").read_text(encoding="utf-8")
    assert "scripts/run_validation.py" in makefile

    runner = (
        project / ".agents/skills/code-change-verification/scripts/run_validation.py"
    ).read_text(encoding="utf-8")
    assert "CHECKS: tuple[Check, ...] = ()" in runner
    assert "not_configured" in runner
    assert ".harnesskit" in runner
    assert "receipts" in runner

    gitignore = (project / ".gitignore").read_text(encoding="utf-8")
    assert ".harnesskit/receipts/" in gitignore


def test_default_integration_is_codex(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    config = read_config(project)
    assert config["default_integration"] == "codex"
    assert (project / ".agents/skills/scan-facts/SKILL.md").is_file()
    assert (project / ".agents/skills/harness-init/SKILL.md").is_file()


def test_init_without_integration_outputs_core_context_harness_assets(
    tmp_path: Path,
) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project), integration=None)

    assert (project / "AGENTS.md").is_file()
    assert (project / "ARCHITECTURE.md").is_file()
    assert (project / "RULES.md").is_file()
    assert (project / ".harnesskit/facts.md").is_file()
    assert not (project / ".harnesskit/rules/RULE-ENG-001.md").exists()
    for practice_doc in PRACTICE_DOCS:
        assert (project / practice_doc).is_file(), practice_doc
    assert not (project / ".agents").exists()
    assert not (project / "CLAUDE.md").exists()
    assert not (project / "Makefile").exists()

    architecture = (project / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "{%" not in architecture
    assert "%}" not in architecture
    assert "CLAUDE.md" not in architecture
    assert "[`Makefile`](Makefile)" not in architecture
    assert "harnesskit integration install codex" in architecture

    config = read_config(project)
    assert config["default_integration"] is None
    assert config["installed_integrations"] == []


def test_agent_guidance_outputs_do_not_leak_template_placeholders(
    tmp_path: Path,
) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    agents = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert "{{" not in agents
    assert "}}" not in agents
    assert "{{#" not in agents
    assert ".agents/skills/" in agents
    assert "RULES.md" in agents
    assert "$harness-init" in agents
    assert "$scan-facts" in agents
    assert "docs/practices/" in agents
    assert "scan/fill 管道的中间产物" in agents
    assert "可作为扫描事实快照" not in agents
    assert "## 编码原则" in agents
    assert "## 1. 编码前先思考" in agents
    assert "## 2. 简单优先" in agents
    assert "## 3. 外科手术式改动" in agents
    assert "## 4. 核实优先" in agents
    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")

    facts = (project / ".harnesskit/facts.md").read_text(encoding="utf-8")
    assert "{{" not in facts
    assert "}}" not in facts
    assert "Harness Facts" in facts
    assert ".harnesskit/facts.md" in facts
    assert "[NEEDS CLARIFICATION:" in facts

    architecture = (project / "ARCHITECTURE.md").read_text(encoding="utf-8")
    assert "{{" not in architecture
    assert "}}" not in architecture
    assert "{%" not in architecture
    assert "%}" not in architecture
    assert "# [PROJECT_NAME] 架构地图" in architecture
    assert "AGENTS.md" in architecture
    assert "RULES.md" in architecture
    assert ".harnesskit/facts.md" in architecture
    assert "docs/practices/" in architecture
    assert "[NEEDS CLARIFICATION:" in architecture

    rules = (project / "RULES.md").read_text(encoding="utf-8")
    assert "{{" not in rules
    assert "}}" not in rules
    assert "Harness Rules" in rules
    assert "Rules 不要求一条规则对应一个 details 文件" in rules
    assert "技术栈与命名空间规则" in rules
    assert "架构与模块依赖规则" in rules
    assert "构建与运行脚本规则" in rules
    assert "安全规则" in rules
    assert "RULE-SEC-001" not in rules
    assert "RULE-ENG-001" not in rules
    assert ".harnesskit/rules/RULE-ENG-001.md" not in rules
    assert "[NEEDS CLARIFICATION:" in rules
    assert ".harnesskit/facts.md" not in rules

    for practice_doc in PRACTICE_DOCS:
        text = (project / practice_doc).read_text(encoding="utf-8")
        assert "{{" not in text, practice_doc
        assert "}}" not in text, practice_doc
        assert "{%" not in text, practice_doc
        assert "%}" not in text, practice_doc
        assert "[NEEDS CLARIFICATION:" in text, practice_doc


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

    scan_facts = (project / ".agents/skills/scan-facts/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "candidate facts" in scan_facts
    assert "用户确认协议" in scan_facts
    assert "暂停等待用户回复" in scan_facts
    assert "single-choice MCQ" in scan_facts
    assert "确认所有 candidate facts 并写入" in scan_facts
    assert "写入前先修正一个或多个 facts" in scan_facts

    harness_init = (project / ".agents/skills/harness-init/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "请用户确认候选 project identity" in harness_init
    assert "展示 candidate rule changes 并请求用户确认" in harness_init

    fill_rules = (project / ".agents/skills/fill-rules/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "candidate rule changes" in fill_rules
    assert "用户确认协议" in fill_rules
    assert "确认所有 candidate rule changes 并写入" in fill_rules
    assert "写入前先修正一个或多个 candidate rules" in fill_rules

    fill_practices = (project / ".agents/skills/fill-practices/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "docs/practices/" in fill_practices
    assert "判断指导" in fill_practices
    assert "硬约束不要放进 practices" in fill_practices

    fill_agents = (project / ".agents/skills/fill-agents/SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "scan/fill 管道输入" in fill_agents
    assert "临时 checklist" in fill_agents


def test_generated_placeholder_sections_include_checklists(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    init_project(str(project))

    checklist_files = [
        ".harnesskit/facts.md",
        "AGENTS.md",
        "ARCHITECTURE.md",
        "RULES.md",
        ".agents/skills/code-change-verification/SKILL.md",
        ".agents/skills/implementation-strategy/SKILL.md",
        ".agents/skills/pr-draft-summary/SKILL.md",
        "docs/practices/CODING.md",
        "docs/practices/PRODUCT_SENSE.md",
        "docs/practices/RELIABILITY.md",
        "docs/practices/SECURITY.md",
    ]
    for relative_path in checklist_files:
        text = (project / relative_path).read_text(encoding="utf-8")
        start_count = text.count("<!-- harnesskit:todo-checklist:start -->")
        end_count = text.count("<!-- harnesskit:todo-checklist:end -->")
        assert start_count > 0, relative_path
        assert end_count == start_count, relative_path


def test_agent_guidance_outputs_claude_symlink_from_dereferenced_template(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    template_root = tmp_path / "templates"
    template_root.mkdir()
    (template_root / "AGENTS.md").write_text("# Guide\n", encoding="utf-8")
    (template_root / "CLAUDE.md").write_text("# Guide\n", encoding="utf-8")
    (template_root / "Makefile").write_text("verify:\n", encoding="utf-8")
    (template_root / "skills").mkdir()
    project = tmp_path / "demo"

    monkeypatch.setattr(init_module, "_locate_templates", lambda: template_root)
    init_project(str(project))

    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")


def test_unsupported_integration_raises(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()

    with pytest.raises(InitError, match="unsupported integration"):
        init_project(str(project), integration="cursor")


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
    skill = project / ".agents" / "skills" / "scan-facts" / "SKILL.md"
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
    skill = project / ".agents" / "skills" / "scan-facts" / "SKILL.md"
    skill.parent.mkdir(parents=True)
    skill.write_text("custom skill\n", encoding="utf-8")

    result = init_project(str(project), integration="codex", force=True)

    assert skill.read_text(encoding="utf-8") != "custom skill\n"
    assert skill in result.created


def test_install_integration_repairs_missing_codex_skills(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    init_project(str(project), integration="codex")
    shutil.rmtree(project / ".agents" / "skills" / "scan-facts")

    result = install_integration(project, "codex")

    assert (project / ".agents/skills/scan-facts/SKILL.md").is_file()
    assert project / ".agents/skills/scan-facts/SKILL.md" in result.created
    config = read_config(project)
    assert config["installed_integrations"] == ["codex"]


def test_install_integration_adds_claude_companion_after_core_init(
    tmp_path: Path,
) -> None:
    project = (tmp_path / "demo").resolve()
    init_project(str(project), integration=None)

    result = install_integration(project, "claude")

    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")
    assert project / "CLAUDE.md" in result.created
    assert not (project / ".agents").exists()
    assert not (project / "Makefile").exists()
    config = read_config(project)
    assert config["default_integration"] == "claude"
    assert config["installed_integrations"] == ["claude"]


def test_install_codex_after_core_init_adds_companion_and_validation_assets(
    tmp_path: Path,
) -> None:
    project = (tmp_path / "demo").resolve()
    init_project(str(project), integration=None)

    result = install_integration(project, "codex")

    assert (project / "CLAUDE.md").is_symlink()
    assert (project / "CLAUDE.md").readlink() == Path("AGENTS.md")
    assert (project / "Makefile").is_file()
    assert (project / ".agents/skills/scan-facts/SKILL.md").is_file()
    assert project / "CLAUDE.md" in result.created
    assert project / "Makefile" in result.created
    config = read_config(project)
    assert config["default_integration"] == "codex"
    assert config["installed_integrations"] == ["codex"]


def test_install_integration_requires_initialized_project(tmp_path: Path) -> None:
    project = (tmp_path / "demo").resolve()
    project.mkdir()

    with pytest.raises(InitError, match="harnesskit init --here"):
        install_integration(project, "codex")


def read_config(project: Path) -> dict[str, object]:
    return json.loads(
        (project / ".harnesskit" / "config.json").read_text(encoding="utf-8")
    )
