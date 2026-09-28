# Agent Note: 文档审计：仓库 URL 规范化与统计单源化

Status: implemented

## Problem

对文档做准确性审计（对照 `pyproject.toml`、`awesome_bioinfo/` 与 `data/`）发现六处问题：

1. 仓库已转移到 `open-genomics` 组织（git remote 为 `open-genomics/awesome-bioinfo-algorithms`，访问 `github.com/LessUp/awesome-bioinfo-algorithms` 会被 GitHub 重定向到新地址），但 `templates/readme_template.md` 生成的 README 中 CI 徽章、clone 地址、bibtex `url`、页脚链接全部指向 `LessUp`；旧组织主页 `github.com/LessUp` 已 404，`LessUp` 只剩仓库级重定向，随时可能失效。
2. README 引用徽章指向 `blob/main/CITATION.cff`，而默认分支是 `master`（`origin/HEAD -> origin/master`），该徽章图片 404。
3. issue 模板 `contact_links` 指向已下线的文档站 `lessup.github.io`（实测 404），并把贡献者引到 `LessUp` 仓库与不存在的 `main` 分支。
4. `CLAUDE.md` 项目统计硬编码「195 条目 / 392 标签」，与数据实际值（`python -m awesome_bioinfo stats`：186 条 / 382 标签 / 16 分类）漂移；该节没有任何机制保持同步。
5. 模板中 `## 📑 目录` 标题没有显式锚点，而每个分类节的「↑ 返回顶部」都链到 `#目录`；GitHub 对带 emoji 的标题生成的 slug 是 `#-目录`（emoji 被剥离成前导连字符），这 16 处返回顶部链接在 GitHub 上全部失效。
6. `data/algorithms/single-cell.yaml` 中 `kallisto | bustools` 名字含竖线，生成 README 后该表格行被拆成两列，渲染错位（全库仅此一条名字含 `|`）。

## Decision

- 文档表面的仓库定位信息（URL 与社区署名）统一指向 `open-genomics/awesome-bioinfo-algorithms` 与 `master` 分支：修改 `templates/readme_template.md`（CI 徽章、引用徽章、clone 地址、bibtex `url`、bibtex `author`、页脚）与 `.github/ISSUE_TEMPLATE/config.yml`，并重新生成 `README.md`。
- `CLAUDE.md` 不再硬编码统计数字：版本指向 `pyproject.toml` 的 `version`，数量指向 `python -m awesome_bioinfo stats`，README 统计由 `generate` 自动同步——README 是统计的唯一展示处。
- `## 📑 目录` 标题在模板中补显式 `<a id="目录"></a>` 锚点（与生成器给分类节加 `<a id="…"></a>` 的既有做法一致），不改 `readme_generator.py`。
- `kallisto | bustools` 改名为 `kallisto + bustools`：这是数据文件而非文档，超出本次文档任务字面范围，但不改它则主文档 README 的破表无法修复（表格修复正确位置在生成器里做转义，但本任务禁止改代码）；改动仅为显示名，不影响 id、验证规则与任何字段语义。

## Alternatives considered

- **保留 `LessUp` URL，依赖 GitHub 转移重定向。** 最强论据：零改动，仓库级重定向今天仍然有效，且若上游计划恢复旧名可少一轮 churn。否：`github.com/LessUp` 组织页已 404（组织消失而非改名，改名会重定向组织页），重定向只剩一层且随时可能因旧路径重建仓库而断裂；`blob/main/` 径直 404，引用徽章已经坏了——「还能用」不成立于已坏的部分。
- **`CLAUDE.md` 仅就地改正数字（195→186、392→382）。** 最强论据：改动最小、diff 一目了然。否：该节是纯手工副本，没有 CI 门禁（CI 只校验 README 漂移），下次数据变更必然再度漂移；单源化到 `stats` 命令才断根，README 本来就是统计的自动同步展示处。
- **数据中写成 `kallisto \| bustools` 保留官方竖线品牌名。** 最强论据：`kallisto|bustools` 是官方写法，转义后 README 表格能正确渲染「kallisto | bustools」。否：转义符会原样泄漏到所有非 Markdown 场景——`info`/`compare` 终端输出、CSV/JSON 导出都显示 `\|`；治本方案是在 `readme_generator.py` 生成表格时统一转义竖线，但本任务禁止改代码，故选对全场景都干净的 `+`。
- **同时修正 `CITATION.cff` 与 `pyproject.toml` 中的 LessUp 署名和 URL。** 最强论据：一次把引用面全部统一，避免 README（新 URL）与 CITATION.cff（旧 URL）短期不一致。否：两者是包元数据/引用元数据，不在本次文档任务的修改范围（只许动 README/CONTRIBUTING/面向人的 .md/templates）；作为后续项于 2026-09-28 完成（连同 `__init__.py`、`link_checker.py`、`test_owner_metadata.py` 一并切换）。

## Consequences

收益：README 徽章、clone 地址、引用链接指向真实仓库与存在的分支；issue 模板不再导流到 404 文档站；16 处「返回顶部」在 GitHub 上恢复可用；CLAUDE.md 统计不再腐烂；kallisto 行表格恢复正常渲染。

代价：`kallisto + bustools` 与官方 `kallisto|bustools` 品牌写法略有出入；`<a id="目录"></a>` 是手工锚点，改「📑 目录」标题时需同步；`config.yml` 删除了文档站入口，若将来重建文档站需自行加回。

后续（2026-09-28）统一收尾：`CITATION.cff`/`pyproject.toml` 的署名与 URL、`awesome_bioinfo/__init__.py` 的 `__author__`、`link_checker.py` 的 User-Agent 与 `tests/test_owner_metadata.py` 的期望值全部切到 open-genomics，README 署名与引用元数据不再分叉；`readme_generator.py` 补 `_escape_cell` 对表格数据单元格统一转义竖线（当时「治本方案在生成器」的判据落地，防御未来含 `|` 的新条目破表），数据侧保留 `+` 写法不变。

## Verification

```bash
cd awesome-bioinfo-algorithms
python -m awesome_bioinfo validate                                  # ✅ All data files are valid!
python -m awesome_bioinfo generate && git diff --exit-code -- README.md   # 先 generate 再重跑应无二次漂移
python -m awesome_bioinfo generate --output /tmp/check.md && diff /tmp/check.md README.md  # 生成稳定
rg -n "LessUp|blob/main|lessup\.github\.io" README.md templates/ .github/ pyproject.toml CITATION.cff awesome_bioinfo/ tests/  # 应无输出（笔记正文除外）
rg -n "open-genomics" templates/readme_template.md                  # 5 处 URL/署名
rg -n "195|392" CLAUDE.md                                           # 应无输出
python3 -m pytest tests/test_owner_metadata.py                      # 4 passed（署名/URL 元数据门禁）
npx tsx <skill>/scripts/verify-agent-note-tree.ts && npx tsx <skill>/scripts/verify-agent-note-format.ts
```
