# Harness Builder MVP 框架：Scan → Rule → Guard 循环

> 状态：设计讨论收口。基于 OpenAI / Anthropic harness 研究和内部产品方向讨论整理。
>
> 日期：2026-06-13

---

## 1. 核心问题：在一切皆概率的系统中寻找守恒量

大模型是概率模型，模型能力在变，harness 模式在变，工具链在变，用户预期在变。在这个所有东西都在漂移的系统里，需要找到一个不变量（守恒量）作为工程锚点。

**守恒量 = Git**

- **宿主无关**：不管 agent 跑在 Codex、Claude Code、Cursor 还是 vim 里，最终都要 `git commit`。不需要适配任何宿主 API。
- **确定性**：repo 状态就是项目事实。diff 是什么就是什么，hash 是什么就是什么，没有概率。
- **自带触发点**：pre-commit、pre-push hook 是天然闸门，不需要额外发明触发机制。
- **自带审计链**：commit history 本身就是证据链。
- **所有 agent 都已经会用它**：不需要教 agent 学新协议。

**一切建立在 Git + Hook 上。**

---

## 2. Harness 三层分类与 MVP 边界

| 层级 | 含义 | 代表参考 | 是否做 |
|------|------|----------|--------|
| **Context Harness** | 项目级上下文、规则、约束、验证契约、evidence 入口 | OpenAI Harness Engineering, Codex agent loop | ✅ **MVP 唯一边界** |
| **Agent Runtime Harness** | agent loop、sandbox、权限、工具注册、shell/browser 执行 | Anthropic long-running agents, managed agents | ❌ 宿主产品自带 |
| **Controller / Orchestration** | 多 agent 调度、issue → workspace 映射、DAG 依赖 | OpenAI Symphony | ❌ 未来方向 |

MVP 只负责 Context Harness：初始化并维护目标项目中 agent-friendly 的 context、规则、验证契约和 evidence 入口。不实现 Agent Runtime，不实现 Controller / Orchestration。

不需要控制 agent 怎么跑（那是 Runtime 的事），只需要控制它**提交什么**。Git hook 就是那道门。

### 为什么需要 Context Harness

AI agent 需要稳定、可复用、随代码一起演进的本地上下文，而不是依赖某一次对话里的临时说明。Context Harness 的作用，就是把项目知识沉淀成仓库中的文件：

- `AGENTS.md`：agent 的操作规则和仓库导航入口
- 架构或质量文档：更深入的工程约束
- 生成或人工整理的参考资料：避免 agent 凭空猜测关键事实
- 验证入口：把自然语言规则连接到可执行检查

`AGENTS.md` 应该保持克制，专注于“agent 在这个仓库里应该怎么工作”。至于 HarnessKit 是什么、为什么存在、MVP 边界在哪里，这些项目定位说明应该放在 `README.md`。

### Context Harness 资产边界

HarnessKit 安装到目标仓库中的资产可以理解为面向 agent 的技术治理层，主要包括：

- 清晰的仓库入口说明
- 项目结构和架构边界
- 开发、测试和验证命令
- 质量、可靠性和安全规则
- agent 可以按需渐进式读取的参考资料

这些资产只定义项目级上下文、规则、约束和验证入口。它们不负责运行 agent，也不负责实现工具沙箱、权限系统、长期任务调度或多 agent 编排；这些能力属于宿主产品或未来的 controller / orchestration 层。

### Scan、Harness 与 Workflow 的边界

Agent 的主要瓶颈通常不是写代码速度，而是目标成形：把模糊意图拆解成清晰目标、边界条件、执行顺序和可验证的完成标准。只要目标、上下文和约束足够明确，代码修改往往会变成相对机械的执行工作。

因此需要区分三类产品问题：

- **Scan**：回答“当前仓库这个物理世界是什么”。它通过读取代码、配置、文档和工具链来建立坐标系，测绘项目地形，提取后续 Harness 和 Workflow 必须依赖的事实。
- **Harness**：回答“agent 如何持续拥有正确的上下文、边界和验证入口，不偏离轨道”。它不是路径本身，而是约束、护栏、坐标系、反馈和纠偏机制。
- **Workflow**：回答“这次任务应该怎样被拆解、按什么顺序推进、什么时候停”。它像是在既定坐标系和约束条件下，为 agent 画一条任务级的最速降线，让不确定性尽早下降，后续执行获得速度。

用物理类比说，经典力学必须先有坐标系；agent workflow 也必须先有仓库坐标系。HarnessKit 当前先建立坐标系并安装约束，下一阶段才是在这个系统里求最速降线。换句话说：Scan 负责测绘地形，Harness 负责安装约束，Workflow 负责画出路径。

当前 HarnessKit 的边界是 Scan + Harness，而不是 Workflow Builder。它可以帮助 agent 保持在正确的项目事实、规则和验证约束中，但不假装知道某个具体任务的最优轨道长什么样。这也是 MVP 的重要限制：HarnessKit 维护的是执行任意 workflow 所需的稳定上下文和约束；任务级目标拆解、路径优化和 workflow 生成属于后续产品层。

这个最速降线类比只是设计语言，不是形式化物理证明。它的价值在于帮助切清产品边界：先建立坐标系，再安装约束，最后才讨论如何优化路径。如果类比不能指导边界、接口或交付范围，就不应继续扩大。

### Harness Preservation 与 Harness Evolution

MVP 暂不追求让 harness 在使用中自动进化成更完整的架构体系；这属于后续的 Harness Evolution。当前更重要的是 Harness Preservation：确认已有的 `AGENTS.md`、skills、配置、验证入口和文档引用仍然存在、可读、可解释，并且没有明显漂移。

---

## 3. 核心循环：Scan → Rule → Guard

### 循环模型

```
Scan → 读 git repo，提取项目事实（技术栈、构建工具、linter、CI 配置等）
  │
Rule → 基于事实生成的项目级规则框架，写进 repo，引导 agent
  │
Guard → 确定性验证，通过 git hook 执行，拦截不合格的 commit
  │
Git commit → 唯一的状态变更入口
```

### 闭环控制

```
Agent 改代码（被 Rule 引导）
       │
       ▼
   尝试 commit
       │
       ▼
  ┌─ Hook 触发 Guard ──┐
  │                     │
  │  pass → commit 成功 │
  │                     │
  │  fail → 拦截        │
  │    │                │
  │    ▼                │
  │  Agent 看到失败原因  │
  │  回去改代码          │
  │    │                │
  └────┘ ← 循环直到 pass │
```

Agent 不需要一次做对，只需要收敛。Rule 让它大概往对的方向走，Guard 在每次 commit 时给出确定性的 pass/fail 反馈，agent 根据反馈修正，再试，直到通过。

---

## 4. Rule 与 Guard 的本质区分

| | Rule | Guard |
|---|---|---|
| **性质** | 指导性、偏好性、概率性 | 确定性、可执行、可判定 |
| **作用** | 引导 agent 往对的方向走 | 拦住 agent 不让它越界 |
| **验证方式** | 只能靠 agent 自己理解和遵循 | 可以跑一个命令，返回 pass/fail |
| **失败模式** | agent 可能忽略，但不一定是错 | 违反就一定是错 |

**Rule 是在概率空间里给模型施加的势场，影响模型的输出分布，但不能硬保证结果。**

**Guard 是确定性的守恒量本身，可验证、不依赖模型。**

核心设计原则：
- Rule 和 Guard 必须配对出现才有闭环
- 每条 Guard 背后应有一条 Rule 解释"为什么有这个约束"
- 每条 Rule 尽可能衍生出一个 Guard 来兜底
- 能变成 Guard 的 Rule 就应该下沉为 Guard；实在不能确定性验证的，才留在 Rule 层

### Rule 的内容范围

Rule 的内容是**人能判断对错，但机器没法一条命令判定**的东西：

1. **架构偏好与风格指导**："本项目倾向组合优于继承"
2. **技术选型的 why**：Scan 能知道用了什么，Rule 要说清楚为什么用、什么场景不该换
3. **取舍方向**："性能和可读性冲突时，优先可读性"
4. **反模式与历史教训**："不要用 X 方案，试过了，因为 Y 原因放弃"
5. **领域知识中的软约束**："所有价格字段用分不用元"
6. **渐进式加载路标**："修改 X 模块前先读对应文档"

### Guard 的内容范围

Guard 的内容是**可以用一条命令或一段确定性逻辑判定 pass/fail** 的东西：

- `npm run lint` / `npm run typecheck` / `npm test` 必须通过
- 模块依赖边界（可用 import 分析工具验证）
- 命名约定（可用 eslint rule 验证）
- 禁用模式（可用 grep 验证）
- Schema 校验必须通过
- 构建产物约束

### Rule 的关键特性：不能预生成，是涌现的

好的项目规则是团队在真实开发中踩坑、做取舍、建共识的结果。没有人能对着一个空项目写出有价值的 Rule。

但 Rule 不是空的，应该提供**分类框架**：
- 告诉团队"这几类东西应该写成 Rule"
- 每个分类下给出填写引导
- Scan 结果可以预填一些显而易见的项（如检测到的技术栈、代码风格配置）
- 需要团队补充的部分留空 + 提示

Rule 框架结构示例：

```
rules/
├── architecture.md    # Scan 可预填：检测到的分层结构、依赖方向
├── conventions.md     # Scan 可预填：检测到的命名风格、代码风格配置
├── tech-choices.md    # Scan 可预填：用了什么包/框架；why 要人写
├── anti-patterns.md   # 纯人工填写：试过什么、为什么放弃了
└── quality.md         # Scan 可预填：测试覆盖率阈值、lint 严格度
```

Rule 是半自动的：Scan 提供事实，框架提供结构，团队填语义，doc lint 检查一致性。

---

## 5. 文档级 Lint（Doc Lint）

### 依据

OpenAI Harness Engineering 文章明确提到：

> "专职 linter 和 CI 作业会验证知识库的更新状况、是否已交叉链接且结构正确。"
>
> "一个定期运行的 'doc-gardening' 智能体会扫描那些不再反映真实代码行为的过时或废弃文档，并发起修复用的 Pull Request。"

文档腐烂是确定性问题，可以用确定性工具解决，不需要 LLM。

### 可确定性检查的维度

| 检查项 | 实现方式 |
|--------|----------|
| **新鲜度** | doc 的最后修改时间 vs 它引用的代码文件的最后修改时间。代码变了但文档没更新 → 告警 |
| **交叉链接完整性** | doc 里引用的文件路径是否真实存在 |
| **结构合规** | 文档是否符合预定义的 schema / 模板结构 |
| **覆盖率** | 主要模块是否都有对应文档 |
| **孤儿检测** | 有没有文档没被任何地方引用 |
| **同步漂移** | `git log` 追踪代码和文档的变更是否同步 |

### 可复用的开源工具

不需要从零构建，组合现有工具即可：

| 工具 | 用途 |
|------|------|
| **markdownlint** | Markdown 格式/风格检查 |
| **markdown-link-check** | 文档内链接完整性 |
| **remark-lint-docs-freshness** | 基于 frontmatter `reviewed` 日期的新鲜度检查 |
| **DocDrift** (`ayush698800/docwatcher`) | 扫描 git diff，代码变更时检测相关文档是否需要更新 |
| **DocSync** (`suhteevah/docsync`) | 基于 tree-sitter 的代码-文档同步检测 |
| **stale-md** | 超过 N 天未修改的 Markdown 告警 |
| **checkdoc** | 孤儿文档和断链检测 |

上述工具串进 git pre-commit hook 或 CI 即为 doc lint Guard。

---

## 6. MVP 交付范围

| 组件 | 自动化程度 | 依赖 LLM | 需要团队配合 |
|------|-----------|----------|-------------|
| **Scan** | ✅ 全自动 | ❌ | ❌ |
| **Rule 框架** | 半自动（Scan 预填 + 人工补充引导） | ❌ | ⚠️ 填语义部分 |
| **Guard** | ✅ 全自动（Scan 结果 → hook 生成） | ❌ | ❌ |
| **Doc Lint** | ✅ 全自动（组合现有工具） | ❌ | ❌ |

### 关键约束

- MVP 全部锚定在 Git 上
- MVP 全部确定性，不依赖 LLM
- 需要人配合的部分尽量少
- 目标：`git clone` 下来自动生效，零配置，零学习成本

### Guard 从 Scan 结果自动推导

- 扫到 eslint → Guard 加 `npm run lint`
- 扫到 TypeScript → Guard 加 `npm run typecheck`
- 扫到 test 框架 → Guard 加 `npm test`
- 挂到 git pre-commit hook

### 非当前目标：动态上下文渲染

可以探索用结构化事实源（如轻量 SQLite、SQL seed 或 YAML）作为 Context Harness 的事实来源，再通过 Codex `UserPromptSubmit` hook 在每次用户消息提交时刷新一个 agent 可读的 Markdown snapshot。这个方向可以降低手写 Markdown 被误改的风险，让 agent 读取的是由结构化事实渲染出的上下文。

但这不是当前 MVP 目标，原因是：

- Codex hook 是宿主相关能力，不适合作为所有 agent 的唯一入口。
- 动态渲染不应替代 Git hook / pre-commit 这类确定性 Guard。
- 每次消息都重写主文档会污染工作区；更合理的是写入 `.harnesskit/generated/` 之类的快照目录。
- agent 是否会读取动态快照仍然需要稳定的 bootstrap 文档说明。

更稳的后续形态是：结构化事实源负责保存机器可校验的数据，Markdown snapshot 负责给人和 agent 阅读，pre-commit 负责检查两者是否同步。当前阶段只记录这个方向，不实现。

---

## 7. 风险与待决事项

### 已确认的风险

| 风险 | 评估 | 应对 |
|------|------|------|
| 模型进化可能压缩 Rule 层价值 | ⚠️ Rule 会被压缩，Guard 不会 | 产品重心偏 Guard |
| Git hook 在 agent 云端沙箱中可能不生效 | ⚠️ Codex 等平台的沙箱可能绕过 hook | 需要设计更抽象的"验证入口" |
| Rule 层的抽象粒度难以把握 | ⚠️ 太笼统无用，太具体易腐烂 | 先给框架，让团队填内容，用 doc lint 检查一致性 |
| 时间窗口压力 | ⚠️ 领域变化极快 | 快速交付最小可用形态 |

### 后续待验证

- Guard 的执行锚点是否需要从 git hook 扩展为更抽象的验证入口（适配云端 agent 环境）
- Rule 框架中哪些分类对低工程纪律团队最有价值
- doc lint 的哪些检查维度在实际使用中误报率最低
- 整个循环在真实项目上端到端跑通后的反馈
