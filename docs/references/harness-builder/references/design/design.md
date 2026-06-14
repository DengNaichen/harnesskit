# OpenAI Harness 目录结构与设计轮廓

以下是 OpenAI Harness Engineering 实践中所推荐的项目资产（Harness）目录结构，以及各部分**“写什么（What）”**与**“为什么这么写（Why）”**的轮廓分析。

```
AGENTS.md
ARCHITECTURE.md
docs/
├── design-docs/ # discard
│   ├── index.md
│   ├── core-beliefs.md
│   └── ...
├── exec-plans/ # discard
│   ├── active/
│   ├── completed/
│   └── tech-debt-tracker.md
├── generated/   # 疑虑
│   └── db-schema.md
├── product-specs[EXCLUDED]/   #明确不做，spec是业务强相关的，我们只做纯技术治理资产
│   ├── index.md
│   ├── new-user-onboarding.md
│   └── ...
├── references/ 
│   ├── design-system-reference-llms.txt
│   ├── nixpacks-llms.txt
│   ├── uv-llms.txt
│   └── ...
├── DESIGN.md                   # MVP不做
├── FRONTEND.md                 # MVP不做
├── PLANS.md
├── PRODUCT_SENSE.md            # MVP不做
├── QUALITY_SCORE.md
├── RELIABILITY.md
└── SECURITY.md
```

---

## 1. 核心入口域 (Core Entrypoints)

### `AGENTS.md`
*   **写什么 (What)**: 
    *   整个项目的“交通枢纽”与“认知地图”，主要由三大部分构成：
        1.  **策略与强制规则 (Policies & Enforcement Rules)**: 声明强制的 AI 技能/微工具调用（例如 `$code-change-verification` 变更验证、`$implementation-strategy` 兼容性决策、`$pr-draft-summary` 总结等）、ExecPlan（执行计划）启用门槛、API 兼容性红线以及特定的安全边界。
        2.  **项目结构与 Domain Knowledge**: 简短的项目目录树，以及重点填写的“项目特有运行时准则”（如主入口文件逻辑边界、多文件联动规则、Schema/状态版本联动等无法通过扫描自动提取的架构约束）。
        3.  **操作指南 (Operations)**: 包含前提条件、核心开发工作流、本地工具链回归命令（测试、格式化、静态检查）及 PR 提交与审查规范。
    *   *注：此文件是一个由 Harness Builder 渲染的模板，其中工具链命令和项目元数据通常由 Builder 从 Makefile/pyproject.toml/GitHub Actions 等配置中自动提取并渲染插值。*
*   **为什么 (Why)**: 这是 Agent 接入项目时读取的第一站。它不需要是长篇累牍的手册，而应该像一张“轻量级的索引地图”。由于 Agent 的上下文窗口（Context Window）和注意力资源是有限的，最省 Token 且不易产生注意力漂移的实践是：在根入口仅加载高空俯瞰索引，需要时由 Agent 自行“渐进式加载”子目录。

### `ARCHITECTURE.md`
*   **写什么 (What)**: 
    *   专为 AI 建立项目全局心智模型（Mental Model）的“边界声明书”：
        1.  **分层架构心智模型**: 系统的宏观组件划分（如 UI 侧、Skill 逻辑层、Engine 引擎层）以及各自的核心职责界定。
        2.  **模块依赖红线 (Dependency Boundaries)**: 严厉声明哪些模块之间**绝对禁止**存在引用关系（例如：*“Engine 引擎层绝不能逆向 import 任何 Skill 层的 LLM 逻辑”*）。
        3.  **核心数据流与 Source of Truth**: 描述核心状态（如 Facts -> Proposal Bundle -> Draft -> Promote）的单向流转逻辑，以及谁拥有数据的最高写入权限。
        4.  **核心设计信念**: 规范项目内的主导设计模式（如：强制使用强 Zod schema 作为协议，禁止使用隐式 ad-hoc 转换器）。
*   **为什么 (Why)**: 
    *   **是否需要**：取决于项目规模。对于简单或纯库类项目（如 OpenAI 的 python 样例），其架构规则极少，直接嵌在 `AGENTS.md` 里的 `Domain Knowledge` 即可，无需单独设立；但对于**中大型或包含复杂多组件协作的项目**，单独设立此文件是极佳的实践。
    *   **防 Spaghetti Code**：大模型编写局部代码时非常容易为了便利而打破架构分层（乱引入模块）。独立的架构声明不仅能够拉起安全依赖红线，还可以作为“渐进式加载”的可选深读文件，避免在 Agent 每次对话的根入口中塞入过多的冗余架构说明。

---

## 2. 演进与规范域 (Standards & Evolution Docs)

### `docs/design-docs/` (设计决策记录 / ADR)
*   **写什么 (What)**: 
    *   `core-beliefs.md`: 开发团队的核心技术信念（如：测试驱动、强 schema 约束）。
    *   具体的决策记录 (RFC / Design Docs): “为什么要这么设计”、“做过哪些取舍”、“为什么放弃了备选方案”。
*   **为什么 (Why)**: Agent 在重构或优化代码时，极易重蹈覆辙（把过去因为踩坑而废弃的旧方案当作新思路重新写一遍）。这些决策记录是“防止 Agent 历史倒退”的防腐层，告诉它“为什么现在是这个状态”。

### `docs/product-specs/` (产品规格说明 - 明确不做)
*   **为什么不做 (Rationale)**: 
    *   **非技术治理资产**：根据 `AGENTS.md` 中的硬约束，Harness 是项目级的技术治理资产，不生成业务功能级的规则手册。
    *   **高维护成本与极易滞后**：业务规则多变且主观性高，自动生成的产品规格极易腐烂。Agent 应当直接阅读项目内的 Zod Schema、类型系统与单元测试来理解确定性的业务契约（Source of Truth）。

---

## 3. 标准与评价指标 (Rules & Evaluation Criteria)
*这部分文件位于根目录下，专注于各技术维度的核心准则。*

*   **写什么 (What)**:
    *   `DESIGN.md`: 通用设计规范，系统美学。
    *   `FRONTEND.md`: 前端组件复用原则、样式隔离标准等。
    *   `PLANS.md`: 任务规划与拆解的标准方法（比如要求每次开工前产出 CGA 和 Plan）。
    *   `PRODUCT_SENSE.md`: 产品体验与交互层面的及格线（要求微交互、禁用占位符等）。
    *   `QUALITY_SCORE.md` & `RELIABILITY.md` & `SECURITY.md`: 质量、可靠性、安全维度的红线指标。
*   **为什么 (Why)**:
    *   **职责解耦**：当 Agent 在做前端修改时，只需加载 `FRONTEND.md`，不需要加载 `SECURITY.md`，实现 Token 的高密度利用。
    *   **作为 Lint 或 Evals 的规则源**：这些文档不仅是给 Agent 读的，更是给后续的 Audit Engine 校验生成的产物是否合格的 Ground Truth 依据。

---

## 4. 执行状态域 (Execution Control)

### `docs/exec-plans/` (执行计划跟踪)
*   **写什么 (What)**:
    *   `active/`: 当前正在执行的端到端纵向切片计划。
    *   `completed/`: 近期已合入主干的计划记录，留作历史对比。
    *   `tech-debt-tracker.md`: 开发过程中发现但未在当前 Milestone 解决的遗留技术债务，作为未来的 Todo 候选池。
*   **为什么 (Why)**: 确保在多 Agent 协作或长周期任务中，Agent 能清晰感知“我们目前在整个交付链路的哪个环节”，避免盲目猜测进度或在错误的分支上叠加工作。

---

## 5. 辅助输入域 (Augmented Entrances & Outputs)

### `docs/references/` (大模型专有参考)
*   **写什么 (What)**:
    *   `*-llms.txt`: 专为 LLM 优化的精炼参考手册（如 Nixpacks, uv, Design System 的命令行速查表或 API 坑点提示）。
*   **为什么 (Why)**: 许多现代轻量级工具（如 `uv`）的最新特性超出了大模型的知识预训练切片，或者官网文档噪声过多。为 Agent 精炼一份“大模型友好版”的无噪指令集，能显著提升 Agent 在使用这些外部工具时的成功率，防止在未知报错里打转。

### `docs/generated/` (机器生成事实)
*   **写什么 (What)**:
    *   由编译/静态分析工具在 CI 或本地自动生成的项目事实文件（如：最新的数据库表拓扑 `db-schema.md`）。
*   **为什么 (Why)**: 排除“人工手写文档滞后”导致的认知偏差。Agent 在做变更时，必须基于 100% 确定性的自动生成结果（Source of Truth），而不是人类两周前更新的过期文档。