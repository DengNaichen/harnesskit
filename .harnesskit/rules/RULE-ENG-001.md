# RULE-ENG-001

## Rule

修改用户可见行为时，必须同步添加或更新自动化测试。

## Details

用户可见行为包括 Typer CLI、初始化逻辑、配置写入、模板输出、harness lint 行为、错误消息、退出行为和生成资产。测试必须证明新行为或回归场景。

证据：

- `tests/test_init.py`
- `harness-linter-poc/tests/test_*.py`
- `AGENTS.md`
- `.agents/skills/code-change-verification/SKILL.md`

验证：

- `uv run pytest`
- `make verify`
- `uv run pre-commit run --all-files`
- review 检查代码变更和测试变更是否匹配；测试命令只能证明现有测试通过。
