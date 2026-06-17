# Rules 说明

[RULES.md](../../RULES.md) 是给团队和 agent 共用的短规则索引。它不教 agent 怎么完成一类任务，也不承载完整项目地图；它只记录这个仓库里永远或局部必须遵守的约束。

Context Harness 中三类资产的边界是：

- **Skills** 教 agent 怎么做一类任务，例如扫描事实、判断兼容性、验证改动或刷新 context。
- **Rules** 告诉 agent 在这个仓库里必须遵守什么约束。
- **Validations** 负责把可检查的约束转成验证反馈，并记录它们在哪些 runner 中执行。

[AGENTS.md](../../AGENTS.md) 负责路由：告诉 agent 什么时候读 [RULES.md](../../RULES.md)、什么时候触发 skill、什么时候运行 validation。[RULES.md](../../RULES.md) 不应该替代 [AGENTS.md](../../AGENTS.md) 或 skill。

## 怎么使用

- 先以仓库事实为准，不要把模板里的示例当成已经启用的规则。
- 在 [RULES.md](../../RULES.md) 中保留短规则句，让 agent 能快速扫描。
- 把规则的解释、证据、例外和 validation 绑定放到 [.harnesskit/rules/](../../.harnesskit/rules/) 中的 `RULE-*.md` 或对应设计文档。
- 暂时确认不了的规则使用 `[NEEDS CLARIFICATION: ...]`，不要写成强制完成门槛。
- 修改验证入口、工具链、模板输出、架构边界或团队约定时，同步更新对应 rule、detail 文件和相关 skill。

## 当前结构

推荐把 [RULES.md](../../RULES.md) 分成面向工程实践的规则类别：

- **通用工程实践**：大多数代码库都适用的约束，例如新增行为必须有测试、依赖声明必须同步。
- **AI Coding 规则**：约束 agent 如何读取 context、处理漂移、避免凭空补全事实。
- **技术栈规则**：和当前仓库工具链强相关的约束，例如包管理器、lint、format、test、build。
- **架构规则**：和目录边界、模块职责、生成资产、运行时代码边界相关的约束。
- **产品 / 领域规则**：和当前项目定位、业务语义或不可破坏的领域约束相关的规则。

每条规则在索引里应尽量是一句话。详情文件再使用稳定字段：

- **Rule**：重复短规则句，方便详情文件独立阅读。
- **Details**：解释适用范围、例外和容易误判的地方。
- **Evidence**：列出支撑规则的仓库事实、配置、脚本、文档或人工确认来源。
- **Validation**：说明可执行检查、runner 绑定和当前执行/阻断强度。

## Rule、Skill 和 Validation

Rule 是开发时的行为约束，比如“新增行为必须有测试”或“模板输出是用户可见行为”。Skill 是完成任务的流程，比如“修改模板前先判断兼容性，再更新测试”。Validation 是可执行或可检查的验证方式，比如 lint、test、build、pre-commit、CI required checks 或 review。

能确定性验证的规则应尽量绑定 Validation；不能完全自动验证的规则，也要写清楚由哪些工具和 review 共同兜底。

## 可验证程度

- **确定性**：可以用命令或平台配置得到明确 pass/fail，例如 lint、format check、test、build、pre-commit、required checks。
- **部分确定性**：工具只能验证一部分，剩下需要 review 判断，例如“新增行为是否有足够测试”“命名是否符合本仓库惯例”“架构说明是否准确”。
- **人工/agent review**：主要依赖人或 agent 审查，暂时没有稳定命令能判断。
- **未配置**：当前仓库没有对应工具、流程或事实来源；agent 不应把它写成完成条件。

## 文件关系

- [`../../RULES.md`](../../RULES.md)：HarnessKit 当前仓库已经确认或待确认的规则。
- [`../../templates/RULES.md`](../../templates/RULES.md)：安装到目标仓库时使用的通用模板。
- [`AGENTS.md`](AGENTS.md)：[AGENTS.md](../../AGENTS.md) 的设计说明，解释 agent 操作入口如何消费规则和技能。
- [`ARCHITECTURE.md`](ARCHITECTURE.md)：[ARCHITECTURE.md](../../ARCHITECTURE.md) 的设计说明，解释架构地图如何承载目录职责和边界。
- [`DESIGN.md`](DESIGN.md)：Rule / Validation 模型背后的产品设计说明。
