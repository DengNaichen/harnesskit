# RULE-ENG-001

## Rule

修改用户可见行为时，必须同步添加或更新自动化测试。

## Details

本规则是 testing 边界，不是完整测试策略。用户可见行为包括 Typer CLI、初始化逻辑、配置写入、模板输出、harness lint 行为、错误消息、退出行为和生成资产。测试必须证明新行为、回归场景或模板生成差异。

适用范围：

- CLI 命令、参数、输出、错误消息或退出码变化。
- `init_project()`、integration 安装、[.harnesskit/config.json](../config.json) 写入或模板渲染变化。
- `harnesskit lint` 的规则、issue、退出行为或扫描边界变化。
- 打包输出、模板包含关系或生成资产变化。

不适用：

- 纯文字修正，且不改变命令、模板输出或配置语义。
- 注释、内部重命名或无行为差异的整理；但 review 仍需确认现有测试覆盖没有被削弱。

违反形态：

- 修改用户可见行为但没有新增或更新对应测试。
- 改了模板生成内容但没有同步 [tests/test_init.py](../../tests/test_init.py) 或等价覆盖。
- 只运行测试命令，却没有检查测试是否覆盖了本次行为变化。

证据：

- [tests/test_init.py](../../tests/test_init.py)
- [harness-linter-poc/tests/](../../harness-linter-poc/tests/) 中的 `test_*.py`
- [tests/test_harnesskit_cli.py](../../tests/test_harnesskit_cli.py)
- [AGENTS.md](../../AGENTS.md)
- [.agents/skills/code-change-verification/SKILL.md](../../.agents/skills/code-change-verification/SKILL.md)

验证：

- runner：`uv run pytest`
- runner：`make verify`
- runner：`uv run pre-commit run --all-files`
- review：检查代码、模板或 CLI 变更和测试变更是否匹配；测试命令只能证明现有测试通过，不能自动证明测试覆盖了本次意图。
