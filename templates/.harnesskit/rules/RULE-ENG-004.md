# RULE-ENG-004

## Rule

不要把没有仓库配置或 runner 证据的检查写成完成条件。

## Details

agent 只能要求真实存在的检查。未配置的 lint、format、typecheck、coverage、docs build、CI、branch protection 或平台 gate 可以记录为待确认或未配置，但不能写成完成门槛。

## Evidence

- [NEEDS CLARIFICATION: 工具配置、脚本、CI、facts 或未配置证据]

## Guard

- [NEEDS CLARIFICATION: verification drift check、review 或 harness lint]
