"""
Property-based tests for Validator class.
Feature: awesome-bioinfo-algorithms
"""

from pathlib import Path

import pytest
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st

from awesome_bioinfo.schema import AlgorithmEntry
from awesome_bioinfo.validate import Validator

# Strategies for generating test data
valid_id = st.text(
    alphabet=st.sampled_from("abcdefghijklmnopqrstuvwxyz-_0123456789"), min_size=1, max_size=50
).filter(lambda x: x and not x.startswith("-"))

valid_name = st.text(min_size=1, max_size=100).filter(lambda x: x.strip())

# Description between 50-500 characters
valid_description = st.text(min_size=50, max_size=500).filter(lambda x: 50 <= len(x.strip()) <= 500)

# Description that's too short
short_description = st.text(min_size=0, max_size=49)

# Description that's too long
long_description = st.text(min_size=501, max_size=600)


@st.composite
def valid_algorithm_data(draw):
    """Generate valid algorithm data dictionary."""
    return {
        "id": draw(valid_id),
        "name": draw(valid_name),
        "description": draw(valid_description),
        "purpose": draw(st.text(min_size=5, max_size=100).filter(lambda x: x.strip())),
        "time_complexity": draw(st.sampled_from(["O(n)", "O(n^2)", "O(mn)", "O(n log n)", "O(1)"])),
        "category": draw(valid_id),
    }


@st.composite
def algorithm_data_missing_field(draw, field_to_remove: str):
    """Generate algorithm data with a specific required field missing."""
    data = draw(valid_algorithm_data())
    del data[field_to_remove]
    return data


@st.composite
def algorithm_data_empty_field(draw, field_to_empty: str):
    """Generate algorithm data with a specific required field empty."""
    data = draw(valid_algorithm_data())
    data[field_to_empty] = ""
    return data


# Property 3: Required Fields Validation
@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    field_name=st.sampled_from(
        ["id", "name", "description", "purpose", "time_complexity", "category"]
    )
)
def test_property_3_missing_required_field(field_name: str):
    """
    Feature: awesome-bioinfo-algorithms, Property 3: Required Fields Validation

    For any algorithm entry submission, if any required field is missing,
    the validator SHALL reject the entry and return an error.

    Validates: Requirements 1.4, 2.1, 4.2
    """
    validator = Validator()

    # Create valid data then remove the field
    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * 60,  # Valid length
        "purpose": "Testing",
        "time_complexity": "O(n)",
        "category": "test-category",
    }
    del data[field_name]

    result = validator.validate_algorithm(data)

    assert not result.is_valid, f"Should reject when '{field_name}' is missing"
    assert any(field_name in error for error in result.errors), (
        f"Error should mention missing field '{field_name}'"
    )


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    field_name=st.sampled_from(
        ["id", "name", "description", "purpose", "time_complexity", "category"]
    )
)
def test_property_3_empty_required_field(field_name: str):
    """
    Feature: awesome-bioinfo-algorithms, Property 3: Required Fields Validation

    For any algorithm entry submission, if any required field is empty,
    the validator SHALL reject the entry and return an error.

    Validates: Requirements 1.4, 2.1, 4.2
    """
    validator = Validator()

    # Create valid data then empty the field
    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * 60,
        "purpose": "Testing",
        "time_complexity": "O(n)",
        "category": "test-category",
    }
    data[field_name] = ""

    result = validator.validate_algorithm(data)

    assert not result.is_valid, f"Should reject when '{field_name}' is empty"
    assert any(field_name in error for error in result.errors), (
        f"Error should mention empty field '{field_name}'"
    )


# Property 7: Validation Error Specificity
@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    missing_fields=st.lists(
        st.sampled_from(["id", "name", "description", "purpose", "time_complexity", "category"]),
        min_size=1,
        max_size=3,
        unique=True,
    )
)
def test_property_7_error_specificity_missing_fields(missing_fields):
    """
    Feature: awesome-bioinfo-algorithms, Property 7: Validation Error Specificity

    For any invalid algorithm entry, the validator SHALL return an error message
    that identifies the specific field issue.

    Validates: Requirements 4.4, 6.3
    """
    validator = Validator()

    # Create data with multiple missing fields
    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * 60,
        "purpose": "Testing",
        "time_complexity": "O(n)",
        "category": "test-category",
    }
    for field in missing_fields:
        del data[field]

    result = validator.validate_algorithm(data)

    assert not result.is_valid
    # Each missing field should be mentioned in errors
    for field in missing_fields:
        assert any(field in error for error in result.errors), (
            f"Error should specifically mention '{field}'"
        )


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(desc_length=st.integers(min_value=0, max_value=49))
def test_property_7_error_specificity_short_description(desc_length):
    """
    Feature: awesome-bioinfo-algorithms, Property 7: Validation Error Specificity

    For description that's too short, the validator SHALL return an error
    that identifies the length issue.

    Validates: Requirements 4.4, 6.3
    """
    validator = Validator()

    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * desc_length,
        "purpose": "Testing",
        "time_complexity": "O(n)",
        "category": "test-category",
    }

    result = validator.validate_algorithm(data)

    if desc_length < 50:
        assert not result.is_valid
        assert any(
            "short" in error.lower() or "description" in error.lower() for error in result.errors
        ), "Error should mention description length issue"


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(desc_length=st.integers(min_value=501, max_value=600))
def test_property_7_error_specificity_long_description(desc_length):
    """
    Feature: awesome-bioinfo-algorithms, Property 7: Validation Error Specificity

    For description that's too long, the validator SHALL return an error
    that identifies the length issue.

    Validates: Requirements 4.4, 6.3
    """
    validator = Validator()

    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * desc_length,
        "purpose": "Testing",
        "time_complexity": "O(n)",
        "category": "test-category",
    }

    result = validator.validate_algorithm(data)

    assert not result.is_valid
    assert any(
        "long" in error.lower() or "description" in error.lower() for error in result.errors
    ), "Error should mention description length issue"


# Property 10: Data Format Validation
@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(data=valid_algorithm_data())
def test_property_10_valid_data_passes(data):
    """
    Feature: awesome-bioinfo-algorithms, Property 10: Data Format Validation

    For any valid algorithm data, the validator SHALL accept it.

    Validates: Requirements 6.2
    """
    validator = Validator()
    result = validator.validate_algorithm(data)

    # Valid data should pass (unless description length is wrong)
    desc_len = len(data["description"].strip())
    if 50 <= desc_len <= 500:
        assert result.is_valid, f"Valid data should pass validation. Errors: {result.errors}"


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(
    tags_value=st.one_of(
        st.text(min_size=1, max_size=20),  # String instead of list
        st.integers(),  # Integer instead of list
        st.dictionaries(
            st.text(max_size=5), st.text(max_size=5), max_size=2
        ),  # Dict instead of list
    )
)
def test_property_10_invalid_tags_format(tags_value):
    """
    Feature: awesome-bioinfo-algorithms, Property 10: Data Format Validation

    For any data with invalid tags format (not a list), the validator SHALL report the violation.

    Validates: Requirements 6.2
    """
    validator = Validator()

    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * 60,
        "purpose": "Testing",
        "time_complexity": "O(n)",
        "category": "test-category",
        "tags": tags_value,
    }

    result = validator.validate_algorithm(data)

    assert not result.is_valid
    assert any("tags" in error.lower() for error in result.errors), (
        "Error should mention 'tags' field"
    )


def build_valid_category(**overrides):
    """Build a valid category payload for validator tests."""
    data = {
        "id": "test-cat",
        "name": "测试分类",
        "name_en": "Test Category",
    }
    data.update(overrides)
    return data


@settings(max_examples=100, suppress_health_check=[HealthCheck.filter_too_much])
@given(field_name=st.sampled_from(["id", "name", "name_en"]))
def test_category_missing_required_field(field_name: str):
    """Test that missing required category fields are detected."""
    validator = Validator()

    data = {
        "id": "test-cat",
        "name": "测试分类",
        "name_en": "Test Category",
    }
    del data[field_name]

    result = validator.validate_category(data)

    assert not result.is_valid
    assert any(field_name in error for error in result.errors)


def test_unknown_category_field_is_rejected():
    """Unexpected category fields should be rejected to catch typos."""
    validator = Validator()

    result = validator.validate_category(build_valid_category(display_name="Alias"))

    assert not result.is_valid
    assert "Unknown field: 'display_name'" in result.errors


@pytest.mark.parametrize("field_name", ["id", "name", "name_en"])
def test_category_required_string_field_requires_string_type(field_name: str):
    """Required category fields should reject non-string values."""
    validator = Validator()

    result = validator.validate_category(build_valid_category(**{field_name: 123}))

    assert not result.is_valid
    assert any(field_name in error and "must be a string" in error for error in result.errors)


@pytest.mark.parametrize("field_name", ["id", "name", "name_en"])
def test_category_required_whitespace_only_string_is_rejected(field_name: str):
    """Whitespace-only required category fields should count as empty."""
    validator = Validator()

    result = validator.validate_category(build_valid_category(**{field_name: "   "}))

    assert not result.is_valid
    assert any(field_name in error and "empty" in error.lower() for error in result.errors)


def test_category_description_requires_string_type():
    """Optional category description should be a string when present."""
    validator = Validator()

    result = validator.validate_category(build_valid_category(description=["not-a-string"]))

    assert not result.is_valid
    assert any("Field 'description' must be a string" in error for error in result.errors)


def test_subcategory_items_must_be_mappings():
    """Subcategory lists should only contain mapping objects."""
    validator = Validator()

    result = validator.validate_category(build_valid_category(subcategories=["pairwise"]))

    assert not result.is_valid
    assert any("must be a mapping" in error for error in result.errors)

    """Test that subcategory validation enforces parent-child relationships."""
    validator = Validator(
        valid_categories=["sequence-alignment", "assembly", "pairwise"],
    )
    validator.category_parents = {
        "sequence-alignment": None,
        "assembly": None,
        "pairwise": "sequence-alignment",
    }

    valid_data = {
        "id": "smith-waterman",
        "name": "Smith-Waterman",
        "description": "A" * 60,
        "purpose": "Local alignment",
        "time_complexity": "O(mn)",
        "category": "sequence-alignment",
        "subcategory": "pairwise",
    }
    assert validator.validate_algorithm(valid_data).is_valid

    wrong_parent = dict(valid_data, category="assembly")
    wrong_parent_result = validator.validate_algorithm(wrong_parent)
    assert not wrong_parent_result.is_valid
    assert any("does not belong" in error for error in wrong_parent_result.errors)

    invalid_subcategory = dict(valid_data, subcategory="multiple")
    invalid_subcategory_result = validator.validate_algorithm(invalid_subcategory)
    assert not invalid_subcategory_result.is_valid
    assert any("Invalid subcategory" in error for error in invalid_subcategory_result.errors)


def build_valid_algorithm(**overrides):
    """Build a valid algorithm payload for validator tests."""
    data = {
        "id": "test-algo",
        "name": "Test Algorithm",
        "description": "A" * 60,
        "purpose": "Testing validator behavior",
        "time_complexity": "O(n)",
        "category": "test-category",
    }
    data.update(overrides)
    return data


def test_unknown_algorithm_field_is_rejected():
    """Unexpected fields should be rejected to catch typos."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(time_compexity="O(n)"))

    assert not result.is_valid
    assert "Unknown field: 'time_compexity'" in result.errors


@pytest.mark.parametrize(
    "field_name", ["id", "name", "description", "purpose", "time_complexity", "category"]
)
def test_required_whitespace_only_string_is_rejected(field_name: str):
    """Whitespace-only required string fields should count as empty."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(**{field_name: "   "}))

    assert not result.is_valid
    assert any(field_name in error and "empty" in error.lower() for error in result.errors)


@pytest.mark.parametrize(
    "field_name", ["id", "name", "description", "purpose", "time_complexity", "category"]
)
def test_required_string_field_requires_string_type(field_name: str):
    """Required textual fields should reject non-string values."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(**{field_name: 123}))

    assert not result.is_valid
    assert any(field_name in error and "must be a string" in error for error in result.errors)


@pytest.mark.parametrize(
    "field_name", ["space_complexity", "subcategory", "paper_url", "implementation_url"]
)
def test_optional_string_field_requires_string_type(field_name: str):
    """Optional textual fields should reject non-string values when present."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(**{field_name: ["not-a-string"]}))

    assert not result.is_valid
    assert any(field_name in error and "must be a string" in error for error in result.errors)


@pytest.mark.parametrize("field_name", ["tags", "related_tools"])
def test_list_field_items_must_be_non_empty_strings(field_name: str):
    """List-valued metadata fields should only contain non-empty strings."""
    validator = Validator()

    non_string_result = validator.validate_algorithm(
        build_valid_algorithm(**{field_name: ["valid", 1]})
    )
    empty_string_result = validator.validate_algorithm(
        build_valid_algorithm(**{field_name: ["valid", "   "]})
    )

    assert not non_string_result.is_valid
    assert any(
        field_name in error and "must be a string" in error for error in non_string_result.errors
    )

    assert not empty_string_result.is_valid
    assert any(
        field_name in error and "cannot be empty" in error for error in empty_string_result.errors
    )


def test_non_integer_year_is_rejected():
    """Non-integer year values would break generate's year sort, so they fail validation."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(year="1998"))

    assert not result.is_valid
    assert any("Field 'year' must be an integer" in error for error in result.errors)


def test_empty_string_year_is_rejected():
    """An empty year string must not slip through to the generator's int sort."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(year=""))

    assert not result.is_valid
    assert any("Field 'year' must be an integer" in error for error in result.errors)


def test_invalid_url_remains_warning():
    """Invalid URL syntax should warn without failing validation."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(paper_url="not-a-url"))

    assert result.is_valid
    assert not result.errors
    assert any("Invalid URL format in 'paper_url'" in warning for warning in result.warnings)


def test_out_of_range_year_remains_warning():
    """Out-of-range years should remain warnings for compatibility."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(year=2045))

    assert result.is_valid
    assert not result.errors
    assert any("Suspicious year value: 2045" in warning for warning in result.warnings)


def test_validate_yaml_file_reports_missing_file(tmp_path: Path):
    """Missing YAML files should produce a file-not-found validation error."""
    validator = Validator()

    result, data = validator.validate_yaml_file(str(tmp_path / "missing.yaml"))

    assert not result.is_valid
    assert data is None
    assert any("File not found" in error for error in result.errors)


def test_validate_yaml_file_reports_empty_document(tmp_path: Path):
    """Empty YAML documents should be rejected."""
    file_path = tmp_path / "empty.yaml"
    file_path.write_text("", encoding="utf-8")
    validator = Validator()

    result, data = validator.validate_yaml_file(str(file_path))

    assert not result.is_valid
    assert data is None
    assert "Empty YAML file" in result.errors


def test_validate_yaml_file_reports_yaml_parse_error(tmp_path: Path):
    """Malformed YAML should be surfaced as a parsing error."""
    file_path = tmp_path / "broken.yaml"
    file_path.write_text("categories: [\n", encoding="utf-8")
    validator = Validator()

    result, data = validator.validate_yaml_file(str(file_path))

    assert not result.is_valid
    assert data is None
    assert any("YAML parsing error" in error for error in result.errors)


def test_validate_algorithms_file_requires_algorithms_key(tmp_path: Path):
    """Algorithm files without an algorithms key should fail validation."""
    file_path = tmp_path / "algorithms.yaml"
    file_path.write_text("metadata: {}\n", encoding="utf-8")
    validator = Validator()

    result = validator.validate_algorithms_file(str(file_path))

    assert not result.is_valid
    assert "Missing 'algorithms' key in file" in result.errors


def test_validate_algorithms_file_requires_algorithms_list(tmp_path: Path):
    """Algorithm files should require algorithms to be a list."""
    file_path = tmp_path / "algorithms.yaml"
    file_path.write_text("algorithms: {}\n", encoding="utf-8")
    validator = Validator()

    result = validator.validate_algorithms_file(str(file_path))

    assert not result.is_valid
    assert "'algorithms' must be a list" in result.errors


def test_validate_algorithms_file_reports_entry_warnings_and_duplicate_ids(tmp_path: Path):
    """Algorithm file validation should surface warnings and duplicate IDs within a file."""
    file_path = tmp_path / "algorithms.yaml"
    file_path.write_text(
        """algorithms:
  - id: shared-id
    name: Example One
    description: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    purpose: Example purpose
    time_complexity: O(n)
    category: sequence-alignment
    year: '1998'
  - id: shared-id
    name: Example Two
    description: BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
    purpose: Example purpose
    time_complexity: O(n)
    category: sequence-alignment
    paper_url: not-a-url
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_algorithms_file(str(file_path))

    assert not result.is_valid
    assert any("Duplicate algorithm ID: 'shared-id'" in error for error in result.errors)
    assert any("Field 'year' must be an integer" in error for error in result.errors)
    assert any("Invalid URL format in 'paper_url'" in warning for warning in result.warnings)


def test_validate_categories_file_requires_categories_key(tmp_path: Path):
    """Category files without a categories key should fail validation."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text("metadata: {}\n", encoding="utf-8")
    validator = Validator()

    result = validator.validate_categories_file(str(file_path))

    assert not result.is_valid
    assert "Missing 'categories' key in file" in result.errors


def test_validate_categories_file_requires_categories_list(tmp_path: Path):
    """Category files should require categories to be a list."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text("categories: {}\n", encoding="utf-8")
    validator = Validator()

    result = validator.validate_categories_file(str(file_path))

    assert not result.is_valid
    assert "'categories' must be a list" in result.errors


def test_validate_categories_file_collects_relationships(tmp_path: Path):
    """Valid category files should populate validator category relationship state."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text(
        """categories:
  - id: sequence-alignment
    name: 序列比对
    name_en: Sequence Alignment
    subcategories:
      - id: pairwise
        name: 双序列比对
        name_en: Pairwise Alignment
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_categories_file(str(file_path))

    assert result.is_valid
    assert validator.category_parents == {
        "sequence-alignment": None,
        "pairwise": "sequence-alignment",
    }
    assert set(validator.valid_categories) == {"sequence-alignment", "pairwise"}


def test_validate_categories_file_reports_duplicate_category_ids(tmp_path: Path):
    """Duplicate category IDs should be rejected while preserving category-state reset."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text(
        """categories:
  - id: duplicated
    name: One
    name_en: One
  - id: duplicated
    name: Two
    name_en: Two
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_categories_file(str(file_path))

    assert not result.is_valid
    assert any("Duplicate category ID: 'duplicated'" in error for error in result.errors)
    assert validator.category_parents == {}
    assert validator.valid_categories == []


def test_validate_algorithm_skips_category_check_when_categories_not_loaded():
    """Field-only validation should keep accepting arbitrary categories before loading."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(category="anything"))

    assert result.is_valid


def test_validate_algorithm_checks_references_after_empty_categories_file(tmp_path: Path):
    """A loaded but empty category table must still reject unknown references."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text("categories: []\n", encoding="utf-8")
    validator = Validator()

    assert validator.validate_categories_file(str(file_path)).is_valid
    result = validator.validate_algorithm(
        build_valid_algorithm(category="nonexistent-category", subcategory="nonexistent-sub")
    )

    assert not result.is_valid
    assert any("Invalid category: 'nonexistent-category'" in error for error in result.errors)
    assert any("Invalid subcategory: 'nonexistent-sub'" in error for error in result.errors)


def test_validate_all_rejects_references_when_categories_file_is_empty(tmp_path: Path):
    """validate_all should not skip reference checks for an empty category table."""
    data_dir = tmp_path / "data"
    algorithms_dir = data_dir / "algorithms"
    algorithms_dir.mkdir(parents=True)
    (data_dir / "categories.yaml").write_text("categories: []\n", encoding="utf-8")
    (algorithms_dir / "entries.yaml").write_text(
        """algorithms:
  - id: ghost-algorithm
    name: Ghost Algorithm
    description: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    purpose: Example purpose
    time_complexity: O(n)
    category: nonexistent-category
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_all(str(data_dir))

    assert not result.is_valid
    assert any("Invalid category: 'nonexistent-category'" in error for error in result.errors)


def test_collect_category_relationships_skips_categories_without_ids():
    """Relationship collection should ignore category objects missing ids."""
    validator = Validator()
    result = validator.validate_category(build_valid_category())

    relationships = validator._collect_category_relationships(
        [
            {"name": "Missing ID", "name_en": "Missing ID"},
            {"id": "sequence-alignment", "name": "序列比对", "name_en": "Sequence Alignment"},
        ],
        result,
    )

    assert relationships == {"sequence-alignment": None}


def test_validate_all_merges_category_and_algorithm_errors(tmp_path: Path):
    """validate_all should aggregate errors and warnings across category and algorithm files."""
    data_dir = tmp_path / "data"
    algorithms_dir = data_dir / "algorithms"
    algorithms_dir.mkdir(parents=True)

    (data_dir / "categories.yaml").write_text(
        """categories:
  - id: duplicated
    name: One
    name_en: One
  - id: duplicated
    name: Two
    name_en: Two
""",
        encoding="utf-8",
    )
    (algorithms_dir / "entries.yaml").write_text(
        """algorithms:
  - id: repeated
    name: Example One
    description: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    purpose: Example purpose
    time_complexity: O(n)
    category: duplicated
    paper_url: not-a-url
  - id: repeated
    name: Example Two
    description: BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB
    purpose: Example purpose
    time_complexity: O(n)
    category: duplicated
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_all(str(data_dir))

    assert not result.is_valid
    assert any("Duplicate category ID: 'duplicated'" in error for error in result.errors)
    assert any(
        "entries.yaml: Duplicate algorithm ID: 'repeated'" in error for error in result.errors
    )
    assert any("Invalid URL format in 'paper_url'" in warning for warning in result.warnings)


def test_validate_all_rejects_duplicate_ids_across_files(tmp_path: Path):
    """Test that duplicate algorithm IDs across files are rejected."""
    data_dir = tmp_path / "data"
    algorithms_dir = data_dir / "algorithms"
    algorithms_dir.mkdir(parents=True)

    (data_dir / "categories.yaml").write_text(
        """categories:
  - id: sequence-alignment
    name: Sequence Alignment
    name_en: Sequence Alignment
""",
        encoding="utf-8",
    )

    algorithm_body = """algorithms:
  - id: shared-id
    name: Example
    description: AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    purpose: Example purpose
    time_complexity: O(n)
    category: sequence-alignment
"""
    (algorithms_dir / "first.yaml").write_text(algorithm_body, encoding="utf-8")
    (algorithms_dir / "second.yaml").write_text(algorithm_body, encoding="utf-8")

    validator = Validator()
    result = validator.validate_all(str(data_dir))

    assert not result.is_valid
    assert any("Duplicate algorithm ID across files" in error for error in result.errors)


def test_validate_all_without_data_files_is_valid(tmp_path: Path):
    """Absent categories and algorithms directories should produce a clean valid result."""
    validator = Validator()

    result = validator.validate_all(str(tmp_path / "data"))

    assert result.is_valid
    assert result.errors == []
    assert result.warnings == []


# --- New field validation tests ---


def _make_algo(**overrides):
    """Helper to create a valid algorithm dict with optional overrides."""
    base = {
        "id": "test-algo",
        "name": "Test Algo",
        "description": "A" * 60,
        "purpose": "testing",
        "time_complexity": "O(n)",
        "category": "test-cat",
    }
    base.update(overrides)
    return base


def test_valid_difficulty_accepted():
    """Valid difficulty values should pass validation."""
    validator = Validator()
    for diff in ["beginner", "intermediate", "advanced"]:
        result = validator.validate_algorithm(_make_algo(difficulty=diff))
        assert result.is_valid, f"difficulty='{diff}' should be valid"


def test_invalid_difficulty_rejected():
    """Invalid difficulty value should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(difficulty="expert"))
    assert not result.is_valid
    assert any("Invalid difficulty" in e for e in result.errors)


def test_difficulty_requires_string_type():
    """Non-string difficulty should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(difficulty=123))
    assert not result.is_valid
    assert any("'difficulty' must be a string" in e for e in result.errors)


def test_valid_language_accepted():
    """Valid language list should pass validation."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(language=["Python", "C++"]))
    assert result.is_valid


def test_language_requires_list():
    """Non-list language should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(language="Python"))
    assert not result.is_valid
    assert any("'language' must be a list" in e for e in result.errors)


def test_language_items_must_be_strings():
    """Non-string language items should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(language=[123]))
    assert not result.is_valid
    assert any("must be a string" in e for e in result.errors)


def test_language_items_cannot_be_empty():
    """Empty language items should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(language=[""]))
    assert not result.is_valid
    assert any("cannot be empty" in e for e in result.errors)


def test_valid_references_accepted():
    """Valid references should pass validation."""
    validator = Validator()
    refs = [{"url": "https://example.com", "title": "Tutorial", "type": "tutorial"}]
    result = validator.validate_algorithm(_make_algo(references=refs))
    assert result.is_valid


def test_references_requires_list():
    """Non-list references should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(references="https://example.com"))
    assert not result.is_valid
    assert any("'references' must be a list" in e for e in result.errors)


def test_references_items_must_be_mappings():
    """Non-dict reference items should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(references=["https://example.com"]))
    assert not result.is_valid
    assert any("must be a mapping" in e for e in result.errors)


def test_references_must_have_url():
    """References without url should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(references=[{"title": "No URL"}]))
    assert not result.is_valid
    assert any("missing required 'url'" in e for e in result.errors)


def test_references_url_must_be_non_empty_string():
    """References with empty url should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(references=[{"url": ""}]))
    assert not result.is_valid
    assert any("'url' must be a non-empty string" in e for e in result.errors)


def test_references_invalid_url_produces_warning():
    """References with invalid URL format should produce a warning."""
    validator = Validator()
    result = validator.validate_algorithm(_make_algo(references=[{"url": "not-a-url"}]))
    assert result.is_valid
    assert any("Invalid URL in references" in w for w in result.warnings)


def test_references_unknown_type_produces_warning():
    """Unknown reference type should produce a warning."""
    validator = Validator()
    result = validator.validate_algorithm(
        _make_algo(references=[{"url": "https://example.com", "type": "podcast"}])
    )
    assert result.is_valid
    assert any("Unknown reference type" in w for w in result.warnings)


def test_references_title_must_be_non_empty_string():
    """Empty title in references should produce an error."""
    validator = Validator()
    result = validator.validate_algorithm(
        _make_algo(references=[{"url": "https://example.com", "title": ""}])
    )
    assert not result.is_valid
    assert any("'title' must be a non-empty string" in e for e in result.errors)


# --- Non-mapping input robustness ---


def test_validate_algorithm_fields_reports_non_mapping_entry():
    """Non-mapping algorithm entries should become validation errors, not exceptions."""
    validator = Validator()

    result = validator.validate_algorithm_fields(["not", "a", "mapping"])

    assert not result.is_valid
    assert any("must be a mapping" in error for error in result.errors)


def test_validate_category_fields_reports_non_mapping_entry():
    """Non-mapping category entries should become validation errors, not exceptions."""
    validator = Validator()

    result = validator.validate_category_fields("not-a-mapping")

    assert not result.is_valid
    assert any("must be a mapping" in error for error in result.errors)


@pytest.mark.parametrize("root", ["- id: example\n", "42\n"])
def test_validate_algorithms_file_rejects_non_mapping_root(tmp_path: Path, root: str):
    """Algorithm files with a non-mapping YAML root should fail validation cleanly."""
    file_path = tmp_path / "algorithms.yaml"
    file_path.write_text(root, encoding="utf-8")
    validator = Validator()

    result = validator.validate_algorithms_file(str(file_path))

    assert not result.is_valid
    assert any("root" in error.lower() and "must be a mapping" in error for error in result.errors)


@pytest.mark.parametrize("root", ["- id: example\n", "42\n"])
def test_validate_categories_file_rejects_non_mapping_root(tmp_path: Path, root: str):
    """Category files with a non-mapping YAML root should fail validation cleanly."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text(root, encoding="utf-8")
    validator = Validator()

    result = validator.validate_categories_file(str(file_path))

    assert not result.is_valid
    assert any("root" in error.lower() and "must be a mapping" in error for error in result.errors)


def test_validate_algorithms_file_reports_non_mapping_entries(tmp_path: Path):
    """Non-mapping items in an algorithms list should be reported per entry."""
    file_path = tmp_path / "algorithms.yaml"
    file_path.write_text(
        """algorithms:
  - just-a-string
  - 42
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_algorithms_file(str(file_path))

    assert not result.is_valid
    assert sum("must be a mapping" in error for error in result.errors) == 2


def test_validate_categories_file_reports_non_mapping_entries(tmp_path: Path):
    """Non-mapping items in a categories list should be reported per entry."""
    file_path = tmp_path / "categories.yaml"
    file_path.write_text(
        """categories:
  - just-a-string
  - 42
""",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_categories_file(str(file_path))

    assert not result.is_valid
    assert sum("must be a mapping" in error for error in result.errors) == 2


def test_validate_all_reports_non_mapping_root(tmp_path: Path):
    """validate_all should report non-mapping file roots instead of raising."""
    data_dir = tmp_path / "data"
    algorithms_dir = data_dir / "algorithms"
    algorithms_dir.mkdir(parents=True)
    (algorithms_dir / "entries.yaml").write_text("- id: example\n", encoding="utf-8")
    validator = Validator()

    result = validator.validate_all(str(data_dir))

    assert not result.is_valid
    assert any("must be a mapping" in error for error in result.errors)


def test_validate_all_reports_non_mapping_entries(tmp_path: Path):
    """validate_all should report non-mapping entries instead of raising."""
    data_dir = tmp_path / "data"
    algorithms_dir = data_dir / "algorithms"
    algorithms_dir.mkdir(parents=True)
    (algorithms_dir / "entries.yaml").write_text(
        "algorithms:\n  - just-a-string\n",
        encoding="utf-8",
    )
    validator = Validator()

    result = validator.validate_all(str(data_dir))

    assert not result.is_valid
    assert any("must be a mapping" in error for error in result.errors)


@pytest.mark.parametrize("field", ["language", "references"])
def test_null_list_fields_are_rejected(field: str):
    """Explicit null list fields must fail validation instead of crashing later."""
    validator = Validator()

    result = validator.validate_algorithm(build_valid_algorithm(**{field: None}))

    assert not result.is_valid
    assert f"Field '{field}' must be a list" in result.errors


def test_schema_normalizes_null_list_fields():
    """Loading data with null list fields should not raise during registry/export."""
    data = build_valid_algorithm(
        language=None,
        references=None,
        tags=None,
        related_tools=None,
    )

    entry = AlgorithmEntry.from_dict(data)

    assert entry.language == []
    assert entry.references == []
    assert entry.tags == []
    assert entry.related_tools == []
