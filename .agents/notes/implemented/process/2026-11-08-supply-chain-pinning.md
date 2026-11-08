# Agent Note: 固定 Actions 与 pre-commit 版本

Status: implemented

## Problem

工作流中的第三方 Action（checkout / setup-python / github-script）与
`.pre-commit-config.yaml` 的两个 hook 都使用可移动的 tag 或主版本号。
tag 被重指或上游仓库被接管时，CI 与本地 hook 会执行未审计的代码；
Dependabot 配置此前被删除，版本变化也不会进入 review。

## Decision

- `.github/workflows` 中所有 `uses:` 固定到 40 位 commit SHA，并保留
  `# vX` 注释说明对应版本。
- `.pre-commit-config.yaml` 的 `rev` 同样改为 SHA + 版本注释。
- 恢复 `.github/dependabot.yml`，配置 github-actions 与 pip 两条每周
  更新，只创建 PR、不自动合并。

## Verification

- `grep -rn "uses:" .github/workflows` 结果全部以 40 位 SHA 结尾；
- `grep -n "rev:" .pre-commit-config.yaml` 两条均为 SHA；
- YAML 语法由 GitHub Actions / pre-commit 解析验证（本次未推送触发 CI）。

## Alternatives considered

- **保留可移动 tag + Dependabot**：Dependabot 只能提示新版本，无法阻止
  tag 被重指后立即执行；SHA 固定才有供应链保证。
- **同时给 pip 依赖加 hash 锁（`pip install --require-hashes`）**：需要
  生成并维护 requirements 锁文件，超出本次改动范围，留作后续。

## Consequences

- 依赖更新改为由 Dependabot PR 驱动；手动升级需要重新解析 SHA。
- pip 安装仍未做 hash 固定，属于已知剩余项。
