<h1 align="center">Awesome Bioinformatics Algorithms</h1>

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://github.com/open-genomics/awesome-bioinfo-algorithms/actions/workflows/ci.yml"><img src="https://github.com/open-genomics/awesome-bioinfo-algorithms/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="http://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg" alt="License"></a>
  <a href="https://github.com/open-genomics/awesome-bioinfo-algorithms/blob/master/CITATION.cff"><img src="https://img.shields.io/badge/Cite%20Me-APA-blue" alt="Citation"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Algorithms-{{ total_algorithms }}-blue.svg" alt="Algorithms">
  <img src="https://img.shields.io/badge/Categories-{{ total_categories }}-green.svg" alt="Categories">
  <img src="https://img.shields.io/badge/Tags-{{ total_tags }}-orange.svg" alt="Tags">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python" alt="Python">
</p>

<p align="center">
  <b>🧬 精选生物信息学算法合集，附时间/空间复杂度分析</b>
</p>

<p align="center">
  <a href="CONTRIBUTING.md">🤝 贡献指南</a> • 
  <a href="#citation">📚 引用</a>
</p>

---

## ✨ 亮点

<table>
<tr>
<td width="50%">

**🎯 面向研究者**
- {{ total_algorithms }}+ 精选算法
- 时间/空间复杂度分析
- 论文与实现链接
- 分类标签体系

</td>
<td width="50%">

**💻 面向开发者**
- CLI 数据管理工具
- 自动校验与生成
- 结构化 YAML 数据
- 完整测试覆盖

</td>
</tr>
</table>

---

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/open-genomics/awesome-bioinfo-algorithms.git
cd awesome-bioinfo-algorithms

# 安装依赖
pip install -e ".[dev]"

# 校验数据
python -m awesome_bioinfo validate

# 查看统计
python -m awesome_bioinfo stats
```

---

## 📊 统计摘要

| 指标 | 数值 |
|:-------|------:|
| 算法总数 | **{{ total_algorithms }}** |
| 分类数量 | **{{ total_categories }}** |
| 标签数量 | **{{ total_tags }}** |

---

## 📑 目录 <a id="目录"></a>

{{ toc }}

---

{{ category_overview }}

---

{{ featured_content }}

---

## 🛠️ CLI 命令

```bash
# 搜索算法
python -m awesome_bioinfo search "alignment"

# 查看算法详情
python -m awesome_bioinfo info smith-waterman

# 对比两个算法
python -m awesome_bioinfo compare smith-waterman needleman-wunsch

# 导出数据为 JSON
python -m awesome_bioinfo export --format json > algorithms.json

# 生成 README
python -m awesome_bioinfo generate
```

---

## 📚 资源

### 学习平台
- [Rosalind](http://rosalind.info/) — 生物信息学算法练习
- [NCBI](https://www.ncbi.nlm.nih.gov/) — 美国国家生物技术信息中心
- [EBI](https://www.ebi.ac.uk/) — 欧洲生物信息学研究所

### 工具与社区
- [Bioconductor](https://www.bioconductor.org/) — R 生物信息学工具集
- [Galaxy](https://usegalaxy.org/) — 开放分析平台
- [BioStars](https://www.biostars.org/) — 生物信息学问答社区
- [scverse](https://scverse.org/) — 单细胞 Python 生态

---

## 🤝 贡献

欢迎贡献！详见[贡献指南](CONTRIBUTING.md)。

### 贡献方式

- 🆕 **添加新算法**
- 📝 **改进描述**
- 🔗 **补充参考文献**
- 🐛 **报告与修复问题**
- 📚 **完善文档**

---

## 📚 引用 <a id="citation"></a>

如在研究中使用了本项目，可引用为：

```bibtex
@software{awesome_bioinfo_algorithms,
  title = {Awesome Bioinformatics Algorithms},
  author = {{open-genomics Community}},
  year = {2025},
  url = {https://github.com/open-genomics/awesome-bioinfo-algorithms}
}
```

更多引用格式见 [CITATION.cff](CITATION.cff)。

---

## 📄 许可证

<p align="center">
  <a href="https://creativecommons.org/publicdomain/zero/1.0/">
    <img src="https://licensebuttons.net/p/zero/1.0/88x31.png" alt="CC0">
  </a>
</p>

本项目采用 [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)（公有领域）许可。

您可以自由地：
- ✅ 复制、修改、分发
- ✅ 用于商业用途
- ✅ 无需署名

---

<p align="center">
  <b>Made with ❤️ by the community</b><br>
  © 2025-2026 <a href="https://github.com/open-genomics">open-genomics</a> Community
</p>
