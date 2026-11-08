# Agent Note: 验证器对非映射输入按错误报告

Status: implemented

## Problem

`Validator` 的 YAML 校验路径默认根节点与列表条目都是映射，遇到其它类型时直接抛出异常而不是返回 `ValidationResult`：

- 算法文件根节点为标量（如 `42`）时，`"algorithms" not in data` 抛 `TypeError`；
- 条目不是映射时，`Validator.validate_algorithm` 的 `data.get(...)`、`validate_algorithms_file` 的 `algo.get(...)`、`validate_categories_file` 的 `cat.get(...)` 抛 `AttributeError`；
- `validate_all` 在重复 ID 扫描阶段对非映射根节点调用 `data.get("algorithms")` 抛 `AttributeError`。

结果是 `python -m awesome_bioinfo validate` 在数据文件被误写成顶层列表/标量时崩溃，而不是给出可操作的错误信息。

## Decision

在字段校验与文件校验两层都显式检查映射类型，把非映射输入转成 `ValidationResult` 错误：

- `FieldValidator.validate_algorithm_fields` / `validate_category_fields` 入口检查 `isinstance(data, dict)`，非映射返回 "must be a mapping" 错误；
- `Validator.validate_algorithm` 在调用父类后对非映射提前返回，避免继续访问 `data.get`；
- `validate_algorithms_file` / `validate_categories_file` 检查 YAML 根节点，条目循环内逐个检查并跳过非映射项（错误信息带序号）；
- `validate_all` 的重复 ID 扫描增加根节点与条目类型检查；
- `_collect_category_relationships` 跳过非映射分类项。

`validate_yaml_file` 保持只负责解析与空文档检查，根节点类型由调用方按文件语义报告。

## Alternatives considered

- **只在文件校验层加检查，字段校验器保持原契约。** 最强论据：改动面更小，`FieldValidator` 的签名本来就声明 `dict`。否：直接调用 `validate_algorithm` / `validate_category` 的入口同样会崩溃，且 `validate_algorithms_file` 的条目循环仍要先调用它们，文件层无法完全兜底。

- **把非映射输入当作「缺字段」继续走完整字段校验。** 最强论据：复用现有错误路径，不新增错误文案。否：非映射对象没有字段语义，逐字段报错会产生大量噪声，且部分分支仍会按索引/迭代方式访问而抛异常。

## Consequences

收益：`validate` 对畸形 YAML（顶层列表/标量、列表里混入字符串或数字）给出确定性的错误列表，不再崩溃；`validate_all` 能继续汇总同一目录下其它文件的错误。

代价：字段校验器新增一层类型判断；错误信息新增 "entry must be a mapping" 与 "Root of ... file must be a mapping" 文案，若有下游按字符串匹配错误需同步。

## Verification

```bash
cd awesome-bioinfo-algorithms
python -m awesome_bioinfo validate
ruff check awesome_bioinfo tests
pytest tests/test_validate.py -k non_mapping -v
pytest tests/ -v --tb=short
```
