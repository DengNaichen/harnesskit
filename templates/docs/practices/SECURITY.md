# Security Practices

本文件记录当前仓库实际存在的安全配置面和风险边界。它回答“在这个项目里，哪些地方改了会影响安全”，不重复通用安全建议。硬约束见 [RULES.md](../../RULES.md)。

<!-- harnesskit:todo-checklist:start -->
补全本文件前请确认：
- 从真实源码、配置、脚本、部署方式、依赖清单和测试入口中提炼安全 surface。
- 不要虚构 security policy、漏洞披露渠道、支持版本、响应 SLA、secret scan、dependency scan 或 CI security gate。
- 未确认内容保留 `[NEEDS CLARIFICATION: ...]`。
<!-- harnesskit:todo-checklist:end -->

## 安全配置面

### 认证、授权与访问控制

- [NEEDS CLARIFICATION: 本仓库是否有登录、会话、token、API key、权限模型、RBAC/ABAC、middleware、route guard 或管理后台访问控制；列出对应源码和配置路径。]
- [NEEDS CLARIFICATION: 哪些配置项或代码路径会改变认证、授权、权限校验、默认开放范围或管理入口暴露面。]

### 数据、文件写入与输出

- [NEEDS CLARIFICATION: 本仓库处理哪些敏感数据、用户数据、业务数据、日志、报告或生成资产；列出主要读写路径。]
- [NEEDS CLARIFICATION: 文件上传、下载、生成、覆盖、删除、临时目录、路径拼接或归档逻辑在哪里；哪些改动可能造成路径逃逸、覆盖用户内容或泄露本机路径。]
- [NEEDS CLARIFICATION: 日志、错误信息、导出文件、缓存、快照或诊断输出是否可能包含 secret、token、私有 URL、用户名、机器路径或真实用户数据。]

### 外部系统与依赖

- [NEEDS CLARIFICATION: 本仓库连接的数据库、对象存储、消息队列、第三方 API、认证服务、支付/通知服务、浏览器/系统命令或其他外部系统。]
- [NEEDS CLARIFICATION: 依赖清单、锁文件、插件、脚本、容器镜像或下载逻辑在哪里；新增依赖或外部命令会引入哪些信任边界。]
- [NEEDS CLARIFICATION: secret、token、证书、私钥、环境变量或本地配置应从哪里读取，哪些文件和输出禁止写入这些信息。]

## 当前安全检查能力

- [NEEDS CLARIFICATION: 当前是否已有 secret scan、dependency scan、SAST、权限测试、安全相关单元测试、pre-commit hook、CI security gate 或人工 review 要求；列出真实 runner 或说明未绑定。]
- [NEEDS CLARIFICATION: 当前没有自动化覆盖但必须人工检查的安全边界。]

## 和 Rules 的关系

- 稳定、可执行、必须遵守的安全约束应沉淀到 [RULES.md](../../RULES.md)，复杂背景保留在本文。
- 可自动检查的安全要求应绑定到测试、lint、pre-commit、CI 或其他 runner；没有 runner 证据时，只能写成 review 或待确认。
- 不要把本文中的待确认项改写成硬规则，除非已经用仓库事实或团队确认支撑。
