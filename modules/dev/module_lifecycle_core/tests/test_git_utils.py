"""Unit tests for _git_utils.parse_github_url.

MOCKS USED IN THIS FILE:
- None — parse_github_url is a pure function (no I/O, no subprocess).
"""

from __future__ import annotations

from module_lifecycle_core._git_utils import ParsedGitSource, parse_github_url


class TestParseGithubUrlBrowserUrls:
    """Browser URLs with /tree/branch/subfolder should decompose correctly."""

    def test_full_browser_url_with_subfolder(self) -> None:
        result = parse_github_url(
            "https://github.com/AI-Driven-Highspeed-Development/adhd_framework_v3"
            "/tree/main/modules/dev/adhd_mcp"
        )
        assert result.clone_url == (
            "https://github.com/AI-Driven-Highspeed-Development/adhd_framework_v3.git"
        )
        assert result.branch == "main"
        assert result.subfolder == "modules/dev/adhd_mcp"

    def test_branch_only_no_subfolder(self) -> None:
        result = parse_github_url("https://github.com/org/repo/tree/develop")
        assert result.clone_url == "https://github.com/org/repo.git"
        assert result.branch == "develop"
        assert result.subfolder is None

    def test_trailing_slash_on_subfolder(self) -> None:
        result = parse_github_url(
            "https://github.com/org/repo/tree/main/path/to/folder/"
        )
        assert result.subfolder == "path/to/folder"

    def test_deep_nested_subfolder(self) -> None:
        result = parse_github_url(
            "https://github.com/org/repo/tree/main/a/b/c/d/e"
        )
        assert result.clone_url == "https://github.com/org/repo.git"
        assert result.branch == "main"
        assert result.subfolder == "a/b/c/d/e"

    def test_branch_with_version_tag(self) -> None:
        result = parse_github_url(
            "https://github.com/org/repo/tree/v1.2.3/src/module"
        )
        assert result.branch == "v1.2.3"
        assert result.subfolder == "src/module"


class TestParseGithubUrlCloneUrls:
    """Standard clone URLs should normalise to .git suffix."""

    def test_https_with_git_suffix(self) -> None:
        result = parse_github_url("https://github.com/org/repo.git")
        assert result.clone_url == "https://github.com/org/repo.git"
        assert result.branch is None
        assert result.subfolder is None

    def test_https_without_git_suffix(self) -> None:
        result = parse_github_url("https://github.com/org/repo")
        assert result.clone_url == "https://github.com/org/repo.git"
        assert result.branch is None
        assert result.subfolder is None

    def test_trailing_slash(self) -> None:
        result = parse_github_url("https://github.com/org/repo/")
        assert result.clone_url == "https://github.com/org/repo.git"

    def test_http_url(self) -> None:
        result = parse_github_url("http://github.com/org/repo")
        assert result.clone_url == "https://github.com/org/repo.git"

    def test_hyphenated_repo_name(self) -> None:
        result = parse_github_url("https://github.com/org/my-cool-repo")
        assert result.clone_url == "https://github.com/org/my-cool-repo.git"

    def test_underscore_repo_name(self) -> None:
        result = parse_github_url("https://github.com/org/my_repo_v3")
        assert result.clone_url == "https://github.com/org/my_repo_v3.git"


class TestParseGithubUrlPassthrough:
    """Non-GitHub and SSH URLs should pass through unchanged."""

    def test_ssh_url_passthrough(self) -> None:
        url = "git@github.com:org/repo.git"
        result = parse_github_url(url)
        assert result.clone_url == url
        assert result.branch is None
        assert result.subfolder is None

    def test_gitlab_https_passthrough(self) -> None:
        url = "https://gitlab.com/org/repo.git"
        result = parse_github_url(url)
        assert result.clone_url == url
        assert result.branch is None
        assert result.subfolder is None

    def test_bitbucket_https_passthrough(self) -> None:
        url = "https://bitbucket.org/org/repo.git"
        result = parse_github_url(url)
        assert result.clone_url == url

    def test_custom_domain_passthrough(self) -> None:
        url = "https://git.example.com/org/repo.git"
        result = parse_github_url(url)
        assert result.clone_url == url

    def test_non_url_string_passthrough(self) -> None:
        url = "not-a-url"
        result = parse_github_url(url)
        assert result.clone_url == url
        assert result.branch is None
        assert result.subfolder is None


class TestParsedGitSourceDataclass:
    """ParsedGitSource dataclass defaults."""

    def test_defaults(self) -> None:
        p = ParsedGitSource(clone_url="https://example.com/repo.git")
        assert p.branch is None
        assert p.subfolder is None

    def test_all_fields(self) -> None:
        p = ParsedGitSource(
            clone_url="https://github.com/org/repo.git",
            branch="main",
            subfolder="path/to/mod",
        )
        assert p.clone_url == "https://github.com/org/repo.git"
        assert p.branch == "main"
        assert p.subfolder == "path/to/mod"
