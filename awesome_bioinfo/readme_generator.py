"""
README Generator for Awesome Bioinformatics Algorithms.
Generates the Chinese README.md from algorithm data.
"""

import os
import re

from .algorithm_registry import AlgorithmRegistry
from .category_manager import CategoryManager
from .schema import AlgorithmEntry, Category


class ReadmeGenerator:
    """Generates README.md from algorithm registry and categories."""

    def __init__(
        self,
        registry: AlgorithmRegistry,
        category_manager: CategoryManager,
        template_path: str = "templates/readme_template.md",
    ):
        self._registry = registry
        self._category_manager = category_manager
        self._template_path = template_path

    def generate(self) -> str:
        """Generate the complete README content."""
        template = self._load_template()

        stats = self._registry.get_statistics()
        toc = self.generate_toc()
        category_overview = self._generate_category_overview()
        featured_content = self._generate_featured_content()

        readme = template.replace("{{ total_algorithms }}", str(stats.total_algorithms))
        readme = readme.replace("{{ total_categories }}", str(stats.total_categories))
        readme = readme.replace("{{ total_tags }}", str(stats.total_tags))
        readme = readme.replace("{{ toc }}", toc)
        readme = readme.replace("{{ category_overview }}", category_overview)
        readme = readme.replace("{{ featured_content }}", featured_content)

        return readme

    def _load_template(self) -> str:
        """Load the README template file."""
        if os.path.exists(self._template_path):
            with open(self._template_path, encoding="utf-8") as f:
                return f.read()
        return self._default_template()

    def _default_template(self) -> str:
        """Return default template if file not found."""
        return """# Awesome Bioinformatics Algorithms

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> 精选生物信息学算法合集，附时间/空间复杂度分析

## 统计摘要

- 📊 算法总数: {{ total_algorithms }}
- 📁 分类数量: {{ total_categories }}
- 🏷️ 标签数量: {{ total_tags }}

## 目录

{{ toc }}

---

{{ category_overview }}

---

{{ featured_content }}

---

## 贡献

欢迎贡献！详见[贡献指南](CONTRIBUTING.md)。

## 许可证

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](https://creativecommons.org/publicdomain/zero/1.0/)
"""

    def generate_toc(self) -> str:
        """Generate table of contents with anchor links."""
        toc_lines = ["<details>", "<summary>点击展开</summary>", ""]
        categories = self._category_manager.list_all_categories()

        for category in categories:
            algos = self._registry.get_by_category(category.id)
            if algos:  # Only include categories with algorithms
                anchor = self._generate_anchor(category.name)
                toc_lines.append(f"- [{category.name}](#{anchor})")

        toc_lines.extend(["", "</details>"])
        return "\n".join(toc_lines)

    @staticmethod
    def _generate_anchor(text: str) -> str:
        """Generate a valid Markdown anchor from text."""
        anchor = text.lower()
        anchor = anchor.replace(" ", "-")
        anchor = re.sub(r"[^\w\u4e00-\u9fff-]", "", anchor)
        anchor = re.sub(r"-+", "-", anchor)
        anchor = anchor.strip("-")
        return anchor

    @staticmethod
    def _escape_cell(value: str) -> str:
        """Escape pipe characters in data values so they cannot break table rows."""
        return str(value).replace("|", r"\|")

    def _generate_category_overview(self) -> str:
        """Generate category overview table with statistics."""
        lines = ["## 分类总览", ""]
        lines.append("| 分类 | 算法数 | 描述 |")
        lines.append("|----------|------------|-------------|")

        categories = self._category_manager.list_all_categories()
        for category in categories:
            algos = self._registry.get_by_category(category.id)
            if algos:
                count = len(algos)
                name = self._escape_cell(category.name)
                description = self._escape_cell(category.description)
                lines.append(f"| {name} | {count} | {description} |")

        lines.append("")
        return "\n".join(lines)

    def _generate_featured_content(self) -> str:
        """Generate the full algorithm listing grouped by category."""
        sections = ["## 算法列表", ""]
        categories = self._category_manager.list_all_categories()

        for category in categories:
            section = self._generate_category_section(category)
            if section.strip():
                sections.append(section)
                sections.append("")

        return "\n".join(sections)

    def _generate_category_section(self, category: Category) -> str:
        """Generate the markdown section listing all algorithms in one category."""
        lines = []
        all_algos = self._registry.get_by_category(category.id)

        if not all_algos:
            return ""

        # Category header with anchor and back-to-top link
        anchor = self._generate_anchor(category.name)
        lines.append(f'### {category.name} <a id="{anchor}"></a>')
        lines.append('<a href="#目录">↑ 返回顶部</a>')
        lines.append("")

        # Get all algorithms with their subcategory info
        algo_data = []
        for algo in all_algos:
            subcategory_name = ""
            if algo.subcategory:
                for sub in category.subcategories:
                    if sub.id == algo.subcategory:
                        subcategory_name = sub.name
                        break
            algo_data.append((algo, subcategory_name))

        # Sort by importance: classic first, then by year (newer first)
        algo_data.sort(
            key=lambda x: (
                0 if x[0].is_classic() else (1 if x[0].is_new() else 2),
                -x[0].year if x[0].year else 0,
            )
        )

        # Group by subcategory
        subcategory_groups: dict[str, list[tuple[AlgorithmEntry, str]]] = {}
        for algo, sub_name in algo_data:
            key = sub_name or "通用"
            if key not in subcategory_groups:
                subcategory_groups[key] = []
            subcategory_groups[key].append((algo, sub_name))

        # Generate tables for each subcategory
        for sub_name, algos in subcategory_groups.items():
            if sub_name != "通用":
                lines.append(f"**{sub_name}**")
                lines.append("")

            # Table header
            lines.append("| 算法 | 年份 | 时间复杂度 | 空间复杂度 | 标签 |")
            lines.append("|-----------|------|------|-------|------|")

            for algo, _ in algos:
                badge = algo.get_year_badge()
                name = self._escape_cell(f"{badge} {algo.name}" if badge else algo.name)
                year = self._escape_cell(str(algo.year) if algo.year else "-")
                time = self._escape_cell(algo.time_complexity)
                space = self._escape_cell(algo.space_complexity or "-")
                tags = " ".join([f"`{t}`" for t in algo.tags[:3]]) if algo.tags else "-"
                tags = self._escape_cell(tags)

                lines.append(f"| {name} | {year} | {time} | {space} | {tags} |")

            lines.append("")

        return "\n".join(lines)

    def _get_subcategory_algorithms(
        self, category_id: str, subcategory_id: str
    ) -> list[AlgorithmEntry]:
        """Return algorithms that match both the parent category and subcategory."""
        return [
            algo
            for algo in self._registry.get_by_subcategory(subcategory_id)
            if algo.category == category_id
        ]

    def generate_statistics(self) -> str:
        """Generate the statistics section."""
        stats = self._registry.get_statistics()
        lines = [
            f"- 📊 算法总数: {stats.total_algorithms}",
            f"- 📁 分类数量: {stats.total_categories}",
            f"- 🏷️ 标签数量: {stats.total_tags}",
        ]
        return "\n".join(lines)

    def save(self, output_path: str = "README.md") -> None:
        """Generate and save README to file."""
        content = self.generate()
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
