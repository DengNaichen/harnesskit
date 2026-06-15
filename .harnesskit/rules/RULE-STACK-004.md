# RULE-STACK-004

## Rule

影响 package、模板打包或构建配置时，必须确认 `uv build` 通过。

## Details

HarnessKit 使用 Hatchling 构建包。影响 package metadata、模板打包或构建配置的变更必须证明 package build 仍然成功。

证据：

- `pyproject.toml`
- `.pre-commit-config.yaml`
- `.agents/skills/code-change-verification/SKILL.md`

验证：

- `uv build`
- `make verify`
