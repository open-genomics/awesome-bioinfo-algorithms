# 贡献指南

感谢你对 Awesome Bioinformatics Algorithms 项目的关注！欢迎各种形式的贡献。

## 添加新算法

1. Fork 本仓库
2. 在 `data/algorithms/` 下找到对应分类的 YAML 文件
3. 按照 `templates/algorithm_template.yaml` 格式追加条目
4. 本地验证通过后提交 Pull Request

```yaml
algorithms:
  - id: algorithm-id          # 唯一标识符（小写字母、数字、连字符）
    name: Algorithm Name      # 算法名称
    description: |            # 算法描述（50-500 字）
      算法的详细描述，包括基本原理、特点和适用场景。
    purpose: 主要用途
    time_complexity: O(n)     # 时间复杂度
    space_complexity: O(n)    # 空间复杂度（可选）
    category: category-id     # 分类 ID
    subcategory: sub-id       # 子分类 ID（可选）
    paper_url: https://...    # 原始论文链接（可选）
    implementation_url: https://...  # 参考实现链接（可选）
    related_tools: [Tool1]    # 相关工具（可选）
    tags: [tag1]              # 标签（可选）
```

## 可用分类

| 分类 ID | 名称 |
|---------|------|
| sequence-alignment | 序列比对 |
| assembly | 序列组装 |
| variant-calling | 变异检测 |
| expression-analysis | 基因表达分析 |
| protein-structure | 蛋白质结构预测 |
| phylogenetics | 系统发育分析 |
| functional-annotation | 功能注释 |
| data-compression | 数据压缩 |
| single-cell | 单细胞基因组学 |
| metagenomics | 宏基因组学 |
| epigenomics | 表观基因组学 |
| gene-prediction | 基因预测 |
| population-genetics | 群体遗传学 |
| spatial-omics | 空间组学 |
| graph-genomics | 图基因组学 |
| protein-language-model | 蛋白质语言模型 |

完整子分类见 `data/categories.yaml`。快速确认分类与已有条目：

```bash
python -m awesome_bioinfo stats
python -m awesome_bioinfo search --category sequence-alignment
```

## 质量要求

- 描述长度 50-500 字
- 必填字段：`id`, `name`, `description`, `purpose`, `time_complexity`, `category`
- 分类/子分类 ID 必须有效，且 `subcategory` 属于对应 `category`
- 算法 ID 全局唯一
- `difficulty`（如填写）为 `beginner` / `intermediate` / `advanced`
- `references[*].type`（如填写）为 `tutorial` / `blog` / `video` / `book` / `documentation` / `slides`

## 本地验证

```bash
# 依赖来自带哈希校验的锁文件；改 pyproject 依赖后须重新生成（见 AGENTS.md）
pip install --require-hashes -r requirements-dev.txt
pip install -e . --no-deps
python -m awesome_bioinfo validate
python -m pytest tests/ -v
# 数据或模板变更后重新生成 README
python -m awesome_bioinfo generate
git diff --exit-code -- README.md
```

`README.md` 由 `templates/readme_template.md` 自动生成，请勿手工编辑。

## 其他贡献方式

- 📝 改进现有算法描述
- 🔗 添加或更新参考链接
- 🐛 报告错误或问题
- 💡 提出新功能建议

## 提交约定

- 提交信息遵循 Conventional Commits
- 单文件小改动可直接提交到默认分支（`master`）
- 非平凡改动走短生命周期分支 `<type>/<description>`，经 PR 合并
