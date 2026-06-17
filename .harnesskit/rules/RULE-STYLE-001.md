# RULE-STYLE-001

## Rule

代码变更必须遵循现有模块边界；跨边界重构需要明确理由和验证。

## Details

本规则保护维护性边界，不把所有代码品味写成硬规则。日常编码判断参考 [docs/practices/CODING.md](../../docs/practices/CODING.md)。如果变更需要移动职责、拆分模块、引入新抽象或跨 runtime/template/linter/docs 边界调整，必须说明为什么这个边界变化是必要的，并提供对应测试或 review 证据。

违反形态：

- 为窄变更引入无必要的新抽象或跨模块重排。
- 把 runtime、template、linter、docs 或 POC 边界混在一起修改，却没有说明原因。
- 顺手重构造成大量无关 diff，增加 review 风险。

证据：

- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [docs/practices/CODING.md](../../docs/practices/CODING.md)
- [src/harnesskit/](../../src/harnesskit/)
- [templates/](../../templates/)
- [tests/](../../tests/)

验证：

- review：判断变更是否保持在正确边界内。
- runner：相关测试证明行为没有因重构退化。
- runner：`make verify` 覆盖 lint、format、tests、build 和 hook。
