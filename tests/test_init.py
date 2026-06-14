from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


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


class InitProjectTests(unittest.TestCase):
    def test_init_with_codex_outputs_context_harness_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()

            init_project(str(project), integration="codex")

            self.assertTrue((project / "AGENTS.md").is_file())
            self.assertTrue((project / "candidate.md").is_file())
            self.assertTrue((project / "CLAUDE.md").is_file())
            self.assertTrue((project / "CLAUDE.md").is_symlink())
            self.assertEqual((project / "CLAUDE.md").readlink(), Path("AGENTS.md"))
            self.assertFalse((project / "skills").exists())
            for skill in SHARED_SKILLS:
                self.assertTrue((project / skill).is_file(), skill)

            config = self._read_config(project)
            self.assertEqual(config["schema_version"], 1)
            self.assertEqual(config["project_name"], "demo")
            self.assertEqual(config["default_integration"], "codex")
            self.assertEqual(config["installed_integrations"], ["codex"])

    def test_default_integration_is_codex(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()

            init_project(str(project))

            config = self._read_config(project)
            self.assertEqual(config["default_integration"], "codex")
            self.assertTrue((project / ".agents/skills/mykit-audit/SKILL.md").is_file())

    def test_agent_guidance_outputs_do_not_leak_template_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()

            init_project(str(project))

            agents = (project / "AGENTS.md").read_text(encoding="utf-8")
            self.assertNotIn("{{", agents)
            self.assertNotIn("}}", agents)
            self.assertNotIn("{{#", agents)
            self.assertIn(".agents/skills/", agents)
            self.assertIn("candidate.md", agents)
            self.assertTrue((project / "CLAUDE.md").is_symlink())
            self.assertEqual((project / "CLAUDE.md").readlink(), Path("AGENTS.md"))

            candidate = (project / "candidate.md").read_text(encoding="utf-8")
            self.assertNotIn("{{", candidate)
            self.assertNotIn("}}", candidate)
            self.assertIn("待沉淀", candidate)

    def test_shared_skill_outputs_do_not_leak_template_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()

            init_project(str(project))

            for skill in SHARED_SKILLS:
                text = (project / skill).read_text(encoding="utf-8")
                self.assertNotIn("{{", text, skill)
                self.assertNotIn("}}", text, skill)
                self.assertNotIn("{%", text, skill)
                self.assertNotIn("%}", text, skill)
                self.assertNotIn("CATEGORY_SIGNALS", text, skill)
                self.assertNotIn("GITHUB_REPO_URL", text, skill)
                self.assertNotIn("PROJECT_SPECIFIC_COMPATIBILITY_RULES", text, skill)

    def test_generated_placeholder_sections_include_checklists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()

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
                self.assertEqual(
                    text.count("<!-- mykit:todo-checklist:start -->"),
                    expected_count,
                    relative_path,
                )
                self.assertEqual(
                    text.count("<!-- mykit:todo-checklist:end -->"),
                    expected_count,
                    relative_path,
                )

    def test_agent_guidance_outputs_claude_symlink_from_dereferenced_template(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template_root = root / "templates"
            template_root.mkdir()
            (template_root / "AGENTS.md").write_text("# Guide\n", encoding="utf-8")
            (template_root / "CLAUDE.md").write_text("# Guide\n", encoding="utf-8")
            (template_root / "skills").mkdir()
            project = root / "demo"

            with patch.object(init_module, "_locate_templates", return_value=template_root):
                init_project(str(project))

            self.assertTrue((project / "CLAUDE.md").is_symlink())
            self.assertEqual((project / "CLAUDE.md").readlink(), Path("AGENTS.md"))

    def test_unsupported_integration_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()

            with self.assertRaisesRegex(InitError, "unsupported integration"):
                init_project(str(project), integration="claude")

    def test_existing_files_are_skipped_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()
            project.mkdir()
            agents = project / "AGENTS.md"
            agents.write_text("custom agents\n", encoding="utf-8")

            result = init_project(str(project), integration="codex")

            self.assertEqual(agents.read_text(encoding="utf-8"), "custom agents\n")
            self.assertIn(agents, result.skipped)

    def test_existing_shared_skills_are_skipped_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()
            skill = project / ".agents" / "skills" / "mykit-audit" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("custom skill\n", encoding="utf-8")

            result = init_project(str(project), integration="codex")

            self.assertEqual(skill.read_text(encoding="utf-8"), "custom skill\n")
            self.assertIn(skill, result.skipped)

    def test_force_overwrites_existing_template_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()
            project.mkdir()
            agents = project / "AGENTS.md"
            agents.write_text("custom agents\n", encoding="utf-8")

            result = init_project(str(project), integration="codex", force=True)

            self.assertNotEqual(agents.read_text(encoding="utf-8"), "custom agents\n")
            self.assertIn(agents, result.created)

    def test_force_overwrites_existing_shared_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()
            skill = project / ".agents" / "skills" / "mykit-audit" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("custom skill\n", encoding="utf-8")

            result = init_project(str(project), integration="codex", force=True)

            self.assertNotEqual(skill.read_text(encoding="utf-8"), "custom skill\n")
            self.assertIn(skill, result.created)

    def test_install_integration_repairs_missing_codex_skills(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()
            init_project(str(project), integration="codex")
            shutil.rmtree(project / ".agents" / "skills" / "mykit-audit")

            result = install_integration(project, "codex")

            self.assertTrue((project / ".agents/skills/mykit-audit/SKILL.md").is_file())
            self.assertIn(project / ".agents/skills/mykit-audit/SKILL.md", result.created)
            config = self._read_config(project)
            self.assertEqual(config["installed_integrations"], ["codex"])

    def test_install_integration_requires_initialized_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = (Path(tmp) / "demo").resolve()
            project.mkdir()

            with self.assertRaisesRegex(InitError, "mykit init --here"):
                install_integration(project, "codex")

    def _read_config(self, project: Path) -> dict[str, object]:
        return json.loads((project / ".mykit" / "config.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
