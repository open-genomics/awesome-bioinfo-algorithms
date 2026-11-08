# awesome_bioinfo 包

> [← 项目根](../CLAUDE.md)

## 包边界

- **是**：数据模型、加载/索引/搜索、字段验证、README 生成、CLI
- **不是**：Web 服务、算法实现（仅收录元数据）

## 模块速查

| 模块 | 职责 |
|------|------|
| `schema.py` | 数据类 `Category`, `AlgorithmEntry`, `Reference`；常量 `VALID_DIFFICULTIES`, `VALID_REFERENCE_TYPES` |
| `algorithm_registry.py` | 加载所有 YAML、按 category/tag/subcategory/id 索引、全文搜索 |
| `category_manager.py` | 分类层级加载与查询；`category_exists()` 用于验证 |
| `validate.py` | 字段规则验证；重复 ID 检测 |
| `data_io.py` | YAML 读写、JSON/CSV 导出 |
| `data_store.py` | 数据存储 |
| `readme_generator.py` | 从 `templates/readme_template.md` 生成 `README.md` |
| `__main__.py` | CLI 入口（包含所有子命令实现） |
| `link_checker.py` | 异步检查算法条目中的 URL |

## 关键不变量

- `AlgorithmEntry.id` 全局唯一，lowercase-hyphenated
- `description` 长度 50-500 字符（trimmed）；`validate` 会强制检查
- `category` 必须存在于 `CategoryManager` 加载的分类表中
- `subcategory` 若填写，必须属于对应 `category` 的子分类
- `time_complexity` / `space_complexity` 须匹配 `O(...)` 模式
- YAML 文件顶级键为 `algorithms:`（列表）

## 测试重点

`tests/` 中高优先级覆盖区域：

- `test_validate.py` - 边界值（description 长度、O(...) 格式、重复 ID）
- `test_algorithm_registry.py` - 索引一致性、搜索结果正确性
- `test_data_completeness.py` - 所有现有 YAML 文件通过 validate
- `test_cli.py` - 各子命令的集成路径

运行：`pytest tests/ -v --tb=short`（`pyproject.toml` 已设置默认参数）
