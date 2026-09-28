# CLAUDE.md

> AI 助手项目上下文。详细模块说明见 [`awesome_bioinfo/CLAUDE.md`](awesome_bioinfo/CLAUDE.md)。

## 项目定位

精选生物信息学算法的 awesome-list：结构化 YAML 数据 + Python CLI 维护工具 + 自动生成的中文 README。
定位为轻量、业余维护项目，避免过度工程化。

## 架构

```
data/
  categories.yaml          # 16 个顶级分类定义
  algorithms/*.yaml        # 每类一个文件，顶级键 algorithms:

awesome_bioinfo/           # 核心 Python 包
  schema.py                # 数据类: Category, AlgorithmEntry, Reference
  algorithm_registry.py    # 加载、索引、搜索
  category_manager.py      # 分类层级查询
  validate.py              # 字段规则 + JSON Schema 双重验证
  data_io.py               # YAML/JSON/CSV 读写
  data_store.py            # 数据存储
  readme_generator.py      # 生成 README.md（从模板）
  link_checker.py          # 异步检查 URL
  __main__.py              # CLI 入口（python -m awesome_bioinfo）

templates/
  algorithm_template.yaml  # 新条目模板
  readme_template.md       # README 模板

schemas/
  algorithm-schema.json    # JSON Schema（validate 命令使用）
```

## 生成输出（禁止手动编辑）

| 文件 | 生成命令 |
|------|----------|
| `README.md` | `python -m awesome_bioinfo generate` |

数据或模板变更后须重新生成并验证无漂移：

```bash
python -m awesome_bioinfo generate
git diff --exit-code -- README.md
```

README 仅维护中文版本，由模板自动生成。

## 常用命令

```bash
# 验证与统计
python -m awesome_bioinfo validate          # 数据 PR 必须通过
python -m awesome_bioinfo stats

# 查询
python -m awesome_bioinfo search <query>
python -m awesome_bioinfo info <id>
python -m awesome_bioinfo compare <id1> <id2>
python -m awesome_bioinfo export --format json

# 生成
python -m awesome_bioinfo generate

# Lint / 测试
ruff check awesome_bioinfo tests && ruff format --check awesome_bioinfo tests
pytest tests/ -v --tb=short
```

## 算法条目规则

- **必填**：`id`, `name`, `description`, `purpose`, `time_complexity`, `category`
- `description`：50-500 字符（trimmed）
- `id`：全局唯一，小写字母 + 连字符（如 `smith-waterman`）
- `tags`：小写字母 + 连字符
- `category` / `subcategory`：必须存在于 `data/categories.yaml`
- `difficulty`：`beginner` | `intermediate` | `advanced`
- `time_complexity` / `space_complexity`：须匹配 `O(...)` 模式
- 模板：`templates/algorithm_template.yaml`

### 添加新算法

1. 复制模板：`templates/algorithm_template.yaml`
2. 追加到 `data/algorithms/<category>.yaml`
3. 填写字段，确保描述长度 50-500 字符
4. `python -m awesome_bioinfo validate`
5. `python -m awesome_bioinfo generate` 并确认 `git diff --exit-code -- README.md`

## 命名与代码约定

- 算法/分类 ID：lowercase-hyphenated
- Python 模块：snake_case；数据类：PascalCase
- 行宽 100（Ruff）；规则集 E, F, W, I, N, UP, B, C4
- YAML 文件 UTF-8 编码

## 常见陷阱

- 不要手工编辑 `README.md`（生成文件）
- `data/categories.yaml` 变更后，所有引用该分类的算法文件都需同步更新

## 项目统计

统计数字随数据变更而变化，本文件不硬编码，以唯一权威出处为准：

- 版本：`pyproject.toml` 的 `version`
- 算法 / 分类 / 标签数量：`python -m awesome_bioinfo stats` 的实时输出
- README 中的统计徽章与分类总览表由 `python -m awesome_bioinfo generate` 自动同步
