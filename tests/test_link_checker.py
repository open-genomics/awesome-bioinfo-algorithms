"""Tests for link_checker module."""

import asyncio
from dataclasses import asdict
from unittest.mock import AsyncMock, MagicMock

from awesome_bioinfo import link_checker
from awesome_bioinfo.link_checker import (
    LinkCheckResult,
    LinkCheckSummary,
    check_url,
    is_safe_url,
    is_valid_url,
)


class TestLinkCheckResult:
    """Test LinkCheckResult dataclass."""

    def test_result_creation(self) -> None:
        """LinkCheckResult should be created with required fields."""
        result = LinkCheckResult(
            url="https://example.com",
            algorithm_id="test-algo",
            field_type="paper_url",
            status="ok",
        )
        assert result.url == "https://example.com"
        assert result.algorithm_id == "test-algo"
        assert result.field_type == "paper_url"
        assert result.status == "ok"
        assert result.status_code is None
        assert result.error_message == ""

    def test_result_with_all_fields(self) -> None:
        """LinkCheckResult should accept all fields."""
        result = LinkCheckResult(
            url="https://example.com",
            algorithm_id="test-algo",
            field_type="implementation_url",
            status="error",
            status_code=404,
            error_message="Not found",
        )
        assert result.status_code == 404
        assert result.error_message == "Not found"

    def test_result_to_dict(self) -> None:
        """LinkCheckResult should be convertible to dict."""
        result = LinkCheckResult(
            url="https://example.com",
            algorithm_id="test-algo",
            field_type="paper_url",
            status="ok",
            status_code=200,
        )
        d = asdict(result)
        assert d["url"] == "https://example.com"
        assert d["status_code"] == 200


class TestLinkCheckSummary:
    """Test LinkCheckSummary dataclass."""

    def test_summary_creation(self) -> None:
        """LinkCheckSummary should start with zero counts."""
        summary = LinkCheckSummary()
        assert summary.total == 0
        assert summary.ok == 0
        assert summary.errors == 0
        assert summary.warnings == 0
        assert summary.results == []

    def test_add_result_ok(self) -> None:
        """add_result should increment ok count for ok status."""
        summary = LinkCheckSummary()
        result = LinkCheckResult(
            url="https://example.com",
            algorithm_id="test",
            field_type="paper_url",
            status="ok",
        )
        summary.add_result(result)
        assert summary.total == 1
        assert summary.ok == 1
        assert summary.errors == 0

    def test_add_result_error(self) -> None:
        """add_result should increment error count for error status."""
        summary = LinkCheckSummary()
        result = LinkCheckResult(
            url="https://example.com",
            algorithm_id="test",
            field_type="paper_url",
            status="error",
        )
        summary.add_result(result)
        assert summary.total == 1
        assert summary.errors == 1
        assert summary.ok == 0

    def test_add_result_warning(self) -> None:
        """add_result should increment warning count for warning status."""
        summary = LinkCheckSummary()
        result = LinkCheckResult(
            url="https://example.com",
            algorithm_id="test",
            field_type="paper_url",
            status="warning",
        )
        summary.add_result(result)
        assert summary.total == 1
        assert summary.warnings == 1

    def test_add_multiple_results(self) -> None:
        """add_result should handle multiple results."""
        summary = LinkCheckSummary()
        results = [
            LinkCheckResult("url1", "a1", "paper_url", "ok"),
            LinkCheckResult("url2", "a2", "paper_url", "error"),
            LinkCheckResult("url3", "a3", "paper_url", "ok"),
        ]
        for r in results:
            summary.add_result(r)
        assert summary.total == 3
        assert summary.ok == 2
        assert summary.errors == 1


class TestIsValidUrl:
    """Test is_valid_url function."""

    def test_valid_http_url(self) -> None:
        """is_valid_url should return True for valid HTTP URL."""
        assert is_valid_url("http://example.com") is True

    def test_valid_https_url(self) -> None:
        """is_valid_url should return True for valid HTTPS URL."""
        assert is_valid_url("https://example.com/path?query=1") is True

    def test_invalid_url_no_scheme(self) -> None:
        """is_valid_url should return False for URL without scheme."""
        assert is_valid_url("example.com") is False

    def test_invalid_url_ftp(self) -> None:
        """is_valid_url should return False for FTP URL."""
        assert is_valid_url("ftp://example.com") is False

    def test_invalid_url_empty(self) -> None:
        """is_valid_url should return False for empty string."""
        assert is_valid_url("") is False


class TestCheckUrl:
    """Test check_url async function."""

    def test_check_url_success(self) -> None:
        """check_url should return status code for valid URL."""

        async def run_test() -> None:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.__aenter__.return_value = mock_response

            mock_session = MagicMock()
            mock_session.head.return_value = mock_response

            status, error = await check_url(mock_session, "https://example.com")
            assert status == 200
            assert error == ""

        asyncio.run(run_test())

    def test_check_url_timeout(self) -> None:
        """check_url should handle timeout."""

        async def run_test() -> None:
            mock_session = MagicMock()
            mock_session.head.side_effect = asyncio.TimeoutError()

            status, error = await check_url(mock_session, "https://example.com")
            assert status is None
            assert "Timeout" in error

        asyncio.run(run_test())

    def test_check_url_405_fallback_to_get(self) -> None:
        """check_url should fallback to GET on 405."""

        async def run_test() -> None:
            mock_head_response = AsyncMock()
            mock_head_response.status = 405
            mock_head_response.__aenter__.return_value = mock_head_response

            mock_get_response = AsyncMock()
            mock_get_response.status = 200
            mock_get_response.__aenter__.return_value = mock_get_response

            mock_session = MagicMock()
            mock_session.head.return_value = mock_head_response
            mock_session.get.return_value = mock_get_response

            status, error = await check_url(mock_session, "https://example.com")
            assert status == 200
            mock_session.get.assert_called_once()

        asyncio.run(run_test())


class TestIsSafeUrl:
    """Test SSRF guard for link checking."""

    def test_rejects_private_and_loopback_targets(self) -> None:
        for url in (
            "http://127.0.0.1/",
            "http://[::1]/",
            "http://10.1.2.3/",
            "http://169.254.169.254/latest/meta-data/",
            "file:///etc/passwd",
        ):
            assert is_safe_url(url) is False

    def test_accepts_public_address(self, monkeypatch) -> None:
        monkeypatch.setattr(
            link_checker.socket,
            "getaddrinfo",
            lambda *args, **kwargs: [(2, 1, 6, "", ("93.184.216.34", 0))],
        )
        assert is_safe_url("https://example.com/path") is True

    def test_check_url_blocks_private_target_before_request(self) -> None:
        async def run_test() -> None:
            mock_session = MagicMock()
            status, error = await check_url(mock_session, "http://127.0.0.1/")
            assert status is None
            assert "non-public" in error
            mock_session.head.assert_not_called()

        asyncio.run(run_test())
