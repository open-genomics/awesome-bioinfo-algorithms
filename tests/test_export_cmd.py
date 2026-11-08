"""Tests for the export command module."""

import csv
import io
import json
import os
import tempfile

import pytest

from awesome_bioinfo.__main__ import cmd_export
from awesome_bioinfo.algorithm_registry import AlgorithmRegistry
from awesome_bioinfo.category_manager import CategoryManager
from awesome_bioinfo.schema import AlgorithmEntry


@pytest.fixture
def mock_category_manager():
    """Create a mock category manager."""
    return CategoryManager()


@pytest.fixture
def mock_registry():
    """Create a mock registry with sample algorithms."""
    registry = AlgorithmRegistry()
    registry.from_algorithms(
        [
            AlgorithmEntry(
                id="algo-1",
                name="Test Algorithm One",
                description="A test algorithm description that meets the minimum length requirement.",
                purpose="Testing purposes",
                time_complexity="O(n)",
                category="test-cat",
                tags=["test", "unit"],
                difficulty="beginner",
                year=2020,
                language=["Python"],
            ),
            AlgorithmEntry(
                id="algo-2",
                name="Test Algorithm Two",
                description="Another test algorithm description that meets the minimum length requirement.",
                purpose="More testing",
                time_complexity="O(n log n)",
                category="test-cat",
                tags=["test", "integration"],
                difficulty="intermediate",
            ),
        ]
    )
    return registry


class TestCmdExport:
    """Tests for cmd_export function."""

    def test_export_json_to_stdout(self, mock_registry, mock_category_manager, capsys):
        """Test JSON export to stdout."""
        result = cmd_export(mock_registry, mock_category_manager, fmt="json")
        assert result == 0
        output = capsys.readouterr().out
        data = json.loads(output)
        assert "algorithms" in data
        assert data["total"] == 2

    def test_export_csv_to_stdout(self, mock_registry, mock_category_manager, capsys):
        """Test CSV export to stdout."""
        result = cmd_export(mock_registry, mock_category_manager, fmt="csv")
        assert result == 0
        output = capsys.readouterr().out
        lines = output.strip().split("\n")
        assert len(lines) == 3  # header + 2 algorithms
        assert "id,name,year" in lines[0]

    def test_export_json_to_file(self, mock_registry, mock_category_manager):
        """Test JSON export to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            output_path = f.name

        try:
            result = cmd_export(
                mock_registry, mock_category_manager, fmt="json", output=output_path
            )
            assert result == 0
            assert os.path.exists(output_path)

            with open(output_path, encoding="utf-8") as f:
                data = json.load(f)
            assert data["total"] == 2
        finally:
            os.unlink(output_path)

    def test_export_csv_neutralizes_formula_prefixes(self, mock_category_manager, capsys):
        """Cells starting with spreadsheet formula prefixes must be quoted."""
        registry = AlgorithmRegistry()
        registry.from_algorithms(
            [
                AlgorithmEntry(
                    id="algo-formula",
                    name='=HYPERLINK("https://example.invalid")',
                    description=(
                        "A test algorithm description that meets the minimum length requirement."
                    ),
                    purpose="+SUM(1,1)",
                    time_complexity="O(n)",
                    category="test-cat",
                )
            ]
        )

        assert cmd_export(registry, mock_category_manager, fmt="csv") == 0
        rows = list(csv.reader(io.StringIO(capsys.readouterr().out)))
        header, row = rows[0], rows[1]
        name = row[header.index("name")]
        purpose = row[header.index("purpose")]
        assert name.startswith("'=")
        assert purpose.startswith("'+")

    def test_export_csv_to_file(self, mock_registry, mock_category_manager):
        """Test CSV export to file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            output_path = f.name

        try:
            result = cmd_export(mock_registry, mock_category_manager, fmt="csv", output=output_path)
            assert result == 0
            assert os.path.exists(output_path)

            with open(output_path, encoding="utf-8") as f:
                content = f.read()
            lines = content.strip().split("\n")
            assert len(lines) == 3
        finally:
            os.unlink(output_path)

    def test_export_invalid_format(self, mock_registry, mock_category_manager, capsys):
        """Test export with invalid format returns error."""
        result = cmd_export(mock_registry, mock_category_manager, fmt="xml")
        assert result == 1
        output = capsys.readouterr().out
        assert "Unsupported format" in output

    def test_export_empty_registry(self, mock_category_manager, capsys):
        """Test export with empty registry."""
        empty_registry = AlgorithmRegistry()
        empty_registry._algorithms = {}
        result = cmd_export(empty_registry, mock_category_manager, fmt="json")
        assert result == 1
        output = capsys.readouterr().out
        assert "No algorithms" in output

    def test_export_json_contains_all_fields(self, mock_registry, mock_category_manager, capsys):
        """Test JSON export contains all expected fields."""
        result = cmd_export(mock_registry, mock_category_manager, fmt="json")
        assert result == 0
        output = capsys.readouterr().out
        data = json.loads(output)

        algo = data["algorithms"][0]
        assert "id" in algo
        assert "name" in algo
        assert "description" in algo
        assert "purpose" in algo
        assert "time_complexity" in algo
        assert "category" in algo

    def test_export_csv_contains_headers(self, mock_registry, mock_category_manager, capsys):
        """Test CSV export contains all expected headers."""
        result = cmd_export(mock_registry, mock_category_manager, fmt="csv")
        assert result == 0
        output = capsys.readouterr().out
        lines = output.strip().split("\n")
        headers = lines[0].strip().split(",")

        expected_headers = [
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
        for header in expected_headers:
            assert header in headers, f"Missing header: {header}"
