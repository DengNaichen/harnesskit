# 规则

HarnessKit 当前通过 Harness Linter POC 支持以下确定性 guard。

## 已支持的 Guard

- 项目路径：目标路径必须是已经存在的目录。
- Harness 配置：`.harnesskit/config.json` 必须存在、能解析为 JSON，并使用受支持的 schema 和 integration 名称。
- 核心 harness 文件：`AGENTS.md` 和 `CLAUDE.md` 必须存在且非空；`CLAUDE.md` 必须指向 `AGENTS.md`。
- Codex integration 资产：已安装的 HarnessKit Codex skills 必须存在且非空。
- Skill 元数据：每个已安装的 `SKILL.md` 必须包含带 `name` 和 `description` 的 frontmatter。
- Skill 引用：`AGENTS.md` 中的 `$skill-name` 引用必须指向已安装的本地 skill。
- Markdown 引用：harness 文件中的本地 Markdown 链接必须指向真实存在的文件。
- Harness markers：`harnesskit:todo-checklist`、`harnesskit:tech-stack` 和 `harnesskit:verification` marker 必须成对出现。
- Architecture map：`ARCHITECTURE.md` 的 Markdown 链接可以声明 `harnesskit:coverage=direct-children`；hint 语法必须有效，被覆盖目录的直接子项必须被文档记录。
- Architecture placeholder：`ARCHITECTURE.md` 中的 placeholder 职责描述会报告 warning。
- 技术栈漂移：`harnesskit:tech-stack` block 会和仓库中检测到的事实对齐。
- 验证流程漂移：当仓库中存在对应工具时，验证文档会检查 pytest/unittest、Ruff check、Ruff format check 和 package build gate 是否对齐。
- 可选 Markdown 风格检查：传入 `--external-markdownlint` 时，会在已安装 markdownlint 的情况下运行它。

## 非目标

- 不检查应用源码风格。
- 不自动修复。
- 不依赖 LLM 判断。
