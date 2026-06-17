from __future__ import annotations

import sys
from pathlib import Path

from typer.testing import CliRunner


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import harnesskit.cli as cli_module  # noqa: E402
from harnesskit.cli import app  # noqa: E402


class FakeConsole:
    def __init__(self) -> None:
        self.messages: list[str] = []

    def print(self, message: str = "", *args, **kwargs) -> None:
        self.messages.append(str(message))


def test_init_selects_integration_from_interactive_menu(
    monkeypatch,
) -> None:
    fake_console = FakeConsole()
    calls: list[dict[str, object]] = []

    class FakeQuestion:
        def ask(self) -> str:
            return "codex"

    def fake_select(message, **kwargs):
        calls.append({"message": message, **kwargs})
        return FakeQuestion()

    monkeypatch.setattr(cli_module, "console", fake_console)
    monkeypatch.setattr(cli_module, "_has_interactive_terminal", lambda: True)
    monkeypatch.setattr(cli_module.questionary, "select", fake_select)

    assert cli_module._select_integration(None) == "codex"
    assert calls
    assert calls[0]["message"] == "Select agent integration"
    assert calls[0]["default"] == "codex"
    choices = calls[0]["choices"]
    assert [choice.title for choice in choices] == [
        "Codex (default)",
        "None / Skip for now",
        "Claude Code",
        "Cursor",
    ]
    assert choices[0].disabled is None
    assert choices[1].disabled is None
    assert choices[2].disabled is None
    assert choices[3].disabled == "coming soon"


def test_init_falls_back_to_default_integration_without_tty(monkeypatch) -> None:
    fake_console = FakeConsole()

    monkeypatch.setattr(cli_module, "console", fake_console)
    monkeypatch.setattr(cli_module, "_has_interactive_terminal", lambda: False)

    assert cli_module._select_integration(None) == "codex"
    assert any(
        "No interactive terminal detected" in item for item in fake_console.messages
    )


def test_init_can_select_no_integration_from_menu(monkeypatch) -> None:
    fake_console = FakeConsole()

    class FakeQuestion:
        def ask(self) -> str:
            return cli_module.NO_INTEGRATION_MENU_VALUE

    monkeypatch.setattr(cli_module, "console", fake_console)
    monkeypatch.setattr(cli_module, "_has_interactive_terminal", lambda: True)
    monkeypatch.setattr(
        cli_module.questionary,
        "select",
        lambda *args, **kwargs: FakeQuestion(),
    )

    assert cli_module._select_integration(None) is None


def test_disabled_menu_integrations_are_not_supported_install_targets() -> None:
    runner = CliRunner()
    result = runner.invoke(app, ["init", "demo", "--integration", "cursor"])

    assert result.exit_code == 1
    assert "unsupported integration 'cursor'" in result.output


def test_init_with_no_integration_skips_agent_assets(tmp_path: Path) -> None:
    runner = CliRunner()
    project = tmp_path / "demo"
    result = runner.invoke(app, ["init", str(project), "--no-integration"])

    assert result.exit_code == 0, result.output
    assert (project / "AGENTS.md").is_file()
    assert (project / "ARCHITECTURE.md").is_file()
    assert (project / "RULES.md").is_file()
    assert not (project / ".agents").exists()
    assert not (project / "CLAUDE.md").exists()


def test_lint_passes_generated_codex_project(tmp_path: Path) -> None:
    runner = CliRunner()
    project = tmp_path / "demo"

    init_result = runner.invoke(app, ["init", str(project), "--integration", "codex"])
    assert init_result.exit_code == 0, init_result.output

    lint_result = runner.invoke(app, ["lint", str(project)])

    assert lint_result.exit_code == 0, lint_result.output
    assert "Harness lint passed" in lint_result.output


def test_lint_passes_generated_claude_project(tmp_path: Path) -> None:
    runner = CliRunner()
    project = tmp_path / "demo"

    init_result = runner.invoke(app, ["init", str(project), "--integration", "claude"])
    assert init_result.exit_code == 0, init_result.output

    lint_result = runner.invoke(app, ["lint", str(project)])

    assert lint_result.exit_code == 0, lint_result.output
    assert "Harness lint passed" in lint_result.output


def test_lint_passes_generated_project_without_integration(tmp_path: Path) -> None:
    runner = CliRunner()
    project = tmp_path / "demo"

    init_result = runner.invoke(app, ["init", str(project), "--no-integration"])
    assert init_result.exit_code == 0, init_result.output

    lint_result = runner.invoke(app, ["lint", str(project)])

    assert lint_result.exit_code == 0, lint_result.output
    assert "Harness lint passed" in lint_result.output


def test_init_rejects_conflicting_integration_options(tmp_path: Path) -> None:
    runner = CliRunner()
    project = tmp_path / "demo"
    result = runner.invoke(
        app,
        ["init", str(project), "--integration", "codex", "--no-integration"],
    )

    assert result.exit_code == 1
    assert "pass either --integration or --no-integration" in result.output


def test_init_with_explicit_integration_skips_selector(
    monkeypatch, tmp_path: Path
) -> None:
    def fail_select(*args, **kwargs):
        raise AssertionError("selector should not run when --integration is provided")

    monkeypatch.setattr(cli_module.questionary, "select", fail_select)

    runner = CliRunner()
    project = tmp_path / "demo"
    result = runner.invoke(app, ["init", str(project), "--integration", "codex"])

    assert result.exit_code == 0, result.output
    assert (project / "AGENTS.md").is_file()
    assert (project / ".harnesskit/config.json").is_file()


def test_integration_list_includes_claude() -> None:
    runner = CliRunner()

    result = runner.invoke(app, ["integration", "list"])

    assert result.exit_code == 0, result.output
    assert "codex" in result.output
    assert "claude" in result.output
