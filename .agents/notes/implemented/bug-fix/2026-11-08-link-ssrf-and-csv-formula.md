# Agent Note: 链接检查 SSRF 防护、CSV 公式注入与 null 列表字段

Status: implemented

## Problem

- `check_url` 对数据文件中的 URL 直接 `HEAD/GET` 并自动跟随重定向；YAML 数据可指向
  `127.0.0.1`、内网或云元数据地址，形成 SSRF。
- CSV 导出未中和 `= + - @` 等公式前缀，电子表格打开时可执行公式（CWE-1236）。
- `language` / `references` 显式为 `null` 时校验以 truthiness 跳过，随后
  `AlgorithmEntry.from_dict` 迭代 `None` 抛 `TypeError`。

## Decision

- 新增 `is_safe_url`：解析主机名并拒绝 loopback/private/link-local/multicast/reserved
  地址；DNS 解析失败放行（无法连接，交给请求报错）。`check_url` 关闭自动重定向，
  逐跳校验 `Location`，最多 5 跳。
- CSV 导出统一经过 `_csv_safe`，对字符串单元格的公式前缀加 `'`。
- 校验把 `null` 视为类型错误；`AlgorithmEntry.from_dict` 对四个列表字段统一 `or []`
  归一化，保证不经过 validate 的读取路径（stats/search/export）也不会崩溃。

## Verification

- `pytest tests/test_link_checker.py tests/test_export_cmd.py tests/test_validate.py -q`：
  112 passed。
- `pytest tests/ -q`：245 passed。
- `python -m awesome_bioinfo generate && git diff --exit-code -- README.md`：无差异。
