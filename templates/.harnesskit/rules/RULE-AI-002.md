# RULE-AI-002

## Rule

不要把模板示例、设计愿景、旧文档或未验证 facts 当成当前实现事实。

## Details

当前实现事实应从源码、测试、配置、脚本、锁文件、CI/hook 和已确认文档交叉验证。`.harnesskit/facts.md` 是扫描 handoff，不是仓库事实的替代品；使用前仍要按风险回到源文件核对。

证据：

- [NEEDS CLARIFICATION: 设计文档、实现入口和事实来源]

验证：

- [NEEDS CLARIFICATION: harness lint、review 或 drift check]
