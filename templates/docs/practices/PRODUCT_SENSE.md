# Product Sense Practices

本文件记录从当前仓库中提取的产品判断约定。它回答“在这个项目里，什么算产品体验”，不重复通用产品设计建议。硬约束见 [RULES.md](../../RULES.md)。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从 README、产品文档、真实用户入口、配置、模板、生成输出、用户反馈或团队确认中提炼事实。
- 只写会影响产品体验判断的项目 surface、职责边界和风险区域；通用 UX 建议不要写进来。
- 明确区分当前已支持能力、配置开关、生成资产、文档说明、路线图和愿景。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## 产品定位

- [NEEDS CLARIFICATION: 本项目服务的用户、主要使用场景、核心用户结果，以及不服务的对象。]
- [NEEDS CLARIFICATION: 本项目的产品体验优先级，例如稳定、清晰、速度、可扩展、可审计或低配置成本。]

## 产品 Surface

### 用户入口

- [NEEDS CLARIFICATION: 主要用户入口，例如 UI、CLI、API、SDK、service、library、admin console 或 job runner，以及各自当前支持什么。]
- [NEEDS CLARIFICATION: 用户会直接感知的交互、错误信息、状态、权限、数据流或兼容性边界。]

### 配置和默认行为

- [NEEDS CLARIFICATION: 影响产品体验的配置文件、环境变量、开关、默认值和部署前提。]
- [NEEDS CLARIFICATION: 哪些默认值会影响首次体验、兼容性、数据安全、性能或用户信任。]

### 生成输出和集成

- [NEEDS CLARIFICATION: 本项目是否生成用户可消费的代码、配置、文档、报告、资产或集成输出；生成来源和输出位置是什么。]
- [NEEDS CLARIFICATION: 生成输出、模板、插件、integration、export 或 import 的质量标准和职责边界。]

## 文档约定

- [NEEDS CLARIFICATION: README 负责说明什么产品事实，哪些内容只是上游背景、演示、愿景或快速开始。]
- [NEEDS CLARIFICATION: docs、examples、API reference、runbook、agent context 或其他文档各自负责什么，不互相复制什么。]

## 风险边界

- [NEEDS CLARIFICATION: 哪些产品声明必须回到源码、配置、测试、真实部署或团队确认后才能写成事实。]
- [NEEDS CLARIFICATION: 哪些能力属于未来路线图、实验功能、演示功能、可选插件或外部系统，不应被写成当前默认能力。]

## 和 Rules 的关系

产品相关硬约束见 [RULES.md](../../RULES.md)。本文件只帮助判断“这个仓库里的产品体验通常应该怎么理解”。
