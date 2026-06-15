# Rules 说明

`RULES.md` 是给团队和 agent 共用的工程规则清单。它把仓库里的事实、约定和完成门槛写成明确指令，让 agent 开发时知道哪些事情必须遵守、哪些检查必须通过、哪些规则目前还只是待确认。

## 怎么使用

- 先以仓库事实为准，不要把模板里的示例当成已经启用的规则。
- 能确认的规则写清楚状态、事实来源、agent 契约、Guard 类型和 Guard。
- 暂时确认不了的规则保留待确认；确认未配置的规则标记为未配置。
- 修改验证入口、工具链、模板输出、架构边界或团队约定时，同步更新 `RULES.md`。

## 当前结构

`RULES.md` 现在分成三块：

- **基础候选规则**：多数仓库都应该优先确认的规则，例如单一验证入口、新增行为必须有测试、测试入口以仓库事实为准、命名风格、依赖同步、context harness 不漂移。
- **可选规则**：只有仓库已经配置对应工具或流程时才启用，例如 branch protection、锁文件一致性、type check、coverage、linter、formatter、build、pre-commit、Architecture Map。
- **项目命令绑定**：把规则落到当前仓库真实命令上，例如 test、lint、format check、build、hook suite；没有配置的命令写 `N/A`。

每条规则都使用同一组字段：

- **状态**：规则在当前仓库里是已确认、部分确认、待确认、未配置还是不适用。
- **事实来源**：支撑这条规则的文件、配置、脚本、CI、平台设置或人工确认来源。
- **agent 契约**：用祈使句写 agent 开发时必须怎么做。
- **Guard 类型**：说明这条规则当前能被工具验证到什么程度。
- **Guard**：写具体命令、hook、CI gate、review gate 或待补配置。

## 规则速览

基础候选规则：

- **RULE-001 单一验证入口**：把本地开发、agent 交付和 CI 的完整验证收敛到同一入口，避免不同角色运行不同检查。
- **RULE-002 新增行为必须有测试**：要求功能、bug fix、CLI、配置或模板输出变化配套自动化测试，避免只改代码、不证明行为。
- **RULE-003 Test 入口以仓库事实为准**：让测试命令跟随仓库真实测试框架，避免文档或 agent 继续使用过期入口。
- **RULE-004 命名遵守本仓库现有风格**：让新增代码融入本地代码风格；工具能拦一部分，仓库惯例主要靠 review。
- **RULE-005 import 和依赖必须同步**：新增第三方引用时同步依赖清单和锁文件，避免在干净环境里缺依赖。
- **RULE-006 文档和 context harness 不漂移**：保持 `AGENTS.md`、`RULES.md`、`ARCHITECTURE.md`、skills 和验证说明与仓库事实一致。

可选规则：

- **RULE-101 Branch protection 和 required checks**：用代码托管平台保护主干，确保合并前检查和 review 已满足。
- **RULE-102 锁文件一致性**：用 locked install 或等价检查保证依赖安装可复现。
- **RULE-103 Type check**：在仓库配置类型检查时，用它提前发现接口、类型和数据形状问题。
- **RULE-104 Linter**：用静态 lint 拦住确定性的代码质量、错误模式和风格问题。
- **RULE-105 Formatter check-only gate**：把格式检查作为完成门槛，但完成检查只使用 check-only 命令。
- **RULE-106 Build 进入验证入口**：仓库有 package、应用或产物构建时，把 build 纳入交付验证。
- **RULE-107 Pre-commit 或 hook suite**：把 pre-commit 或同类 hook 当作验证套件，但不要把它误认为唯一 Guard。
- **RULE-108 Architecture Map**：让 agent 修改模块前理解目录职责和边界，重要职责变化时同步架构地图。
- **RULE-109 测试覆盖率 gate**：在仓库配置 coverage 时，把覆盖率作为辅助质量信号；它不能替代新增行为测试。

## Rule 和 Guard

Rule 是开发时的行为约束，比如“新增行为必须有测试”或“命名遵守本仓库现有风格”。Guard 是可执行或可检查的验证方式，比如 lint、test、build、pre-commit、CI required checks 或 review gate。

能确定性验证的规则应尽量绑定 Guard；不能完全自动验证的规则，也要写清楚由哪些工具和 review 共同兜底。

## 可验证程度

- **确定性**：可以用命令或平台配置得到明确 pass/fail，例如 lint、format check、test、build、pre-commit、required checks。
- **部分确定性**：工具只能验证一部分，剩下需要 review 判断，例如“新增行为是否有足够测试”“命名是否符合本仓库惯例”“架构说明是否准确”。
- **人工/agent review**：主要依赖人或 agent 审查，暂时没有稳定命令能判断。
- **未配置**：当前仓库没有对应工具、流程或事实来源；agent 不应把它写成完成条件。

## 文件关系

- [`../../RULES.md`](../../RULES.md)：HarnessKit 当前仓库已经确认或待确认的规则。
- [`../../templates/RULES.md`](../../templates/RULES.md)：安装到目标仓库时使用的通用模板。
- [`AGENTS.md`](AGENTS.md)：`AGENTS.md` 的设计说明，解释 agent 操作入口如何消费规则和技能。
- [`ARCHITECTURE.md`](ARCHITECTURE.md)：`ARCHITECTURE.md` 的设计说明，解释架构地图如何承载目录职责和边界。
- [`DESIGN.md`](DESIGN.md)：Rule / Guard 模型背后的产品设计说明。
