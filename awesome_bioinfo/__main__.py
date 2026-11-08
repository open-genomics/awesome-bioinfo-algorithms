#!/usr/bin/env python3
"""
CLI entry point for Awesome Bioinformatics Algorithms scripts.

Usage:
    python -m awesome_bioinfo generate                     # Generate README.md
    python -m awesome_bioinfo validate                     # Validate all data files
    python -m awesome_bioinfo stats                        # Show statistics
    python -m awesome_bioinfo search [options]             # Search algorithms
    python -m awesome_bioinfo info <id>                    # Show algorithm details
    python -m awesome_bioinfo compare <id1> <id2>          # Compare two algorithms
    python -m awesome_bioinfo export [options]             # Export data to JSON/CSV
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path
from typing import Optional

from .algorithm_registry import AlgorithmRegistry
from .category_manager import CategoryManager
from .data_store import DataStore
from .readme_generator import ReadmeGenerator
from .schema import DIFFICULTY_LABELS, VALID_DIFFICULTIES, AlgorithmEntry
from .validate import Validator


def get_base_dir() -> Path:
    """Return the project root directory for a repository checkout."""
    return Path(__file__).resolve().parent.parent


def validate_repo_layout(base_dir: Path) -> list[str]:
    """Return missing repository paths required by the maintenance CLI."""
    required_paths = [
        base_dir / "data" / "categories.yaml",
        base_dir / "data" / "algorithms",
        base_dir / "templates" / "readme_template.md",
    ]
    return [str(path) for path in required_paths if not path.exists()]


def ensure_repo_layout() -> tuple[Path, list[str]]:
    """Validate that commands are being run from a repository checkout."""
    base_dir = get_base_dir()
    return base_dir, validate_repo_layout(base_dir)


def _print_repo_layout_error(missing_paths: list[str]) -> int:
    print("Error: This command must be run from an intact repository checkout.")
    print("Missing required paths:")
    for path in missing_paths:
        print(f"  - {path}")
    return 1


def _load_data_store(base_dir: Path) -> DataStore:
    """Load and return an initialized DataStore."""
    return DataStore(base_dir).load_all()


def _load_registry_and_categories(base_dir: Path) -> tuple[AlgorithmRegistry, CategoryManager]:
    """Load and return an initialized registry and category manager."""
    store = _load_data_store(base_dir)
    return store.registry, store.category_manager


# =========================================================================
# Search functions (merged from search.py)
# =========================================================================


def search_algorithms(
    registry: AlgorithmRegistry,
    category_manager: CategoryManager,
    keyword: str = "",
    tag: str = "",
    category: str = "",
    difficulty: str = "",
) -> list[AlgorithmEntry]:
    """Search algorithms with optional filters."""
    if keyword:
        results = registry.search(keyword)
    else:
        results = registry.get_all_algorithms()

    if tag:
        tag_lower = tag.lower()
        results = [a for a in results if any(tag_lower in t.lower() for t in a.tags)]

    if category:
        results = [a for a in results if a.category == category or a.subcategory == category]

    if difficulty:
        results = [a for a in results if a.difficulty == difficulty]

    return results


def format_algorithm_short(algo: AlgorithmEntry, category_manager: CategoryManager) -> str:
    """Format a single algorithm as a short listing line."""
    cat = category_manager.get_category(algo.category)
    cat_label = cat.name_en if cat else algo.category
    year_str = f" ({algo.year})" if algo.year else ""
    diff_str = f" [{algo.difficulty}]" if algo.difficulty else ""
    return f"  {algo.id}{year_str} - {algo.name}{diff_str} | {cat_label}"


def cmd_search(
    registry: AlgorithmRegistry,
    category_manager: CategoryManager,
    keyword: str = "",
    tag: str = "",
    category: str = "",
    difficulty: str = "",
) -> int:
    """Execute the search command."""
    if difficulty and difficulty not in VALID_DIFFICULTIES:
        print(f"Invalid difficulty: '{difficulty}'. Valid: {', '.join(VALID_DIFFICULTIES)}")
        return 1

    if not any([keyword, tag, category, difficulty]):
        print("Usage: python -m awesome_bioinfo search [options]")
        print("Options:")
        print("  --keyword <text>    Search in name, description, purpose, tags")
        print("  --tag <tag>         Filter by tag")
        print("  --category <id>     Filter by category ID")
        print("  --difficulty <d>    Filter by difficulty (beginner/intermediate/advanced)")
        return 1

    results = search_algorithms(registry, category_manager, keyword, tag, category, difficulty)

    if not results:
        print("No algorithms found matching your criteria.")
        return 0

    print(f"Found {len(results)} algorithm(s):\n")
    for algo in results:
        print(format_algorithm_short(algo, category_manager))

    return 0


# =========================================================================
# Info functions (merged from info_cmd.py)
# =========================================================================


def cmd_info(
    registry: AlgorithmRegistry,
    category_manager: CategoryManager,
    algo_id: str,
) -> int:
    """Show detailed info about an algorithm."""
    algo = registry.get_algorithm(algo_id)
    if not algo:
        matches = registry.search(algo_id)
        if not matches:
            print(f"Algorithm not found: '{algo_id}'")
            return 1
        if len(matches) > 1:
            print(f"Multiple matches for '{algo_id}':")
            for m in matches:
                print(f"  - {m.id}: {m.name}")
            return 1
        algo = matches[0]

    cat = category_manager.get_category(algo.category)
    sub = category_manager.get_category(algo.subcategory) if algo.subcategory else None

    print(f"{'=' * 60}")
    print(f"  {algo.name}" + (f" ({algo.year})" if algo.year else ""))
    print(f"{'=' * 60}")
    print(f"  ID:               {algo.id}")
    print(
        f"  分类:             {cat.name} ({cat.name_en})"
        if cat
        else f"  分类:             {algo.category}"
    )
    if sub:
        print(f"  子分类:           {sub.name} ({sub.name_en})")
    if algo.difficulty:
        print(f"  难度:             {DIFFICULTY_LABELS.get(algo.difficulty, algo.difficulty)}")
    print()
    print("  描述:")
    for line in algo.description.strip().split("\n"):
        print(f"    {line.strip()}")
    print()
    print(f"  用途:             {algo.purpose}")
    print(f"  时间复杂度:       {algo.time_complexity}")
    if algo.space_complexity:
        print(f"  空间复杂度:       {algo.space_complexity}")
    if algo.language:
        print(f"  实现语言:         {', '.join(algo.language)}")
    if algo.paper_url:
        print(f"  论文:             {algo.paper_url}")
    if algo.implementation_url:
        print(f"  实现:             {algo.implementation_url}")
    if algo.related_tools:
        print(f"  相关工具:         {', '.join(algo.related_tools)}")
    if algo.tags:
        print(f"  标签:             {', '.join(algo.tags)}")
    if algo.references:
        print("  扩展资料:")
        for ref in algo.references:
            title = ref.title or ref.url
            ref_type = f" [{ref.type}]" if ref.type else ""
            print(f"    - {title}{ref_type}: {ref.url}")

    print()
    return 0


# =========================================================================
# Compare functions (merged from compare.py)
# =========================================================================


def _resolve_algorithm(
    registry: AlgorithmRegistry, algo_id: str
) -> tuple[Optional[AlgorithmEntry], list[AlgorithmEntry]]:
    """Resolve an algorithm by exact ID or unambiguous fuzzy search."""
    algo = registry.get_algorithm(algo_id)
    if algo:
        return algo, []
    matches = registry.search(algo_id)
    if len(matches) == 1:
        return matches[0], []
    if len(matches) > 1:
        return None, matches
    return None, []


def cmd_compare(
    registry: AlgorithmRegistry,
    category_manager: CategoryManager,
    id1: str,
    id2: str,
) -> int:
    """Compare two algorithms side by side."""
    r1, r1_candidates = _resolve_algorithm(registry, id1)
    r2, r2_candidates = _resolve_algorithm(registry, id2)

    problems: list[tuple[str, str, Optional[list[AlgorithmEntry]]]] = []
    if r1_candidates:
        problems.append(("ambiguous", id1, r1_candidates))
    elif not r1:
        problems.append(("missing", id1, None))

    if r2_candidates:
        problems.append(("ambiguous", id2, r2_candidates))
    elif not r2:
        problems.append(("missing", id2, None))

    if problems:
        for problem_type, query, candidates in problems:
            if problem_type == "ambiguous":
                assert candidates is not None
                print(f"Ambiguous argument '{query}': matches multiple algorithms:")
                for candidate in candidates:
                    print(f"  - {candidate.id}: {candidate.name}")
            else:
                print(f"Algorithm not found: '{query}'")
        return 1

    assert r1 is not None
    assert r2 is not None
    a1 = r1
    a2 = r2

    fields = [
        ("Name", lambda a: a.name),
        ("Year", lambda a: str(a.year) if a.year else "-"),
        ("Category", lambda a: a.category),
        ("Difficulty", lambda a: a.difficulty or "-"),
        ("Time Complexity", lambda a: a.time_complexity),
        ("Space Complexity", lambda a: a.space_complexity or "-"),
        ("Language", lambda a: ", ".join(a.language) if a.language else "-"),
        ("Purpose", lambda a: a.purpose),
        ("Related Tools", lambda a: ", ".join(a.related_tools) if a.related_tools else "-"),
        ("Tags", lambda a: ", ".join(a.tags) if a.tags else "-"),
    ]

    w1, w2 = 40, 40
    print(f"{'Field':<20} | {'Algorithm 1':^{w1}} | {'Algorithm 2':^{w2}}")
    print(f"{'-' * 20}-+-{'-' * w1}-+-{'-' * w2}")
    print(f"{'ID':<20} | {a1.id:^{w1}} | {a2.id:^{w2}}")
    for label, getter in fields:
        v1 = getter(a1)
        v2 = getter(a2)
        print(f"{label:<20} | {v1:<{w1}} | {v2:<{w2}}")

    print()
    print(f"  Description ({a1.name}):")
    for line in a1.description.strip().split("\n")[:3]:
        print(f"    {line.strip()}")
    print()
    print(f"  Description ({a2.name}):")
    for line in a2.description.strip().split("\n")[:3]:
        print(f"    {line.strip()}")
    print()

    return 0


# =========================================================================
# Export functions (merged from export_cmd.py)
# =========================================================================


_CSV_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")


def _csv_safe(value: object) -> object:
    """Neutralize spreadsheet formula prefixes in exported CSV cells."""
    if isinstance(value, str) and value.startswith(_CSV_FORMULA_PREFIXES):
        return "'" + value
    return value


def cmd_export(
    registry: AlgorithmRegistry,
    category_manager: CategoryManager,
    fmt: str = "json",
    output: str = "",
) -> int:
    """Export all algorithms to JSON or CSV."""
    if fmt not in ("json", "csv"):
        print(f"Unsupported format: '{fmt}'. Use 'json' or 'csv'.")
        return 1

    algorithms = registry.get_all_algorithms()
    if not algorithms:
        print("No algorithms to export.")
        return 1

    if fmt == "json":
        data = {
            "algorithms": [a.to_dict() for a in algorithms],
            "total": len(algorithms),
        }
        content = json.dumps(data, ensure_ascii=False, indent=2)
    else:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(
            [
                "id",
                "name",
                "year",
                "category",
                "subcategory",
                "difficulty",
                "time_complexity",
                "space_complexity",
                "language",
                "tags",
                "purpose",
            ]
        )
        for a in algorithms:
            writer.writerow(
                [
                    _csv_safe(value)
                    for value in (
                        a.id,
                        a.name,
                        a.year or "",
                        a.category,
                        a.subcategory,
                        a.difficulty,
                        a.time_complexity,
                        a.space_complexity,
                        "|".join(a.language),
                        "|".join(a.tags),
                        a.purpose,
                    )
                ]
            )
        content = buf.getvalue()

    if output:
        with open(output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Exported {len(algorithms)} algorithms to {output}")
    else:
        sys.stdout.write(content)

    return 0


def cmd_generate(output_path: Optional[Path] = None) -> int:
    """Generate README.md from algorithm data."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    data_dir = base_dir / "data"
    categories_path = base_dir / "data" / "categories.yaml"
    algorithms_dir = base_dir / "data" / "algorithms"
    template_path = base_dir / "templates" / "readme_template.md"
    output_path = output_path or (base_dir / "README.md")

    print("Validating data files...")
    validator = Validator()
    validation_result = validator.validate_all(str(data_dir))
    if validation_result.errors:
        print(
            f"  Error: Cannot generate README with {len(validation_result.errors)} validation error(s)."
        )
        for error in validation_result.errors:
            print(f"    - {error}")
        return 1

    if validation_result.warnings:
        print(f"  Warning: {len(validation_result.warnings)} validation warning(s) detected.")
        for warning in validation_result.warnings:
            print(f"    - {warning}")

    print("Loading categories...")
    category_manager = CategoryManager()
    try:
        category_manager.load_categories(str(categories_path))
        print(f"  Loaded {len(category_manager.list_all_categories())} categories")
    except FileNotFoundError:
        print(f"  Warning: Categories file not found at {categories_path}")

    print("Loading algorithms...")
    registry = AlgorithmRegistry(str(algorithms_dir))
    try:
        registry.load_all()
    except ValueError as exc:
        print(f"  Error: {exc}")
        return 1
    stats = registry.get_statistics()
    print(f"  Loaded {stats.total_algorithms} algorithms")
    print(f"  Categories with algorithms: {stats.total_categories}")
    print(f"  Unique tags: {stats.total_tags}")

    print("Generating README...")
    generator = ReadmeGenerator(registry, category_manager, str(template_path))
    generator.save(str(output_path))
    print(f"  README saved to {output_path}")
    print("\nDone!")
    return 0


def cmd_validate() -> int:
    """Validate all data files."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    data_dir = base_dir / "data"

    print("Validating data files...")
    validator = Validator()
    result = validator.validate_all(str(data_dir))

    if result.errors:
        print(f"\n❌ {len(result.errors)} error(s):")
        for error in result.errors:
            print(f"  - {error}")

    if result.warnings:
        print(f"\n⚠️  {len(result.warnings)} warning(s):")
        for warning in result.warnings:
            print(f"  - {warning}")

    if result.is_valid:
        print("\n✅ All data files are valid!")
        return 0

    print("\n❌ Validation failed.")
    return 1


def cmd_stats() -> int:
    """Show statistics about the algorithm registry."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    registry, category_manager = _load_registry_and_categories(base_dir)
    stats = registry.get_statistics()

    print("📊 Awesome Bioinformatics Algorithms - Statistics")
    print("=" * 50)
    print(f"  算法总数 (Total Algorithms): {stats.total_algorithms}")
    print(f"  有算法的分类数 (Categories with algorithms): {stats.total_categories}")
    print(f"  标签数量 (Tags):             {stats.total_tags}")
    print()
    print("📁 Algorithms per Category:")
    for cat_id, count in sorted(stats.algorithms_by_category.items()):
        cat = category_manager.get_category(cat_id)
        label = f"{cat.name} ({cat.name_en})" if cat else cat_id
        print(f"  {label}: {count}")

    return 0


def cmd_search_cli(
    *,
    keyword: str = "",
    tag: str = "",
    category: str = "",
    difficulty: str = "",
) -> int:
    """CLI wrapper for the search command."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    registry, category_manager = _load_registry_and_categories(base_dir)
    return cmd_search(registry, category_manager, keyword, tag, category, difficulty)


def cmd_info_cli(algo_id: str) -> int:
    """CLI wrapper for the info command."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    registry, category_manager = _load_registry_and_categories(base_dir)
    return cmd_info(registry, category_manager, algo_id)


def cmd_compare_cli(id1: str, id2: str) -> int:
    """CLI wrapper for the compare command."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    registry, category_manager = _load_registry_and_categories(base_dir)
    return cmd_compare(registry, category_manager, id1, id2)


def cmd_export_cli(*, fmt: str = "json", output: str = "") -> int:
    """CLI wrapper for the export command."""
    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    registry, category_manager = _load_registry_and_categories(base_dir)
    return cmd_export(registry, category_manager, fmt, output)


def cmd_check_links() -> int:
    """Check validity of algorithm URLs."""
    from .link_checker import cmd_check_links as _cmd_check_links

    base_dir, missing_paths = ensure_repo_layout()
    if missing_paths:
        return _print_repo_layout_error(missing_paths)

    return _cmd_check_links()


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level CLI parser."""
    parser = argparse.ArgumentParser(prog="python -m awesome_bioinfo")
    subparsers = parser.add_subparsers(dest="command")

    generate_parser = subparsers.add_parser(
        "generate", help="Generate README.md from algorithm data"
    )
    generate_parser.add_argument("--output", type=Path, help="Write README output to a custom path")

    subparsers.add_parser("validate", help="Validate all YAML data files")
    subparsers.add_parser("stats", help="Show algorithm statistics")

    search_parser = subparsers.add_parser(
        "search", help="Search algorithms (keyword, tag, category, difficulty)"
    )
    search_parser.add_argument("keyword", nargs="?", default="", help="Keyword to search for")
    search_parser.add_argument(
        "--keyword", dest="keyword_flag", default="", help="Keyword to search for"
    )
    search_parser.add_argument("--tag", default="", help="Filter by tag")
    search_parser.add_argument(
        "--category", default="", help="Filter by category or subcategory ID"
    )
    search_parser.add_argument(
        "--difficulty",
        default="",
        help="Filter by difficulty (beginner/intermediate/advanced)",
    )

    info_parser = subparsers.add_parser("info", help="Show detailed info about an algorithm")
    info_parser.add_argument("algo_id", help="Algorithm ID or fuzzy keyword")

    compare_parser = subparsers.add_parser("compare", help="Compare two algorithms side by side")
    compare_parser.add_argument("id1", help="First algorithm ID or fuzzy keyword")
    compare_parser.add_argument("id2", help="Second algorithm ID or fuzzy keyword")

    export_parser = subparsers.add_parser("export", help="Export algorithms to JSON or CSV")
    export_parser.add_argument(
        "--format", dest="fmt", default="json", help="Export format: json or csv"
    )
    export_parser.add_argument("--output", default="", help="Write export output to a file")

    subparsers.add_parser("check-links", help="Check validity of algorithm URLs")

    return parser


def main(argv: Optional[list[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "generate":
        return cmd_generate(output_path=args.output)
    if args.command == "validate":
        return cmd_validate()
    if args.command == "stats":
        return cmd_stats()
    if args.command == "search":
        keyword = args.keyword_flag or args.keyword
        return cmd_search_cli(
            keyword=keyword,
            tag=args.tag,
            category=args.category,
            difficulty=args.difficulty,
        )
    if args.command == "info":
        return cmd_info_cli(args.algo_id)
    if args.command == "compare":
        return cmd_compare_cli(args.id1, args.id2)
    if args.command == "export":
        return cmd_export_cli(fmt=args.fmt, output=args.output)
    if args.command == "check-links":
        return cmd_check_links()
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
