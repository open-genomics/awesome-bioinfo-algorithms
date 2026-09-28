<h1 align="center">Awesome Bioinformatics Algorithms</h1>

<p align="center">
  <a href="https://awesome.re"><img src="https://awesome.re/badge.svg" alt="Awesome"></a>
  <a href="https://github.com/open-genomics/awesome-bioinfo-algorithms/actions/workflows/ci.yml"><img src="https://github.com/open-genomics/awesome-bioinfo-algorithms/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="http://creativecommons.org/publicdomain/zero/1.0/"><img src="https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg" alt="License"></a>
  <a href="https://github.com/open-genomics/awesome-bioinfo-algorithms/blob/master/CITATION.cff"><img src="https://img.shields.io/badge/Cite%20Me-APA-blue" alt="Citation"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Algorithms-186-blue.svg" alt="Algorithms">
  <img src="https://img.shields.io/badge/Categories-16-green.svg" alt="Categories">
  <img src="https://img.shields.io/badge/Tags-382-orange.svg" alt="Tags">
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
- 186+ 精选算法
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
| 算法总数 | **186** |
| 分类数量 | **16** |
| 标签数量 | **382** |

---

## 📑 目录 <a id="目录"></a>

<details>
<summary>点击展开</summary>

- [序列比对](#序列比对)
- [序列组装](#序列组装)
- [变异检测](#变异检测)
- [基因表达分析](#基因表达分析)
- [蛋白质结构预测](#蛋白质结构预测)
- [系统发育分析](#系统发育分析)
- [功能注释](#功能注释)
- [数据压缩](#数据压缩)
- [单细胞基因组学](#单细胞基因组学)
- [宏基因组学](#宏基因组学)
- [表观基因组学](#表观基因组学)
- [基因预测](#基因预测)
- [群体遗传学](#群体遗传学)
- [空间组学](#空间组学)
- [图基因组学](#图基因组学)
- [蛋白质语言模型](#蛋白质语言模型)

</details>

---

## 分类总览

| 分类 | 算法数 | 描述 |
|----------|------------|-------------|
| 序列比对 | 19 | 用于比较和对齐生物序列的算法 |
| 序列组装 | 14 | 从短读段重建完整序列的算法 |
| 变异检测 | 14 | 检测基因组变异的算法 |
| 基因表达分析 | 12 | 分析基因表达水平的算法 |
| 蛋白质结构预测 | 14 | 预测蛋白质三维结构的算法 |
| 系统发育分析 | 12 | 构建和分析进化树的算法 |
| 功能注释 | 12 | 预测基因和蛋白质功能的算法 |
| 数据压缩 | 8 | 压缩生物信息学数据的算法 |
| 单细胞基因组学 | 15 | 单细胞水平的基因组和转录组分析算法 |
| 宏基因组学 | 12 | 微生物群落的基因组分析算法 |
| 表观基因组学 | 6 | 分析表观遗传修饰的算法 |
| 基因预测 | 9 | 基因结构预测和基因组注释算法 |
| 群体遗传学 | 12 | 分析群体遗传结构和进化的算法 |
| 空间组学 | 10 | 保留空间信息的组学数据分析算法 |
| 图基因组学 | 8 | 基于图结构表示和分析基因组的算法 |
| 蛋白质语言模型 | 9 | 基于大规模预训练模型的蛋白质分析算法 |


---

## 算法列表

### 序列比对 <a id="序列比对"></a>
<a href="#目录">↑ 返回顶部</a>

**双序列比对**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| ⭐ BLAST | 1990 | O(mn) | O(mn) | `heuristic` `database-search` `classic` |
| ⭐ Smith-Waterman | 1981 | O(mn) | O(mn) | `dynamic-programming` `local-alignment` `classic` |
| ⭐ Needleman-Wunsch | 1970 | O(mn) | O(mn) | `dynamic-programming` `global-alignment` `classic` |
| 🆕 WFA2-lib | 2023 | O(ns) | O(s) | `wavefront` `adaptive` `ultra-fast` |
| Minimap2 | 2018 | O(n) | O(n) | `minimizer` `long-read` `versatile` |
| MMseqs2 | 2017 | O(mn) | O(m + n) | `clustering` `search` `fast` |
| Edlib | 2017 | O(mn / w) | O(m) | `edit-distance` `bit-parallel` `fast` |
| parasail | 2016 | O(mn / w) | O(m) | `simd` `parallel` `vectorized` |
| HISAT2 | 2015 | O(n) | O(n) | `fm-index` `splice-aware` `rna-seq` |
| DIAMOND | 2015 | O(mn) | O(m + n) | `heuristic` `protein-alignment` `fast` |
| Bowtie2 | 2012 | O(n) | O(n) | `fm-index` `short-read` `fast` |
| Burrows-Wheeler Transform Alignment | 2009 | O(n) | O(n) | `bwt` `indexing` `short-read` |
| Exonerate | 2005 | O(mn) | O(m) | `pairwise` `database-search` `versatile` |
| LASTZ | 2004 | O(n^2) | O(n) | `genome-alignment` `whole-genome` `classic` |

**多序列比对**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Clustal Omega | 2011 | O(n * L^2) | O(n * L) | `multiple-alignment` `guide-tree` `progressive` |
| Kalign | 2005 | O(n^2 * L) | O(n * L) | `multiple-alignment` `fast` `wu-manber` |
| MUSCLE | 2004 | O(n^2 * L) | O(n * L) | `multiple-alignment` `iterative` `refinement` |
| MAFFT | 2002 | O(n * L * log L) | O(n * L) | `fft` `multiple-alignment` `scalable` |
| POA | 2002 | O(n^2 * L^2) | O(n * L^2) | `multiple-alignment` `partial-order` `graph-based` |


### 序列组装 <a id="序列组装"></a>
<a href="#目录">↑ 返回顶部</a>

**从头组装**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 Verkko | 2023 | O(n log n) | O(n) | `t2t` `hybrid` `hifi` |
| Hifiasm | 2021 | O(n log n) | O(n) | `hifi` `haplotype-aware` `long-read` |
| Shasta | 2020 | O(n) | O(n) | `long-read` `fast` `run-length` |
| Flye | 2019 | O(n log n) | O(n) | `repeat-graph` `long-read` `ont` |
| Wtdbg2 | 2019 | O(n) | O(n) | `long-read` `fuzzy-bruijn` `fast` |
| Canu | 2017 | O(n^2) | O(n) | `long-read` `pacbio` `ont` |
| Unicycler | 2017 | O(n log n) | O(n) | `hybrid` `bacterial` `circular` |
| MaSuRCA | 2013 | O(n log n) | O(n) | `hybrid` `super-read` `de-novo` |
| QUAST | 2013 | O(n * r) | O(n) | `quality-assessment` `n50` `assembly-evaluation` |
| SPAdes | 2012 | O(n * k) | O(n) | `de-bruijn` `multi-kmer` `versatile` |
| Overlap-Layout-Consensus (OLC) | 2010 | O(n^2) | O(n^2) | `overlap` `long-read` `de-novo` |
| De Bruijn Graph Assembly | 2001 | O(n) | O(k * 4^k) | `graph-based` `k-mer` `de-novo` |

**参考引导组装**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| RagTag | 2022 | O(n log n) | O(n) | `reference-based` `scaffolding` `assembly-polishing` |
| Reference-Guided Assembly | 2011 | O(n log n) | O(n) | `reference-based` `scaffolding` `resequencing` |


### 变异检测 <a id="变异检测"></a>
<a href="#目录">↑ 返回顶部</a>

**单核苷酸变异**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 DeepSomatic | 2024 | O(n * r) | O(r) | `deep-learning` `somatic` `cancer` |
| Clair3 | 2022 | O(n * r) | O(r) | `long-read` `nanopore` `pacbio` |
| Octopus | 2021 | O(n * h) | O(h) | `bayesian` `haplotype` `germline-somatic` |
| DeepVariant | 2018 | O(n * r) | O(r) | `deep-learning` `cnn` `snp` |
| Strelka2 | 2018 | O(n * r) | O(r) | `somatic` `germline` `fast` |
| MuTect2 | 2013 | O(n * r) | O(r) | `somatic` `cancer` `gatk` |
| FreeBayes | 2012 | O(n * h) | O(h) | `bayesian` `haplotype` `polyploid` |
| GATK HaplotypeCaller | 2010 | O(n * r) | O(r) | `haplotype` `snp` `indel` |

**结构变异**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 Sniffles2 | 2023 | O(n * c) | O(n) | `structural-variant` `long-read` `breakpoint` |
| cuteSV | 2020 | O(n * c) | O(n) | `structural-variant` `long-read` `clustering` |
| GRIDSS | 2017 | O(n * c) | O(n) | `structural-variant` `breakend` `assembly-based` |
| Manta | 2016 | O(n * c) | O(c) | `structural-variant` `graph-assembly` `clinical` |
| SvABA | 2016 | O(n * c) | O(c) | `structural-variant` `somatic` `assembly-based` |
| Delly | 2012 | O(n * c) | O(n) | `structural-variant` `split-read` `paired-end` |


### 基因表达分析 <a id="基因表达分析"></a>
<a href="#目录">↑ 返回顶部</a>

**表达定量**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Salmon | 2017 | O(n) | O(t) | `selective-alignment` `quantification` `rna-seq` |
| Kallisto | 2016 | O(n) | O(t) | `pseudoalignment` `quantification` `rna-seq` |
| tximport | 2016 | O(n * t) | O(g) | `import` `summarization` `offset-correction` |
| StringTie | 2015 | O(n) | O(g) | `transcript-assembly` `quantification` `rna-seq` |
| STAR | 2013 | O(n) | O(g) | `rna-seq` `splice-aware` `alignment` |
| RSEM | 2011 | O(n * t) | O(t) | `quantification` `expectation-maximization` `rna-seq` |

**差异表达**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Sleuth | 2017 | O(n * g) | O(g) | `differential-expression` `bootstrap` `rna-seq` |
| NOISeq | 2015 | O(n * g) | O(g) | `differential-expression` `non-parametric` `noiseq` |
| DESeq2 | 2014 | O(n * g) | O(g) | `rna-seq` `differential-expression` `negative-binomial` |
| limma-voom | 2014 | O(n * g) | O(g) | `differential-expression` `precision-weight` `linear-model` |
| Ballgown | 2014 | O(n * g) | O(g) | `differential-expression` `fpkm` `transcript-level` |
| edgeR | 2010 | O(n * g) | O(g) | `rna-seq` `differential-expression` `empirical-bayes` |


### 蛋白质结构预测 <a id="蛋白质结构预测"></a>
<a href="#目录">↑ 返回顶部</a>

**从头预测**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 AlphaFold3 | 2024 | O(n^2) | O(n^2) | `deep-learning` `structure-prediction` `multi-modal` |
| 🆕 Chai-1 | 2024 | O(n^2) | O(n^2) | `structure-prediction` `multi-modal` `drug-discovery` |
| 🆕 Boltz-1 | 2024 | O(n^2) | O(n^2) | `structure-prediction` `open-source` `diffusion` |
| 🆕 ESMFold | 2023 | O(n^2) | O(n^2) | `language-model` `single-sequence` `fast` |
| OmegaFold | 2022 | O(n^2) | O(n^2) | `language-model` `single-sequence` `structure-prediction` |
| OpenFold | 2022 | O(n^2) | O(n^2) | `open-source` `trainable` `structure-prediction` |
| ColabFold | 2022 | O(n^2) | O(n^2) | `fast` `msa` `colab` |
| AlphaFold | 2021 | O(n^2) | O(n^2) | `deep-learning` `attention` `structure-prediction` |
| RoseTTAFold | 2021 | O(n^2) | O(n^2) | `deep-learning` `three-track` `structure-prediction` |

**模板方法**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 Foldseek | 2023 | O(n) | O(n) | `structure-search` `fast` `3Di` |
| I-TASSER | 2008 | O(n^3) | O(n^2) | `threading` `template-based` `fragment-assembly` |
| TM-align | 2005 | O(n^3) | O(n^2) | `structure-alignment` `rmsd` `classic` |
| Rosetta | 2003 | O(n^3) | O(n^2) | `energy-function` `monte-carlo` `protein-design` |
| MODELLER | 1993 | O(n^2) | O(n^2) | `homology-modeling` `template-based` `comparative-modeling` |


### 系统发育分析 <a id="系统发育分析"></a>
<a href="#目录">↑ 返回顶部</a>

**距离法**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| ⭐ Neighbor-Joining | 1987 | O(n^3) | O(n^2) | `distance-based` `tree-building` `classic` |
| FastTree | 2010 | O(n * s * log n) | O(n * s) | `tree-building` `approximate-likelihood` `scalable` |

**特征法**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| IQ-TREE 2 | 2020 | O(n^2 * s) | O(n * s) | `maximum-likelihood` `model-finder` `partition` |
| RAxML-NG | 2019 | O(n^2 * s * r) | O(n * s) | `maximum-likelihood` `scalable` `ultrafast-bootstrap` |
| ASTRAL | 2018 | O(n * m) | O(n * m) | `species-tree` `summary-method` `coalescent` |
| RevBayes | 2016 | O(n^2 * s * r) | O(n * s) | `bayesian` `probabilistic-programming` `flexible` |
| IQ-TREE | 2015 | O(n^2 * s) | O(n * s) | `maximum-likelihood` `model-selection` `ultrafast-bootstrap` |
| Maximum Likelihood Phylogeny | 2014 | O(n^2 * s * r) | O(n * s) | `maximum-likelihood` `statistical` `tree-building` |
| BEAST2 | 2014 | O(n^2 * s * r) | O(n * s) | `bayesian` `mcmc` `phylodynamics` |
| MrBayes | 2012 | O(n^2 * s * r) | O(n * s) | `bayesian` `mcmc` `metropolis-coupled` |
| PhyML | 2003 | O(n^2 * s) | O(n * s) | `maximum-likelihood` `fast` `model-selection` |
| Bayesian Phylogenetic Inference | 2001 | O(n^2 * s * r) | O(n * s) | `bayesian` `mcmc` `molecular-clock` |


### 功能注释 <a id="功能注释"></a>
<a href="#目录">↑ 返回顶部</a>

**同源性方法**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| ⭐ BLAST-based Annotation | 1990 | O(mn) | O(m) | `sequence-similarity` `database-search` `classic` |
| Bakta | 2021 | O(n) | O(n) | `prokaryotic` `annotation` `standardized` |
| KofamKOALA | 2020 | O(n * m) | O(m) | `kegg` `orthology` `annotation` |
| OrthoFinder | 2019 | O(n^2) | O(n^2) | `orthology` `comparative-genomics` `gene-family` |
| eggNOG-mapper | 2017 | O(n * m) | O(m) | `orthology` `go-annotation` `kegg` |
| Prokka | 2014 | O(n) | O(n) | `prokaryotic` `annotation` `pipeline` |

**结构域方法**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| SignalP | 2019 | O(n) | O(n) | `signal-peptide` `deep-learning` `secretion` |
| InterProScan | 2014 | O(m * d) | O(m) | `multi-database` `domain-detection` `go-annotation` |
| InterPro | 2014 | O(m * d) | O(m) | `database` `domain` `protein-family` |
| HMMER | 2011 | O(mn) | O(m) | `hmm` `domain-detection` `remote-homology` |
| PfamScan | 2011 | O(mn) | O(m) | `domain-detection` `pfam` `protein-family` |
| TMHMM | 2001 | O(n) | O(n) | `transmembrane` `hmm` `membrane-protein` |


### 数据压缩 <a id="数据压缩"></a>
<a href="#目录">↑ 返回顶部</a>

**专用压缩**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Genozip | 2021 | O(n) | O(1) | `multi-format` `high-ratio` `random-access` |
| SPRING Compress | 2020 | O(n log n) | O(n) | `fastq` `reordering` `high-ratio` |
| SPRING | 2019 | O(n) | O(n) | `fastq` `specialized-compression` `high-ratio` |
| fqzcomp | 2014 | O(n) | O(1) | `fastq` `quality-score` `lossless` |
| DSRC | 2013 | O(n) | O(1) | `fastq` `specialized-compression` `archival` |
| CRAM | 2011 | O(n) | O(r) | `reference-based` `alignment` `bam` |

**通用压缩**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| BGZF and Tabix | 2011 | O(n) | O(1) | `block-compression` `indexing` `random-access` |
| GZIP for FASTQ | 1992 | O(n) | O(1) | `lossless` `general-purpose` `standard` |


### 单细胞基因组学 <a id="单细胞基因组学"></a>
<a href="#目录">↑ 返回顶部</a>

**细胞聚类与注释**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 scVI-tools | 2023 | O(c * g * e) | O(c * g) | `variational-autoencoder` `deep-learning` `batch-correction` |
| scArches | 2022 | O(c * g * e) | O(c * g) | `reference-mapping` `transfer-learning` `surgery` |
| CellTypist | 2022 | O(c * g) | O(c * g) | `cell-type` `annotation` `logistic-regression` |
| scANVI | 2021 | O(c * g * e) | O(c * g) | `semi-supervised` `annotation` `deep-learning` |
| SCENIC | 2020 | O(c * g^2) | O(c * g) | `regulatory-network` `transcription-factor` `grn` |
| Harmony | 2019 | O(c * k) | O(c * k) | `batch-correction` `integration` `embedding` |
| Monocle 3 | 2019 | O(c * g) | O(c * g) | `trajectory-inference` `pseudotime` `differentiation` |
| Scanpy | 2018 | O(c * g) | O(c * g) | `python` `scalable` `scverse` |
| scVI | 2018 | O(c * g * e) | O(c * g) | `deep-learning` `vae` `batch-correction` |
| Seurat | 2015 | O(c * g) | O(c * g) | `clustering` `multi-modal` `integration` |

**数据预处理**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| alevin-fry | 2022 | O(n * k) | O(g) | `quantification` `memory-efficient` `simpleaf` |
| STARsolo | 2021 | O(n * g) | O(c * g) | `preprocessing` `alignment` `umi` |
| kallisto + bustools | 2021 | O(n * k) | O(g) | `preprocessing` `pseudoalignment` `fast` |
| Alevin | 2019 | O(n * g) | O(c * g) | `preprocessing` `umi` `lightweight-mapping` |
| Cell Ranger | 2017 | O(n * g) | O(c * g) | `10x-genomics` `preprocessing` `umi` |


### 宏基因组学 <a id="宏基因组学"></a>
<a href="#目录">↑ 返回顶部</a>

**物种分类**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 MetaPhlAn 4 | 2023 | O(n * m) | O(m) | `marker-gene` `profiling` `enhanced` |
| Kraken2 | 2019 | O(n * k) | O(d) | `k-mer` `classification` `fast` |
| QIIME 2 | 2019 | O(n * d) | O(n) | `pipeline` `microbiome` `diversity` |
| mOTUs | 2017 | O(n * m) | O(m) | `marker-gene` `profiling` `universal` |
| Bracken | 2017 | O(n) | O(d) | `abundance-estimation` `bayesian` `kraken` |
| Centrifuge | 2016 | O(n * log d) | O(d) | `classification` `compressed-index` `low-memory` |
| Kaiju | 2016 | O(n * log d) | O(d) | `protein-level` `classification` `sensitive` |
| MetaPhlAn | 2012 | O(n * m) | O(m) | `marker-gene` `abundance` `low-memory` |

**功能分析**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| MetaBAT 2 | 2019 | O(n * c) | O(n) | `binning` `mags` `coverage` |
| HUMAnN 3 | 2018 | O(n * d) | O(d) | `functional-profiling` `pathway` `gene-families` |
| MaxBin 2 | 2016 | O(n * c) | O(n) | `binning` `expectation-maximization` `mags` |
| HUMAnN | 2014 | O(n * d) | O(d) | `pathway-analysis` `gene-family` `functional` |


### 表观基因组学 <a id="表观基因组学"></a>
<a href="#目录">↑ 返回顶部</a>

**ChIP-seq 分析**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| HMMRATAC | 2019 | O(n) | O(n) | `atac-seq` `hmm` `peak-calling` |
| ChromHMM | 2012 | O(n * s^2) | O(n * s) | `hmm` `chromatin-state` `histone` |
| MACS2 | 2008 | O(n) | O(n) | `peak-calling` `chip-seq` `histone` |

**甲基化分析**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| DSS | 2014 | O(n * s) | O(n) | `methylation` `beta-binomial` `dmr` |
| methylKit | 2012 | O(n * s) | O(n) | `methylation` `differential-analysis` `rrbs` |
| Bismark | 2011 | O(n * g) | O(g) | `bisulfite-seq` `methylation` `cpg` |


### 基因预测 <a id="基因预测"></a>
<a href="#目录">↑ 返回顶部</a>

**真核基因预测**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| BRAKER | 2016 | O(n * g) | O(n) | `pipeline` `evidence-based` `automated` |
| MAKER | 2008 | O(n * g) | O(n) | `annotation-pipeline` `evidence-based` `eukaryotic` |
| SNAP | 2004 | O(n * s) | O(n) | `semi-hmm` `ab-initio` `eukaryotic` |
| AUGUSTUS | 2003 | O(n * s^2) | O(n * s) | `ghmm` `ab-initio` `exon-intron` |

**原核基因预测**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Prodigal | 2010 | O(n) | O(n) | `prokaryotic` `self-training` `metagenome` |
| RNAmmer | 2007 | O(n * s) | O(n) | `rrna` `gene-prediction` `hmm` |
| GeneMark-ES | 2005 | O(n) | O(n) | `gene-prediction` `hmm` `prokaryotic` |
| GLIMMER | 1998 | O(n) | O(n) | `interpolated-markov-model` `prokaryotic` `gene-finding` |
| GeneMark | 1993 | O(n) | O(n) | `hmm` `coding-potential` `gene-finding` |


### 群体遗传学 <a id="群体遗传学"></a>
<a href="#目录">↑ 返回顶部</a>

**选择信号检测**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| ⭐ Tajima's D | 1989 | O(n * L) | O(L) | `neutrality-test` `selection` `classic` |
| PCAdapt | 2016 | O(n * m * k) | O(n * m) | `selection` `pca` `outlier-detection` |
| Selscan | 2014 | O(n * m) | O(n * m) | `selection` `haplotype` `ihs` |
| HapFLK | 2013 | O(n * m * K) | O(m * K) | `selection` `haplotype` `population-differentiation` |
| BayeScan | 2008 | O(m * k * n) | O(m * k) | `selection` `bayesian` `fst` |

**全基因组关联分析**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| REGENIE | 2021 | O(n * m) | O(n * m) | `gwas` `scalable` `two-stage` |
| SAIGE | 2018 | O(n * m) | O(n * m) | `gwas` `mixed-model` `rare-variant` |
| BOLT-LMM | 2015 | O(n * m) | O(n * m) | `lmm` `gwas` `scalable` |
| PLINK | 2007 | O(n * m) | O(n * m) | `gwas` `association` `qc` |

**主成分与群体结构**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| ADMIXTURE | 2009 | O(n * m * k) | O(n * m) | `ancestry` `maximum-likelihood` `population-structure` |
| PCA for Population Structure | 2006 | O(n * m * k) | O(n * m) | `pca` `population-structure` `ancestry` |
| STRUCTURE | 2000 | O(n * m * k * g) | O(n * k) | `bayesian` `mcmc` `population-structure` |


### 空间组学 <a id="空间组学"></a>
<a href="#目录">↑ 返回顶部</a>

**空间转录组学**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Seurat Spatial | 2021 | O(c * g) | O(c * g) | `spatial` `clustering` `integration` |
| Giotto Suite | 2021 | O(c * g) | O(c * g) | `spatial` `multi-platform` `comprehensive` |
| Squidpy | 2021 | O(c * g) | O(c * g) | `spatial` `graph-analysis` `cell-interaction` |
| SPARK-X | 2021 | O(g * n) | O(n) | `spatial` `fast` `non-parametric` |
| stLearn | 2021 | O(c * g) | O(c * g) | `spatial` `image-integration` `trajectory` |
| SPARK | 2019 | O(g * n^2) | O(n^2) | `spatial` `spatially-variable-gene` `statistical` |
| SpatialDE | 2018 | O(g * n^2) | O(n^2) | `spatial` `gaussian-process` `pattern-detection` |

**空间蛋白质组学**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| CellChat | 2021 | O(c^2 * g) | O(c^2) | `cell-communication` `ligand-receptor` `signaling` |
| Cellpose | 2020 | O(p) | O(p) | `segmentation` `deep-learning` `cell-detection` |
| StarDist | 2018 | O(p) | O(p) | `segmentation` `deep-learning` `cell-nuclei` |


### 图基因组学 <a id="图基因组学"></a>
<a href="#目录">↑ 返回顶部</a>

**变异图**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 PanVC | 2023 | O(n * m) | O(n) | `pangenome` `variant-calling` `genotyping` |
| GraphAligner | 2019 | O(n * d) | O(n) | `graph-alignment` `long-read` `variation-graph` |
| VG (Variation Graph) | 2017 | O(n log n) | O(n) | `variation-graph` `alignment` `variant-calling` |
| GCSA2 | 2017 | O(n) | O(n) | `indexing` `k-mer` `compressed-suffix-array` |

**泛基因组**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| Minigraph | 2020 | O(n log n) | O(n) | `pangenome` `graph-alignment` `minimizer` |
| odgi | 2020 | O(n) | O(n) | `pangenome` `graph-operations` `visualization` |
| seqwish | 2020 | O(n^2) | O(n^2) | `pangenome` `graph-construction` `alignment-to-graph` |
| Cactus | 2011 | O(n^2 * k) | O(n * k) | `pangenome` `alignment` `progressive` |


### 蛋白质语言模型 <a id="蛋白质语言模型"></a>
<a href="#目录">↑ 返回顶部</a>

**蛋白质功能预测**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 RFdiffusion | 2023 | O(n^2 * T) | O(n^2) | `diffusion-model` `protein-design` `structure-generation` |
| ProteinMPNN | 2022 | O(n^2 * d) | O(n^2) | `protein-design` `inverse-folding` `graph-neural-network` |
| ESM-1v | 2021 | O(n^2 * d) | O(n^2) | `variant-effect` `zero-shot` `pathogenicity` |
| ProGen | 2020 | O(n^2 * d) | O(n^2) | `generative` `protein-design` `conditional-generation` |
| DeepSEA | 2015 | O(n * d) | O(d) | `deep-learning` `functional-prediction` `chromatin` |

**蛋白质语言模型预训练**

| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |
|-----------|------|------|-------|------|
| 🆕 Ankh | 2023 | O(n^2 * d) | O(n^2) | `language-model` `lightweight` `efficient` |
| ESM-2 | 2022 | O(n^2 * d) | O(n^2) | `language-model` `transformer` `representation-learning` |
| ProtTrans | 2021 | O(n^2 * d) | O(n^2) | `language-model` `transfer-learning` `representation-learning` |
| ProtBERT | 2020 | O(n^2 * d) | O(n^2) | `language-model` `bert` `sequence-embedding` |



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
