"""
URL validation module for checking algorithm paper and implementation links.

Usage:
    python -m awesome_bioinfo check-links

This command validates all URLs in algorithm entries and reports broken links.
"""

from __future__ import annotations

import asyncio
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import yaml


@dataclass
class LinkCheckResult:
    """Result of checking a single URL."""

    url: str
    algorithm_id: str
    field_type: str  # 'paper_url' or 'implementation_url'
    status: str  # 'ok', 'error', 'warning'
    status_code: int | None = None
    error_message: str = ""


@dataclass
class LinkCheckSummary:
    """Summary of all link checks."""

    total: int = 0
    ok: int = 0
    errors: int = 0
    warnings: int = 0
    results: list[LinkCheckResult] = field(default_factory=list)

    def add_result(self, result: LinkCheckResult) -> None:
        """Add a result and update counters."""
        self.results.append(result)
        self.total += 1
        if result.status == "ok":
            self.ok += 1
        elif result.status == "error":
            self.errors += 1
        elif result.status == "warning":
            self.warnings += 1


async def check_url(
    session: aiohttp.ClientSession, url: str, timeout: int = 30
) -> tuple[int | None, str]:
    """Check if a URL is accessible."""
    try:
        async with session.head(url, timeout=timeout, allow_redirects=True) as response:
            # HEAD request might not be supported, try GET for 405 errors
            if response.status == 405:
                async with session.get(url, timeout=timeout, allow_redirects=True) as get_response:
                    return get_response.status, ""
            return response.status, ""
    except asyncio.TimeoutError:
        return None, "Timeout"
    except aiohttp.ClientError as e:
        return None, str(e)
    except Exception as e:
        return None, str(e)


def is_valid_url(url: str) -> bool:
    """Check if URL has valid format."""
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except Exception:
        return False


async def check_all_links(data_dir: Path) -> LinkCheckSummary:
    """Check all URLs in algorithm data files."""
    summary = LinkCheckSummary()
    algorithms_dir = data_dir / "algorithms"

    # Collect all URLs to check
    urls_to_check: list[tuple[str, str, str]] = []  # (url, algorithm_id, field_type)

    for yaml_file in algorithms_dir.glob("*.yaml"):
        try:
            with open(yaml_file, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or "algorithms" not in data:
                continue

            for algo in data["algorithms"]:
                algo_id = algo.get("id", "unknown")

                # Check paper_url
                if paper_url := algo.get("paper_url"):
                    urls_to_check.append((paper_url, algo_id, "paper_url"))

                # Check implementation_url
                if impl_url := algo.get("implementation_url"):
                    urls_to_check.append((impl_url, algo_id, "implementation_url"))

                # Check reference URLs
                if references := algo.get("references", []):
                    for ref in references:
                        if ref_url := ref.get("url"):
                            urls_to_check.append(
                                (ref_url, algo_id, f"reference:{ref.get('title', 'unknown')}")
                            )

        except Exception as e:
            print(f"Warning: Error reading {yaml_file}: {e}")
            continue

    # Check URLs concurrently with rate limiting
    connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
    timeout = aiohttp.ClientTimeout(total=60)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout,
        headers={
            "User-Agent": "AwesomeBioinfoBot/1.0 (+https://github.com/open-genomics/awesome-bioinfo-algorithms)"
        },
    ) as session:
        semaphore = asyncio.Semaphore(5)  # Limit concurrent requests

        async def check_with_limit(url: str, algo_id: str, field_type: str) -> LinkCheckResult:
            async with semaphore:
                # Rate limiting - small delay between requests
                await asyncio.sleep(0.5)

                if not is_valid_url(url):
                    return LinkCheckResult(
                        url=url,
                        algorithm_id=algo_id,
                        field_type=field_type,
                        status="error",
                        error_message="Invalid URL format",
                    )

                status_code, error = await check_url(session, url)

                if error:
                    return LinkCheckResult(
                        url=url,
                        algorithm_id=algo_id,
                        field_type=field_type,
                        status="error",
                        error_message=error,
                    )

                # Consider 2xx and 3xx as OK, 403 as warning (often blocks bots)
                if status_code and 200 <= status_code < 400:
                    return LinkCheckResult(
                        url=url,
                        algorithm_id=algo_id,
                        field_type=field_type,
                        status="ok",
                        status_code=status_code,
                    )
                elif status_code == 403:
                    return LinkCheckResult(
                        url=url,
                        algorithm_id=algo_id,
                        field_type=field_type,
                        status="warning",
                        status_code=status_code,
                        error_message="Access forbidden (may require authentication)",
                    )
                else:
                    return LinkCheckResult(
                        url=url,
                        algorithm_id=algo_id,
                        field_type=field_type,
                        status="error",
                        status_code=status_code,
                        error_message=f"HTTP {status_code}" if status_code else "Unknown error",
                    )

        # Run all checks concurrently
        tasks = [
            check_with_limit(url, algo_id, field_type) for url, algo_id, field_type in urls_to_check
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                summary.add_result(
                    LinkCheckResult(
                        url="unknown",
                        algorithm_id="unknown",
                        field_type="unknown",
                        status="error",
                        error_message=str(result),
                    )
                )
            else:
                # result is LinkCheckResult here, but mypy can't narrow from Exception check
                summary.add_result(result)  # type: ignore[arg-type]

    return summary


def cmd_check_links() -> int:
    """Command entry point for link checking."""
    from pathlib import Path

    base_dir = Path(__file__).resolve().parent.parent
    data_dir = base_dir / "data"

    print("🔍 Checking algorithm URLs...")
    print("=" * 60)

    try:
        summary = asyncio.run(check_all_links(data_dir))
    except KeyboardInterrupt:
        print("\n⚠️  Link check interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error during link check: {e}")
        return 1

    # Print results
    if summary.errors > 0:
        print("\n❌ Errors:")
        for result in summary.results:
            if result.status == "error":
                print(f"  [{result.algorithm_id}] {result.field_type}")
                print(f"    URL: {result.url}")
                print(f"    Error: {result.error_message}")
                print()

    if summary.warnings > 0:
        print("\n⚠️  Warnings:")
        for result in summary.results:
            if result.status == "warning":
                print(f"  [{result.algorithm_id}] {result.field_type}")
                print(f"    URL: {result.url}")
                print(f"    Warning: {result.error_message}")
                print()

    # Print summary
    print("=" * 60)
    print(f"📊 Summary: {summary.total} URLs checked")
    print(f"  ✅ OK:       {summary.ok}")
    print(f"  ⚠️  Warning:  {summary.warnings}")
    print(f"  ❌ Error:    {summary.errors}")

    if summary.errors > 0:
        print("\n❌ Link check failed with errors")
        return 1
    elif summary.warnings > 0:
        print("\n⚠️  Link check completed with warnings")
        return 0
    else:
        print("\n✅ All links are valid!")
        return 0


if __name__ == "__main__":
    sys.exit(cmd_check_links())
