"""
Tests for correct owner/repository/Pages URL metadata.

Ensures no stale 'shane' owner references survive in generators,
config, or link-checker metadata.
"""

import inspect
import os
import re

WRONG_OWNER_RE = re.compile(
    r"(shane\.github\.io|github\.com/shane\b|shane/awesome-bioinfo)", re.IGNORECASE
)
CORRECT_AUTHOR = "open-genomics Community"
CORRECT_REPO_URL = "https://github.com/open-genomics/awesome-bioinfo-algorithms"


# ---------------------------------------------------------------------------
# readme_generator.py
# ---------------------------------------------------------------------------


def test_readme_generator_no_wrong_owner():
    """ReadmeGenerator source must not contain stale shane owner references."""
    from awesome_bioinfo import readme_generator

    source = inspect.getsource(readme_generator)
    assert not WRONG_OWNER_RE.search(source), (
        "awesome_bioinfo/readme_generator.py still contains wrong owner/URL: "
        + str(WRONG_OWNER_RE.findall(source))
    )


# ---------------------------------------------------------------------------
# link_checker.py
# ---------------------------------------------------------------------------


def test_link_checker_user_agent_no_wrong_owner(project_root):
    """link_checker User-Agent must not contain stale shane owner URL."""
    path = os.path.join(project_root, "awesome_bioinfo", "link_checker.py")
    content = open(path, encoding="utf-8").read()
    assert not WRONG_OWNER_RE.search(content), (
        "awesome_bioinfo/link_checker.py still contains wrong owner/URL: "
        + str(WRONG_OWNER_RE.findall(content))
    )


def test_link_checker_repo_url_exact(project_root):
    """link_checker must reference the exact canonical repo URL."""
    path = os.path.join(project_root, "awesome_bioinfo", "link_checker.py")
    content = open(path, encoding="utf-8").read()
    assert CORRECT_REPO_URL in content, (
        f"awesome_bioinfo/link_checker.py must contain '{CORRECT_REPO_URL}'"
    )


# ---------------------------------------------------------------------------
# package metadata
# ---------------------------------------------------------------------------


def test_package_author_uses_canonical_owner():
    """Package metadata should use the canonical open-genomics owner name."""
    from awesome_bioinfo import __author__

    assert __author__ == CORRECT_AUTHOR
