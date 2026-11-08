# Agent Note: 分类表加载状态与被引用校验

Status: implemented

## Problem

`Validator` 与 `CategoryManager` 用集合真值判断「分类表是否已加载」：

- `Validator.validate_algorithm` 的 `if self.valid_categories` 与 `if self.category_parents` 把「已加载但为空」当作「未加载」，`categories: []` 时跳过 category/subcategory 校验。
- `CategoryManager.validate_category_reference` 同样在 `valid_categories` 为空时放行任意 category。
- `CategoryManager.load_categories` 在 YAML 缺少 `categories` 键或文档为空时提前 `return []`，早于清空旧状态，导致上一次加载的分类泄漏。

结果是 `validate` 对空分类表 + 未知 category 的数据误报合法；`README` 生成时统计仍有算法但列表为空，自相矛盾。

## Decision

显式记录加载状态，替代集合真值判断：

- `Validator` 新增 `_categories_loaded`：构造函数显式传入 `valid_categories` 时视为已加载；`validate_categories_file` 成功解析出 `categories` 列表后置 True；`validate_all` 开始时置 False。
- `validate_algorithm` 仅在已加载时校验 category/subcategory，空集合也拒绝未知引用；未加载时保持只做字段校验（`test_property_10_valid_data_passes` 等依赖）。
- `CategoryManager` 新增 `_loaded`：`load_categories` / `from_categories` 置 True，`validate_category_reference` 在已加载时即使集合为空也拒绝未知 category。
- `load_categories` 把状态重置移到缺少 `categories` 键的早退分支之前，任何成功解析的 YAML 都替换而非叠加旧状态。
- 补回归测试覆盖空分类表、未加载直调、缺键/空文档重置三种路径。

## Alternatives considered

- **保留真值判断，只把空列表当作特殊情况。** 最强论据：改动最少。否：真值判断无法区分「未加载」与「加载为空」，这正是缺陷根因；加标记后两种语义各自明确。
- **构造 `Validator` 时不再接受 `valid_categories` 参数。** 最强论据：状态来源只剩文件加载，更简单。否：`tests/test_validate.py` 与下游直接构造的用法依赖该参数，属于不必要的破坏性变更。

## Consequences

收益：空分类表不再静默放行未知引用；`validate` 能对空数据目录给出可操作错误；`CategoryManager` 在文件缺键/为空时不再泄漏旧状态。

代价：`README` 生成命令现在会在空分类表下失败（这符合数据完整性预期）；额外维护两个私有布尔标记，未来新增加载入口需同步置位。

## Verification

```bash
cd awesome-bioinfo-algorithms
python -m awesome_bioinfo validate
ruff check awesome_bioinfo tests
ruff format --check awesome_bioinfo tests
pytest tests/ -v --tb=short
```
