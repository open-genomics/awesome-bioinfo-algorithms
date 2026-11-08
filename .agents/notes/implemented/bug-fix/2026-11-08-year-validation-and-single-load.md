# Agent Note: year 必须为整数，validate_all 只解析一次 YAML

Status: implemented

## Problem

1. `FieldValidator` 对非整数 `year` 只给 warning，空字符串/`null` 直接跳过。
   但 `generate` 的年份排序按 `year` 比较，字符串与整数混排会抛
   `TypeError`，校验阶段却显示通过。
2. `validate_all` 先调用 `validate_algorithms_file()`，内部已经
   `open + safe_load` 一次；随后又重新 `validate_yaml_file()` 读同一文件，
   只为拿 `algorithms` 列表做跨文件重复 ID 检查。每个 YAML 被解析两次。

## Decision

- `year` 不是 `int`（含空字符串、`null`、`bool`）时直接报 error；
  缺失仍按 0 处理。越界年份保持 warning。
- `validate_algorithms_file(file_path, parsed=None)` 增加可选输出参数，
  成功解析时把内容写入调用方提供的 dict；`validate_all` 复用该结果做重复
  ID 扫描，不再二次读盘。默认参数保持原有调用方式不变。

## Verification

- 新增/更新 `test_validate.py`：非整数 year、空字符串 year 均判错；
  `validate_algorithms_file` 的既有测试保持不变。
- `uv run --with pytest --with hypothesis pytest tests/ -q`：246 passed。
- `python -m awesome_bioinfo generate` 后 `README.md` 无 diff。

## Alternatives considered

- **在 generate 里把 year 强制转 int**：会把脏数据静默转成 0 或抛异常，
  错误发现点离数据更远；校验层拒绝更直接。
- **为 validate_algorithms_file 增加返回值元组**：会破坏现有测试与调用方
  的返回类型；可选输出参数改动面最小。

## Consequences

- 现有 246 项测试全部通过；含非整数 year 的数据文件现在会被
  `validate` 拒绝，需要修正数据。
- 每个算法 YAML 的解析次数从 2 次降为 1 次。
