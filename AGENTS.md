# AGENTS.md

AI 助手工作指引。详细架构与模块说明见 [`CLAUDE.md`](CLAUDE.md)。

## 项目

精选生物信息学算法 awesome-list：YAML 数据 + Python CLI（`awesome_bioinfo` 包）+ 自动生成的中文 README。轻量、业余维护。

## 核心规则

- `README.md` 由 `python -m awesome_bioinfo generate` 从 `templates/readme_template.md` 生成，**禁止手工编辑**。
- 改 `data/` 或 `templates/` 后必须重新生成并确认无漂移：`python -m awesome_bioinfo generate && git diff --exit-code -- README.md`。
- 数据真相源在 `data/algorithms/*.yaml` 与 `data/categories.yaml`。

## 常用命令

```bash
python -m awesome_bioinfo validate          # 数据变更前必过
python -m awesome_bioinfo stats
python -m awesome_bioinfo search <query>
python -m awesome_bioinfo info <id>
python -m awesome_bioinfo compare <id1> <id2>
python -m awesome_bioinfo export --format json
python -m awesome_bioinfo generate          # 生成 README.md
python -m awesome_bioinfo check-links       # 检查条目 URL 有效性

ruff check awesome_bioinfo tests
pytest tests/ -v --tb=short
```

## 算法条目

- 必填：`id`（lowercase-hyphenated，全局唯一）、`name`、`description`（50-500 字）、`purpose`、`time_complexity`（`O(...)`）、`category`
- `category`/`subcategory` 必须存在于 `data/categories.yaml`
- 模板：`templates/algorithm_template.yaml`

## 决策笔记

非平凡改动（行为、架构、跨文件契约、流程/工具链、文档约定等维护者日后可能重访的决定）须写决策笔记到 `.agents/notes/`；纯机械改动（错别字、格式化、死链修复、无歧义重命名）直接改，不写笔记。

- 路径即分类：`.agents/notes/<lifecycle>/<class>/yyyy-mm-dd-topic.md`，lifecycle ∈ `proposed` / `implemented` / `rejected`，class ∈ `feature` / `bug-fix` / `simplification` / `architecture` / `process` / `testing`；只建用到的目录
- 格式：前三行 `# Agent Note: <标题>` + 空行 + `Status: implemented`；正文骨架 `## Problem` → `## Decision`（现在时）→ `## Alternatives considered`（只记真实考虑过的备选）→ `## Consequences`（代价与收益）→ `## Verification`（具体命令）
- 动手前先检索历史决策：`rg --hidden --glob '!.agents/notes/archived/**' "<关键词>" .agents/notes/`

## 依赖锁

`requirements-dev.txt` 是 runtime + dev 的**唯一**依赖真相源：CI 与本地都用
`pip install --require-hashes -r requirements-dev.txt && pip install -e . --no-deps`
安装，pip 不会重新解析 `pyproject.toml`。

```bash
uv pip compile pyproject.toml --extra dev --generate-hashes --universal \
  --python-version 3.9 -o requirements-dev.txt
```

- `--universal --python-version 3.9` 生成带 `python_full_version` 标记的跨版本、
  跨平台锁，CI 的 3.9–3.12 矩阵共用一份。
- 改 `pyproject.toml` 依赖后必须重新生成并提交锁文件，否则 CI 装不到新依赖。
- `ruff` 在 `pyproject.toml` 里精确固定，且必须与 `.pre-commit-config.yaml` 的
  `ruff-pre-commit` rev 一致：`ruff format` 输出随版本变化，两者不同版本会互相改写。
