"""
Data validation for Awesome Bioinformatics Algorithms.
Implements FieldValidator class for algorithm and category field validation.
"""

import os
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

import yaml

from .schema import VALID_DIFFICULTIES, VALID_REFERENCE_TYPES


@dataclass
class ValidationResult:
    """Result of a validation operation."""

    is_valid: bool
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)
        self.is_valid = False

    def add_warning(self, warning: str) -> None:
        """Add a warning message."""
        self.warnings.append(warning)

    def merge(self, other: "ValidationResult") -> None:
        """Merge another validation result into this one."""
        if not other.is_valid:
            self.is_valid = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)


class FieldValidator:
    """Validates algorithm entry field formats (pure functions, no external state)."""

    REQUIRED_ALGORITHM_FIELDS = [
        "id",
        "name",
        "description",
        "purpose",
        "time_complexity",
        "category",
    ]
    OPTIONAL_ALGORITHM_FIELDS = [
        "space_complexity",
        "year",
        "paper_url",
        "implementation_url",
        "related_tools",
        "tags",
        "subcategory",
        "difficulty",
        "language",
        "references",
        "description_en",
        "purpose_en",
    ]
    REQUIRED_CATEGORY_FIELDS = ["id", "name", "name_en"]
    OPTIONAL_CATEGORY_FIELDS = ["description", "description_en", "subcategories"]
    CATEGORY_STRING_FIELDS = ["id", "name", "name_en", "description"]
    ALGORITHM_STRING_FIELDS = [
        "id",
        "name",
        "description",
        "purpose",
        "time_complexity",
        "category",
        "space_complexity",
        "paper_url",
        "implementation_url",
        "subcategory",
        "description_en",
        "purpose_en",
    ]
    ALGORITHM_LIST_FIELDS = ["related_tools", "tags"]

    MIN_DESCRIPTION_LENGTH = 50
    MAX_DESCRIPTION_LENGTH = 500

    URL_PATTERN = re.compile(
        r"^https?://"
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"
        r"localhost|"
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
        r"(?::\d+)?"
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )

    def validate_algorithm_fields(self, data: dict[str, Any]) -> ValidationResult:
        """
        Validate an algorithm entry's field formats (does not validate category references).

        Args:
            data: Dictionary containing algorithm data

        Returns:
            ValidationResult with validation status and any errors/warnings
        """
        result = ValidationResult(is_valid=True)

        if not isinstance(data, dict):
            result.add_error(f"Algorithm entry must be a mapping, got {type(data).__name__}")
            return result

        allowed_fields = set(self.REQUIRED_ALGORITHM_FIELDS + self.OPTIONAL_ALGORITHM_FIELDS)
        unknown_fields = sorted(
            field_name for field_name in data if field_name not in allowed_fields
        )
        for field_name in unknown_fields:
            result.add_error(f"Unknown field: '{field_name}'")

        for field_name in self.REQUIRED_ALGORITHM_FIELDS:
            if field_name not in data:
                result.add_error(f"Missing required field: '{field_name}'")
                continue

            value = data[field_name]
            if field_name in self.ALGORITHM_STRING_FIELDS:
                if not isinstance(value, str):
                    result.add_error(
                        f"Field '{field_name}' must be a string, got {type(value).__name__}"
                    )
                elif not value.strip():
                    result.add_error(f"Required field '{field_name}' is empty")
            elif not value:
                result.add_error(f"Required field '{field_name}' is empty")

        optional_string_fields = [
            field_name
            for field_name in self.ALGORITHM_STRING_FIELDS
            if field_name not in self.REQUIRED_ALGORITHM_FIELDS
        ]
        for field_name in optional_string_fields:
            if field_name in data and not isinstance(data[field_name], str):
                result.add_error(
                    f"Field '{field_name}' must be a string, got {type(data[field_name]).__name__}"
                )

        for field_name in self.ALGORITHM_LIST_FIELDS:
            if field_name not in data:
                continue

            value = data[field_name]
            if not isinstance(value, list):
                result.add_error(f"Field '{field_name}' must be a list")
                continue

            for index, item in enumerate(value):
                if not isinstance(item, str):
                    result.add_error(
                        f"Field '{field_name}' item {index} must be a string, got {type(item).__name__}"
                    )
                elif not item.strip():
                    result.add_error(f"Field '{field_name}' item {index} cannot be empty")

        if not result.is_valid:
            return result

        description = data.get("description", "")
        desc_length = len(description.strip())
        if desc_length < self.MIN_DESCRIPTION_LENGTH:
            result.add_error(
                f"Description too short: {desc_length} characters "
                f"(minimum: {self.MIN_DESCRIPTION_LENGTH})"
            )
        elif desc_length > self.MAX_DESCRIPTION_LENGTH:
            result.add_error(
                f"Description too long: {desc_length} characters "
                f"(maximum: {self.MAX_DESCRIPTION_LENGTH})"
            )

        year = data.get("year", 0)
        # 非整数 year（含空字符串/null）会让 generate 的年份排序抛 TypeError，
        # 这里直接判错，而不是只给警告放行。
        if not isinstance(year, int) or isinstance(year, bool):
            result.add_error(f"Field 'year' must be an integer, got {type(year).__name__}: {year}")
        elif year and (year < 1950 or year > datetime.now().year + 5):
            result.add_warning(f"Suspicious year value: {year}")

        for url_field in ["paper_url", "implementation_url"]:
            url = data.get(url_field, "")
            if url and not self.URL_PATTERN.match(url):
                result.add_warning(f"Invalid URL format in '{url_field}': {url}")

        difficulty = data.get("difficulty", "")
        if difficulty:
            if not isinstance(difficulty, str):
                result.add_error(
                    f"Field 'difficulty' must be a string, got {type(difficulty).__name__}"
                )
            elif difficulty not in VALID_DIFFICULTIES:
                result.add_error(
                    f"Invalid difficulty: '{difficulty}'. "
                    f"Valid values: {', '.join(VALID_DIFFICULTIES)}"
                )

        language = data.get("language", [])
        if language is None or not isinstance(language, list):
            result.add_error("Field 'language' must be a list")
        else:
            for i, item in enumerate(language):
                if not isinstance(item, str):
                    result.add_error(
                        f"Field 'language' item {i} must be a string, got {type(item).__name__}"
                    )
                elif not item.strip():
                    result.add_error(f"Field 'language' item {i} cannot be empty")

        references = data.get("references", [])
        if references is None or not isinstance(references, list):
            result.add_error("Field 'references' must be a list")
        else:
            for i, ref in enumerate(references):
                if not isinstance(ref, dict):
                    result.add_error(
                        f"Field 'references' item {i} must be a mapping, got {type(ref).__name__}"
                    )
                    continue
                if "url" not in ref:
                    result.add_error(f"Field 'references' item {i} missing required 'url'")
                elif not isinstance(ref["url"], str) or not ref["url"].strip():
                    result.add_error(
                        f"Field 'references' item {i} 'url' must be a non-empty string"
                    )
                elif not self.URL_PATTERN.match(ref["url"]):
                    result.add_warning(f"Invalid URL in references item {i}: {ref['url']}")
                if "title" in ref and (
                    not isinstance(ref["title"], str) or not ref["title"].strip()
                ):
                    result.add_error(
                        f"Field 'references' item {i} 'title' must be a non-empty string"
                    )
                if "type" in ref:
                    if not isinstance(ref["type"], str):
                        result.add_error(f"Field 'references' item {i} 'type' must be a string")
                    elif ref["type"] not in VALID_REFERENCE_TYPES:
                        result.add_warning(
                            f"Unknown reference type: '{ref['type']}'. "
                            f"Valid types: {', '.join(VALID_REFERENCE_TYPES)}"
                        )

        return result

    def validate_category_fields(self, data: dict[str, Any]) -> ValidationResult:
        """
        Validate a category entry's field formats.

        Args:
            data: Dictionary containing category data

        Returns:
            ValidationResult with validation status and any errors/warnings
        """
        result = ValidationResult(is_valid=True)

        if not isinstance(data, dict):
            result.add_error(f"Category entry must be a mapping, got {type(data).__name__}")
            return result

        allowed_fields = set(self.REQUIRED_CATEGORY_FIELDS + self.OPTIONAL_CATEGORY_FIELDS)
        unknown_fields = sorted(
            field_name for field_name in data if field_name not in allowed_fields
        )
        for field_name in unknown_fields:
            result.add_error(f"Unknown field: '{field_name}'")

        for field_name in self.REQUIRED_CATEGORY_FIELDS:
            if field_name not in data:
                result.add_error(f"Missing required field: '{field_name}'")
                continue

            value = data[field_name]
            if not isinstance(value, str):
                result.add_error(
                    f"Field '{field_name}' must be a string, got {type(value).__name__}"
                )
            elif not value.strip():
                result.add_error(f"Required field '{field_name}' is empty")

        if "description" in data and not isinstance(data["description"], str):
            result.add_error(
                f"Field 'description' must be a string, got {type(data['description']).__name__}"
            )

        if "subcategories" in data:
            if not isinstance(data["subcategories"], list):
                result.add_error("Field 'subcategories' must be a list")
            else:
                for i, sub in enumerate(data["subcategories"]):
                    if not isinstance(sub, dict):
                        result.add_error(
                            f"Subcategory {i} must be a mapping, got {type(sub).__name__}"
                        )
                        continue

                    sub_result = self.validate_category_fields(sub)
                    for error in sub_result.errors:
                        result.add_error(f"Subcategory {i}: {error}")
                    for warning in sub_result.warnings:
                        result.add_warning(f"Subcategory {i}: {warning}")

        return result

    def validate_yaml_file(self, file_path: str) -> tuple[ValidationResult, Any]:
        """
        Validate a YAML file and return parsed data.

        Args:
            file_path: Path to the YAML file

        Returns:
            Tuple of (ValidationResult, parsed data or None)
        """
        result = ValidationResult(is_valid=True)

        if not os.path.exists(file_path):
            result.add_error(f"File not found: {file_path}")
            return result, None

        try:
            with open(file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            result.add_error(f"YAML parsing error: {str(e)}")
            return result, None
        except UnicodeDecodeError as e:
            result.add_error(f"Encoding error (use UTF-8): {str(e)}")
            return result, None

        if data is None:
            result.add_error("Empty YAML file")
            return result, None

        return result, data

    # =========================================================================
    # Backward compatibility methods
    # =========================================================================

    def validate_algorithm(self, data: dict[str, Any]) -> ValidationResult:
        """Backward compatible method - delegates to validate_algorithm_fields."""
        return self.validate_algorithm_fields(data)

    def validate_category(self, data: dict[str, Any]) -> ValidationResult:
        """Backward compatible method - delegates to validate_category_fields."""
        return self.validate_category_fields(data)


class Validator(FieldValidator):
    """
    Full validator with category relationship tracking.
    Maintains backward compatibility with tests that expect stateful validation.
    """

    def __init__(self, valid_categories: Optional[list[str]] = None):
        """Initialize validator with optional list of valid category IDs."""
        super().__init__()
        self.valid_categories = valid_categories or []
        self.category_parents: dict[str, Optional[str]] = {}
        self._categories_loaded = valid_categories is not None

    def validate_algorithm(self, data: dict[str, Any]) -> ValidationResult:
        """
        Validate an algorithm entry with category reference checking.

        Args:
            data: Dictionary containing algorithm data

        Returns:
            ValidationResult with validation status and any errors/warnings
        """
        result = super().validate_algorithm(data)
        if not isinstance(data, dict):
            return result

        # Validate category references
        if self._categories_loaded and data.get("category") not in self.valid_categories:
            result.add_error(
                f"Invalid category: '{data.get('category')}'. "
                f"Valid categories: {', '.join(self.valid_categories)}"
            )

        subcategory = data.get("subcategory", "")
        if subcategory:
            if self._categories_loaded:
                if subcategory not in self.category_parents:
                    result.add_error(f"Invalid subcategory: '{subcategory}'")
                else:
                    parent_category = self.category_parents[subcategory]
                    if parent_category is None:
                        result.add_error(
                            f"Invalid subcategory: '{subcategory}' is a top-level category"
                        )
                    elif parent_category != data.get("category"):
                        result.add_error(
                            f"Subcategory '{subcategory}' does not belong to "
                            f"category '{data.get('category')}'"
                        )

        return result

    def validate_algorithms_file(
        self, file_path: str, parsed: dict[str, Any] | None = None
    ) -> ValidationResult:
        """
        Validate an algorithms YAML file.

        Args:
            file_path: Path to the algorithms YAML file
            parsed: 可选输出参数；成功解析时写入文件内容，供调用方复用，
                避免对同一文件重复 open + safe_load。

        Returns:
            ValidationResult with validation status and any errors/warnings
        """
        result, data = self.validate_yaml_file(file_path)
        if isinstance(parsed, dict) and isinstance(data, dict):
            parsed.clear()
            parsed.update(data)
        if not result.is_valid:
            return result

        if not isinstance(data, dict):
            result.add_error(
                f"Root of algorithms file must be a mapping, got {type(data).__name__}"
            )
            return result

        if "algorithms" not in data:
            result.add_error("Missing 'algorithms' key in file")
            return result

        if not isinstance(data["algorithms"], list):
            result.add_error("'algorithms' must be a list")
            return result

        seen_ids = set()
        for i, algo in enumerate(data["algorithms"]):
            if not isinstance(algo, dict):
                result.add_error(
                    f"Algorithm {i} entry must be a mapping, got {type(algo).__name__}"
                )
                continue

            algo_result = self.validate_algorithm(algo)
            for error in algo_result.errors:
                result.add_error(f"Algorithm {i} ({algo.get('id', 'unknown')}): {error}")
            for warning in algo_result.warnings:
                result.add_warning(f"Algorithm {i} ({algo.get('id', 'unknown')}): {warning}")

            algo_id = algo.get("id")
            if algo_id:
                if algo_id in seen_ids:
                    result.add_error(f"Duplicate algorithm ID: '{algo_id}'")
                seen_ids.add(algo_id)

        return result

    def validate_categories_file(self, file_path: str) -> ValidationResult:
        """
        Validate a categories YAML file.

        Args:
            file_path: Path to the categories YAML file

        Returns:
            ValidationResult with validation status and any errors/warnings

        Note:
            On successful validation, populates self.valid_categories and
            self.category_parents for use in subsequent algorithm validation.
        """
        result, data = self.validate_yaml_file(file_path)
        if not result.is_valid:
            return result

        if not isinstance(data, dict):
            result.add_error(
                f"Root of categories file must be a mapping, got {type(data).__name__}"
            )
            return result

        if "categories" not in data:
            result.add_error("Missing 'categories' key in file")
            return result

        if not isinstance(data["categories"], list):
            result.add_error("'categories' must be a list")
            return result

        self._categories_loaded = True
        self.valid_categories = []
        self.category_parents = {}

        for i, cat in enumerate(data["categories"]):
            if not isinstance(cat, dict):
                result.add_error(f"Category {i} entry must be a mapping, got {type(cat).__name__}")
                continue

            cat_result = self.validate_category(cat)
            for error in cat_result.errors:
                result.add_error(f"Category {i} ({cat.get('id', 'unknown')}): {error}")
            for warning in cat_result.warnings:
                result.add_warning(f"Category {i} ({cat.get('id', 'unknown')}): {warning}")

        relationships = self._collect_category_relationships(data["categories"], result)
        if result.is_valid:
            self.category_parents = relationships
            self.valid_categories = list(relationships.keys())

        return result

    def validate_all(self, data_dir: str) -> ValidationResult:
        """
        Validate all data files in a directory.

        Args:
            data_dir: Path to the data directory

        Returns:
            ValidationResult with validation status and any errors/warnings
        """
        result = ValidationResult(is_valid=True)
        self._categories_loaded = False
        self.valid_categories = []
        self.category_parents = {}

        categories_path = os.path.join(data_dir, "categories.yaml")
        if os.path.exists(categories_path):
            cat_result = self.validate_categories_file(categories_path)
            result.merge(cat_result)

        algorithms_dir = os.path.join(data_dir, "algorithms")
        seen_ids: dict[str, str] = {}
        if os.path.exists(algorithms_dir):
            for filename in sorted(os.listdir(algorithms_dir)):
                if filename.endswith(".yaml") or filename.endswith(".yml"):
                    file_path = os.path.join(algorithms_dir, filename)
                    parsed: dict[str, Any] = {}
                    algo_result = self.validate_algorithms_file(file_path, parsed)
                    for error in algo_result.errors:
                        result.add_error(f"{filename}: {error}")
                    for warning in algo_result.warnings:
                        result.add_warning(f"{filename}: {warning}")

                    if isinstance(parsed.get("algorithms"), list):
                        for algo in parsed["algorithms"]:
                            if not isinstance(algo, dict):
                                continue
                            algo_id = algo.get("id")
                            if not algo_id:
                                continue
                            if algo_id in seen_ids:
                                result.add_error(
                                    f"Duplicate algorithm ID across files: '{algo_id}' "
                                    f"({seen_ids[algo_id]}, {filename})"
                                )
                            else:
                                seen_ids[algo_id] = filename

        return result

    def _collect_category_relationships(
        self,
        categories: list[dict[str, Any]],
        result: ValidationResult,
        parent_id: Optional[str] = None,
        relationships: Optional[dict[str, Optional[str]]] = None,
    ) -> dict[str, Optional[str]]:
        """Collect category IDs and their parent category IDs."""
        if relationships is None:
            relationships = {}

        for category in categories:
            if not isinstance(category, dict):
                continue

            category_id = category.get("id")
            if not category_id:
                continue

            if category_id in relationships:
                result.add_error(f"Duplicate category ID: '{category_id}'")
                continue

            relationships[category_id] = parent_id
            subcategories = category.get("subcategories", [])
            if isinstance(subcategories, list):
                self._collect_category_relationships(
                    subcategories,
                    result,
                    parent_id=category_id,
                    relationships=relationships,
                )

        return relationships
