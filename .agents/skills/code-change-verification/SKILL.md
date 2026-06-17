---
name: code-change-verification
description: 当变更影响运行时代码、测试、模板生成行为或构建/验证行为时，运行仓库强制验证栈。
---

# 代码变更验证

## 概览

确保只有在仓库可用验证命令通过后，才把工作标记为完成。变更影响运行时代码、会改变生成行为的模板、测试或构建/测试配置时使用本 skill。纯文档或仓库元数据变更可跳过，除非用户要求完整验证栈。

## 快速开始

1. 保持本 skill 位于 [`.agents/skills/code-change-verification`](./)，让仓库能自动加载它。
2. 如果依赖未安装或依赖发生变化，先运行 `uv sync`。
3. 在仓库根目录运行：
   ```bash
   make verify
   ```
4. 如果命令失败，修复问题，重新运行，并报告最终失败输出。
5. 只有命令成功且没有剩余问题时，才确认完成。

## 手动流程

- 如果依赖未安装或依赖发生变化，先运行 `uv sync`。
- 从仓库根目录运行 `make verify`。它会调用 [`scripts/run_validation.py`](scripts/run_validation.py) 中的 skill runner。
- 确认 runner 写入 `.harnesskit/receipts/latest.json`；有帮助时在最终回复中引用 receipt 路径。
- 只有排查失败时才使用 `make verify-core`、`make hooks` 或单个 Make target。
- 本仓库当前没有 type checker 或 docs build 命令；不要虚构这些检查。
- 修复后重新运行测试/验证命令，确保最终报告对应当前 working tree。

<!-- harnesskit:verification:start -->
- Full verification: make verify
- Markdown links: lychee './**/*.md'
- Python lint: uv run ruff check .
- Python format: uv run ruff format --check .
- Tests: uv run pytest
- Package build: uv build
- Pre-commit hooks: uv run pre-commit run --all-files
<!-- harnesskit:verification:end -->
