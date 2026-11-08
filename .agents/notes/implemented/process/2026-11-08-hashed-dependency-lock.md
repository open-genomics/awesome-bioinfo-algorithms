# Agent Note: 哈希锁定的依赖清单与 CI 安装

Status: implemented

## Problem

CI 与本地都以 `pip install -e ".[dev]"` 安装依赖：`pyproject.toml` 只有下限约束
（`PyYAML>=6.0`、`aiohttp>=3.9.0`、`pytest>=7.0` …），每次运行解析到的版本都不同，
且没有任何完整性校验。供应链污染或上游发新版即可改变 CI 结果；`ruff` 尤其敏感——
`ruff format` 的输出随版本变化，本地 pre-commit 固定在 v0.9.0，CI 却装最新版，
两者会互相改写代码。

顺带发现三处 CI 实际为红的问题：

1. `ruff format --check` 失败：`awesome_bioinfo/link_checker.py` 与
   `tests/test_export_cmd.py` 已提交的代码未按当前格式书写（v0.9.0 与 v0.17.4
   都要求同样改写）。
2. `test (3.9)` 在 `actions/setup-python` 阶段失败：`ubuntu-latest` 已切到
   Ubuntu 26.04，没有 Python 3.9 构建。
3. Python 3.9 导入即崩：`validate_algorithms_file(..., parsed: dict[str, Any] | None = None)`
   的 PEP 604 注解在 3.9 运行时求值会抛 `TypeError`，而 `requires-python` 声明
   `>=3.9`。

## Decision

- 新增 `requirements-dev.txt`：runtime + dev 的统一锁文件，由
  `uv pip compile pyproject.toml --extra dev --generate-hashes --universal --python-version 3.9`
  生成，包含每个包的 sha256 与按 `python_full_version` / `sys_platform` 的标记，
  3.9–3.12 与三大平台共用一份。
- CI（`ci.yml` 三个 job 与 `data-quality.yml`）改为
  `pip install --require-hashes -r requirements-dev.txt` + `pip install -e . --no-deps`：
  依赖只能来自锁文件，项目本体不再触发依赖解析。
- `ruff` 在 `pyproject.toml` 的 dev extra 里精确固定为 `0.9.0`，与
  `.pre-commit-config.yaml` 的 `ruff-pre-commit` rev 一致；锁文件因此用普通生成命令
  即可复现，不需要额外约束参数。
- `test` job 矩阵改为 `include` 列表：3.9 固定 `ubuntu-22.04`，其余走
  `ubuntu-latest`，并加 `fail-fast: false` 让一个版本失败不掩盖其它版本。
- 修正上述三处红：格式化两个文件、`validate.py` 的注解改回
  `Optional[dict[str, Any]]`。锁文件加入 CI `paths` 触发列表。
- `data-quality.yml` 复用同一份 dev 锁（多装 ruff/pytest 无副作用），只保留一份
  清单，避免 runtime 与 dev 两份锁漂移。

## Alternatives considered

- **`pip-compile` / `pip-tools`**：同样能生成哈希锁，但跨版本标记需要多份文件
  （每个 Python 版本一份）或 `--universal` 的下游工具，uv 一条命令即可。
- **只锁顶层依赖、不锁传递依赖**：`--require-hashes` 要求全部包都有哈希，
  半锁装不上；锁一半等于没锁。
- **单独生成 runtime 锁给 `data-quality.yml`**：多一份文件、多一处漂移源，
  weekly 任务多装几个包的成本可忽略。
- **放弃 Python 3.9 支持**：3.9 已 EOL，但 `requires-python`、classifiers 与
  README 都声明支持，砍版本是产品决定，不在本项范围内；先让 3.9 真的通过。
- **CI 里加"锁文件与 pyproject 同步"校验**：需要额外引入 `setup-uv` action 与
  可执行文件，收益是在 CI 报错而不是本地报错——靠 AGENTS.md 的再生成命令与
  Dependabot pip 更新即可，暂不引入。

## Consequences

- 依赖安装完全可复现，且任何锁文件的改动都会在 review 中显示为版本/哈希变更。
- 改 `pyproject.toml` 依赖后必须重新生成锁文件，否则 CI 装不到新依赖（已写入
  AGENTS.md「依赖锁」一节）。
- `ruff` 升级需要同时改 `pyproject.toml` 与 `.pre-commit-config.yaml`，两处不一致
  时 CI 的 format 检查会直接失败——这是有意的 fail-closed。
- 锁文件约 1900 行，含全部平台 wheel 哈希；review 时只看顶层版本变化即可，但
  diff 体积较大。
- Dependabot 的 pip 生态会尝试更新 `requirements-dev.txt`，与 `pyproject.toml`
  的更新行为需要在后续 PR 中确认。

## Verification

四个 Python 版本的干净虚拟环境（`uv venv` + `pip install --require-hashes` +
`pip install -e . --no-deps`）：

- 3.9 / 3.10 / 3.11 / 3.12：`pytest tests/ -q` 各 246 passed。
- `ruff check awesome_bioinfo tests` 与 `ruff format --check awesome_bioinfo tests`
  在 3.9 / 3.11 / 3.12 环境通过（锁定版本 0.9.0，27 个文件已格式化）。
- `python -m awesome_bioinfo generate` 后 `git diff --exit-code -- README.md`
  无漂移（README 由模板变动同步更新）。
