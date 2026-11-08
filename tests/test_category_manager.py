"""
Property-based tests for CategoryManager.
Feature: awesome-bioinfo-algorithms, Property 2: Subcategory Hierarchy Preservation
"""

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from awesome_bioinfo.category_manager import CategoryManager
from awesome_bioinfo.schema import Category


def build_category_with_subcategory() -> Category:
    """Build a representative category tree for category manager tests."""
    return Category(
        id="sequence-alignment",
        name="序列比对",
        name_en="Sequence Alignment",
        description="用于比较和对齐生物序列的算法",
        subcategories=[
            Category(
                id="pairwise",
                name="双序列比对",
                name_en="Pairwise Alignment",
                description="两条序列之间的比对算法",
                subcategories=[],
                parent_id="sequence-alignment",
            )
        ],
        parent_id=None,
    )


def write_categories_yaml(path, content: str) -> None:
    """Write a categories YAML fixture."""
    path.write_text(content, encoding="utf-8")


# Strategies for generating test data
valid_id = st.text(
    alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyz0123456789"), min_size=1, max_size=20
).filter(lambda x: x and x[0].isalpha())

valid_name = st.text(min_size=1, max_size=50).filter(lambda x: x.strip())


@st.composite
def subcategory_strategy(draw, parent_id: str):
    """Generate a subcategory with reference to parent."""
    return Category(
        id=draw(valid_id),
        name=draw(valid_name),
        name_en=draw(valid_name),
        description=draw(st.text(min_size=0, max_size=100)),
        subcategories=[],
        parent_id=parent_id,
    )


@st.composite
def categories_list_strategy(draw):
    """Generate a list of categories with subcategories, ensuring unique IDs."""
    num_categories = draw(st.integers(min_value=1, max_value=5))
    categories = []
    used_ids = set()
    counter = [0]  # Use list to allow mutation in nested function

    def get_unique_id():
        """Generate a unique ID."""
        base = draw(valid_id)
        while base in used_ids:
            counter[0] += 1
            base = f"{base}{counter[0]}"
        used_ids.add(base)
        return base

    for _ in range(num_categories):
        cat_id = get_unique_id()
        num_subcategories = draw(st.integers(min_value=0, max_value=3))

        subcategories = []
        for _ in range(num_subcategories):
            sub_id = get_unique_id()
            sub = Category(
                id=sub_id,
                name=draw(valid_name),
                name_en=draw(valid_name),
                description=draw(st.text(min_size=0, max_size=100)),
                subcategories=[],
                parent_id=cat_id,  # Correctly set parent_id to current category
            )
            subcategories.append(sub)

        cat = Category(
            id=cat_id,
            name=draw(valid_name),
            name_en=draw(valid_name),
            description=draw(st.text(min_size=0, max_size=100)),
            subcategories=subcategories,
            parent_id=None,
        )
        categories.append(cat)

    return categories


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(categories=categories_list_strategy())
def test_property_2_subcategory_hierarchy_preservation(categories):
    """
    Feature: awesome-bioinfo-algorithms, Property 2: Subcategory Hierarchy Preservation

    For any category with subcategories, retrieving the category SHALL return
    all its subcategories, and each subcategory SHALL correctly reference its parent category.

    Validates: Requirements 1.3
    """
    manager = CategoryManager()
    manager.from_categories(categories)

    for category in categories:
        # Retrieve the category
        retrieved = manager.get_category(category.id)
        assert retrieved is not None, f"Category '{category.id}' should be retrievable"

        # Verify all subcategories are present
        assert len(retrieved.subcategories) == len(category.subcategories), (
            f"Category '{category.id}' should have {len(category.subcategories)} subcategories"
        )

        # Verify each subcategory references the parent
        for sub in retrieved.subcategories:
            assert sub.parent_id == category.id, (
                f"Subcategory '{sub.id}' should reference parent '{category.id}'"
            )

            # Verify subcategory is retrievable
            retrieved_sub = manager.get_category(sub.id)
            assert retrieved_sub is not None, f"Subcategory '{sub.id}' should be retrievable"

            # Verify parent lookup works
            parent = manager.get_parent_category(sub.id)
            assert parent is not None, f"Parent of subcategory '{sub.id}' should be retrievable"
            assert parent.id == category.id, f"Parent of '{sub.id}' should be '{category.id}'"


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(categories=categories_list_strategy())
def test_all_category_ids_listed(categories):
    """Test that all category IDs (including subcategories) are listed."""
    manager = CategoryManager()
    manager.from_categories(categories)

    all_ids = manager.list_all_category_ids()

    for category in categories:
        assert category.id in all_ids, f"Category '{category.id}' should be in ID list"
        for sub in category.subcategories:
            assert sub.id in all_ids, f"Subcategory '{sub.id}' should be in ID list"


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(categories=categories_list_strategy())
def test_category_exists_check(categories):
    """Test that category_exists correctly identifies existing categories."""
    manager = CategoryManager()
    manager.from_categories(categories)

    for category in categories:
        assert manager.category_exists(category.id), f"Category '{category.id}' should exist"
        for sub in category.subcategories:
            assert manager.category_exists(sub.id), f"Subcategory '{sub.id}' should exist"

    # Non-existent category
    assert not manager.category_exists("nonexistent-category-xyz")


def test_load_categories_raises_for_missing_file(tmp_path):
    """Loading a missing categories file should raise FileNotFoundError."""
    manager = CategoryManager()

    with pytest.raises(FileNotFoundError):
        manager.load_categories(str(tmp_path / "missing.yaml"))


def test_load_categories_returns_empty_list_for_missing_categories_key(tmp_path):
    """Files without a categories key should load as an empty category set."""
    file_path = tmp_path / "categories.yaml"
    write_categories_yaml(file_path, "metadata: {}\n")

    manager = CategoryManager()
    loaded = manager.load_categories(str(file_path))

    assert loaded == []
    assert manager.list_all_categories() == []
    assert manager.list_all_category_ids() == []


def test_load_categories_loads_nested_categories_from_yaml(tmp_path):
    """YAML loading should populate both top-level categories and subcategory lookups."""
    file_path = tmp_path / "categories.yaml"
    write_categories_yaml(
        file_path,
        """categories:
  - id: sequence-alignment
    name: 序列比对
    name_en: Sequence Alignment
    description: 用于比较和对齐生物序列的算法
    subcategories:
      - id: pairwise
        name: 双序列比对
        name_en: Pairwise Alignment
        description: 两条序列之间的比对算法
""",
    )

    manager = CategoryManager()
    loaded = manager.load_categories(str(file_path))

    assert len(loaded) == 1
    assert loaded[0].id == "sequence-alignment"
    assert manager.get_category("pairwise") is not None
    assert manager.get_parent_category("pairwise").id == "sequence-alignment"


def test_get_subcategories_returns_copy_and_missing_parent_returns_empty():
    """Subcategory lookup should return a copy and tolerate unknown IDs."""
    manager = CategoryManager()
    manager.from_categories([build_category_with_subcategory()])

    subcategories = manager.get_subcategories("sequence-alignment")
    assert len(subcategories) == 1

    subcategories.clear()
    assert len(manager.get_subcategories("sequence-alignment")) == 1
    assert manager.get_subcategories("missing-category") == []


def test_get_parent_category_returns_none_for_top_level_and_missing():
    """Parent lookup should return None for top-level and missing category IDs."""
    manager = CategoryManager()
    manager.from_categories([build_category_with_subcategory()])

    assert manager.get_parent_category("sequence-alignment") is None
    assert manager.get_parent_category("missing-category") is None


def test_list_all_categories_returns_copy():
    """Top-level category listing should return a defensive copy."""
    manager = CategoryManager()
    manager.from_categories([build_category_with_subcategory()])

    categories = manager.list_all_categories()
    categories.clear()

    assert len(manager.list_all_categories()) == 1


def test_to_dict_serializes_loaded_categories():
    """to_dict should round-trip top-level categories with nested subcategories."""
    category = build_category_with_subcategory()
    manager = CategoryManager()
    manager.from_categories([category])

    exported = manager.to_dict()

    assert exported["categories"][0]["id"] == "sequence-alignment"
    assert exported["categories"][0]["subcategories"][0]["id"] == "pairwise"


def test_from_categories_replaces_previous_state():
    """Loading a new category list should replace previous manager state."""
    manager = CategoryManager()
    manager.from_categories([build_category_with_subcategory()])

    replacement = Category(
        id="assembly",
        name="序列组装",
        name_en="Sequence Assembly",
        description="从短读段重建完整序列的算法",
        subcategories=[],
        parent_id=None,
    )
    manager.from_categories([replacement])

    assert manager.get_category("sequence-alignment") is None
    assert manager.get_category("assembly") is not None
    assert manager.list_all_category_ids() == ["assembly"]


def test_load_categories_resets_previous_state_on_empty_input(tmp_path):
    """Loading an empty categories document should clear prior in-memory state."""
    manager = CategoryManager()
    manager.from_categories([build_category_with_subcategory()])

    file_path = tmp_path / "categories.yaml"
    write_categories_yaml(file_path, "categories: []\n")
    loaded = manager.load_categories(str(file_path))

    assert loaded == []
    assert manager.list_all_categories() == []
    assert manager.list_all_category_ids() == []


def test_load_categories_accepts_empty_yaml_document(tmp_path):
    """An empty YAML document should produce an empty category list."""
    file_path = tmp_path / "categories.yaml"
    write_categories_yaml(file_path, "")

    manager = CategoryManager()
    loaded = manager.load_categories(str(file_path))

    assert loaded == []
    assert manager.list_all_categories() == []
    assert manager.list_all_category_ids() == []


@pytest.mark.parametrize("content", ["metadata: {}\n", ""])
def test_load_categories_resets_previous_state_without_categories_key(tmp_path, content):
    """Loading a file without a categories list should clear prior in-memory state."""
    manager = CategoryManager()
    manager.from_categories([build_category_with_subcategory()])

    file_path = tmp_path / "categories.yaml"
    write_categories_yaml(file_path, content)
    loaded = manager.load_categories(str(file_path))

    assert loaded == []
    assert manager.list_all_categories() == []
    assert manager.list_all_category_ids() == []


def test_validate_category_reference_rejects_unknown_id_after_empty_categories(tmp_path):
    """A loaded empty category table should reject any category reference."""
    file_path = tmp_path / "categories.yaml"
    write_categories_yaml(file_path, "categories: []\n")
    manager = CategoryManager()
    manager.load_categories(str(file_path))

    result = manager.validate_category_reference("nonexistent-category")

    assert not result.is_valid
    assert any("Invalid category: 'nonexistent-category'" in error for error in result.errors)
