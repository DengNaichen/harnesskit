# RULE-PRODUCT-001

## Rule

用户可见文案和生成资产必须明确区分已支持能力、待确认占位和未来愿景。

## Details

本规则保护产品真实性。产品判断参考 [docs/practices/PRODUCT_SENSE.md](../../docs/practices/PRODUCT_SENSE.md)，但只有“不能把未实现能力写成已支持”属于硬约束。HarnessKit 的 README、CLI 输出、模板、facts、rules、report 和设计文档都可能被 agent 当成事实来源，因此必须保持清楚的状态边界。

违反形态：

- 把路线图、设计愿景、coming soon 或占位能力写成当前已支持。
- 在模板中把示例命令、目录或集成当成目标仓库事实。
- 用模糊文案隐藏未配置状态，而不是保留 `NEEDS CLARIFICATION`、未配置或待确认。

证据：

- [docs/practices/PRODUCT_SENSE.md](../../docs/practices/PRODUCT_SENSE.md)
- [README.md](../../README.md)
- [docs/design/](../../docs/design/)
- [templates/](../../templates/)
- [src/harnesskit/cli.py](../../src/harnesskit/cli.py)

验证：

- harness lint 和 Markdown link checks 可发现部分漂移。
- review：核对文案、模板和 docs 是否把愿景误写成当前事实。
- runner：模板行为变化按 `tests/test_init.py` 覆盖。
