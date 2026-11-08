# Agent Note: 修复周检死链告警被 continue-on-error 吞掉

Status: implemented

## Problem

`.github/workflows/data-quality.yml` 的周检链路存在两处缺陷，导致「发现死链」永远不会产生任何告警：

1. `Check URL validity` 步骤设置了 `continue-on-error: true`。`check-links` 在存在错误时返回 1（`awesome_bioinfo/link_checker.py`），但 `continue-on-error` 会把该步骤的 conclusion 变为 success、job 不失败，后续 `if: failure()` 的 `Create Issue on Failure` 步骤永不执行，工作流整体显示绿色。
2. 工作流级 `permissions` 只声明了 `contents: read`，未声明的 scope 均为 none；`github-script` 调用 `issues.create` 需要 `issues: write`，即使触发也会 403。

## Decision

- 删除 `Check URL validity` 的 `continue-on-error: true`，让死链使 job 失败并触发告警步骤。
- 在 `permissions` 增加 `issues: write`，使 issue 创建可用；其余权限保持最小（`contents: read`）。
- 周检触发方式（每周日 cron 与 `workflow_dispatch`）不变，仅恢复「失败→告警」的原有意图。

## Alternatives considered

- **保留 `continue-on-error`，把告警条件改为 `steps.<id>.outcome == 'failure'`。** 最强论据：死链不阻断 job，仅创建 issue，保留「周检非阻塞」语义。否：工作流整体仍为绿色，与「失败要能真正告警」的目标相悖，且需新增 step id 并改变步骤状态语义，改动面更大。
- **把 `issues: write` 放在 job 级 `permissions`。** 最强论据：权限只授予需要的 job。否：本工作流只有一个 job，放在工作流级同样最小且 diff 更小。

## Consequences

收益：死链检测失败时工作流变红并自动创建 issue，周检恢复实际告警能力。

代价：死链会让周检运行标记为失败（这是预期行为）；`issues: write` 仅授予该工作流的 `GITHUB_TOKEN`，不涉及其他工作流。

## Verification

```bash
python3 -c "import yaml; d=yaml.safe_load(open('.github/workflows/data-quality.yml')); assert d['permissions']['issues']=='write'; assert 'continue-on-error' not in open('.github/workflows/data-quality.yml').read()"
```

未运行全量 CI（工作流只能在 GitHub 上执行）；`check-links` 的退出码语义已通过阅读 `awesome_bioinfo/link_checker.py` 确认。
