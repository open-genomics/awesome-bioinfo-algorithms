"""
Category Manager for Awesome Bioinformatics Algorithms.
Manages algorithm categories and subcategories.
"""

import os
from dataclasses import dataclass, field
from typing import Optional

import yaml

from .schema import Category
from .validate import ValidationResult


@dataclass
class CategoryRelationships:
    """Stores category/subcategory relationships for validation."""

    valid_categories: list[str] = field(default_factory=list)
    category_parents: dict[str, Optional[str]] = field(default_factory=dict)


class CategoryManager:
    """Manages algorithm categories loaded from YAML files."""

    def __init__(self):
        self._categories: list[Category] = []
        self._category_map: dict[str, Category] = {}
        self._relationships = CategoryRelationships()
        self._loaded = False

    def load_categories(self, path: str) -> list[Category]:
        """
        Load categories from a YAML file.

        Args:
            path: Path to the categories YAML file

        Returns:
            List of Category objects
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Categories file not found: {path}")

        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)

        self._categories = []
        self._category_map = {}
        self._relationships = CategoryRelationships()
        self._loaded = True

        if not data or "categories" not in data:
            return []

        for cat_data in data["categories"]:
            category = Category.from_dict(cat_data)
            self._categories.append(category)
            self._register_category(category)

        # Build relationships after all categories are loaded
        self._build_relationships()

        return self._categories

    def _register_category(self, category: Category):
        """Register a category and its subcategories in the lookup map."""
        self._category_map[category.id] = category
        for sub in category.subcategories:
            self._register_category(sub)

    def _build_relationships(self):
        """Build category/subcategory relationships for validation."""
        self._relationships.valid_categories = list(self._category_map.keys())
        self._relationships.category_parents = {}

        def collect_parents(categories: list[Category], parent_id: Optional[str] = None):
            for cat in categories:
                self._relationships.category_parents[cat.id] = parent_id
                if cat.subcategories:
                    collect_parents(cat.subcategories, parent_id=cat.id)

        collect_parents(self._categories)

    def get_category(self, category_id: str) -> Optional[Category]:
        """
        Get a category by its ID.

        Args:
            category_id: The category ID to look up

        Returns:
            Category object or None if not found
        """
        return self._category_map.get(category_id)

    def list_all_categories(self) -> list[Category]:
        """
        List all top-level categories.

        Returns:
            List of top-level Category objects
        """
        return self._categories.copy()

    def list_all_category_ids(self) -> list[str]:
        """
        List all category IDs including subcategories.

        Returns:
            List of all category IDs
        """
        return list(self._category_map.keys())

    def get_subcategories(self, category_id: str) -> list[Category]:
        """
        Get subcategories of a category.

        Args:
            category_id: The parent category ID

        Returns:
            List of subcategory objects
        """
        category = self.get_category(category_id)
        if category:
            return category.subcategories.copy()
        return []

    def get_parent_category(self, category_id: str) -> Optional[Category]:
        """
        Get the parent category of a subcategory.

        Args:
            category_id: The subcategory ID

        Returns:
            Parent Category object or None
        """
        category = self.get_category(category_id)
        if category and category.parent_id:
            return self.get_category(category.parent_id)
        return None

    def category_exists(self, category_id: str) -> bool:
        """Check if a category ID exists."""
        return category_id in self._category_map

    def to_dict(self) -> dict:
        """Convert all categories to dictionary for serialization."""
        return {"categories": [cat.to_dict() for cat in self._categories]}

    def from_categories(self, categories: list[Category]) -> None:
        """Load categories from a list of Category objects."""
        self._categories = categories
        self._category_map = {}
        self._relationships = CategoryRelationships()
        self._loaded = True
        for cat in categories:
            self._register_category(cat)
        self._build_relationships()

    # =========================================================================
    # Category Validation Methods (moved from Validator)
    # =========================================================================

    def get_valid_categories(self) -> list[str]:
        """Get all valid category IDs including subcategories."""
        return self._relationships.valid_categories.copy()

    def get_category_parents(self) -> dict[str, Optional[str]]:
        """Get mapping of category_id -> parent_category_id."""
        return self._relationships.category_parents.copy()

    def validate_category_reference(self, category: str, subcategory: str = "") -> ValidationResult:
        """
        Validate that a category/subcategory reference is valid.

        Args:
            category: The category ID to validate
            subcategory: The subcategory ID (optional)

        Returns:
            ValidationResult with any errors
        """
        result = ValidationResult(is_valid=True)

        # Validate category exists
        if self._loaded and category not in self._relationships.valid_categories:
            result.add_error(
                f"Invalid category: '{category}'. "
                f"Valid categories: {', '.join(sorted(self._relationships.valid_categories))}"
            )
            return result

        # Validate subcategory if provided
        if subcategory:
            if subcategory not in self._relationships.category_parents:
                result.add_error(f"Invalid subcategory: '{subcategory}'")
            else:
                parent_category = self._relationships.category_parents[subcategory]
                if parent_category is None:
                    result.add_error(
                        f"Invalid subcategory: '{subcategory}' is a top-level category"
                    )
                elif parent_category != category:
                    result.add_error(
                        f"Subcategory '{subcategory}' does not belong to category '{category}'"
                    )

        return result
