# GitHub API Core

Lightweight wrapper around the GitHub CLI (`gh`) for repo metadata, cloning, file fetching, and repository provisioning.

## Overview
- Wraps the `gh` CLI for all GitHub operations — no direct HTTP or SSH libraries needed
- Validates `gh` installation and authentication once per process via `require_gh`
- Provides repo-scoped helpers through `GithubRepo` for cloning, file access, and temp cleanup
- Automates repository creation and initial commit pushes with sanitized URLs

## Features
- **Repo helper objects** – `GithubApi.repo(...)` returns a `GithubRepo` with cached metadata and branch info
- **Flexible cloning** – clone into a persistent destination or a managed temp dir with optional callback cleanup
- **File access** – fetch raw bytes or decoded text for any file via `gh api repos/:owner/:repo/contents/...`
- **Provisioning** – create repos, push initial commits, and compute canonical HTTPS URLs
- **Auth helpers** – surface authenticated user login and organization memberships for wizard prompts

## Quickstart

Clone a repo and inspect files:

```python
from pathlib import Path
from github_api_core import GithubApi

api = GithubApi()
repo = api.repo("https://github.com/octocat/Hello-World")

def inspect(clone_dir: str) -> None:
    for entry in sorted(Path(clone_dir).iterdir()):
        print(entry.name)

repo.clone_repo(callback=inspect)
```

Fetch a single file as text:

```python
from github_api_core import GithubApi

api = GithubApi()
repo = api.repo("github/gitignore", branch="main")
license_text = repo.get_file("LICENSE")
```

Create a repo and push:

```python
from github_api_core import GithubApi

api = GithubApi()
api.create_repo(owner="my-org", name="new-project", private=True)
api.push_initial_commit("./local-project", owner="my-org", name="new-project")
```

## API

```python
class GithubApi:
    def __init__(self, *, temp_mgr: TempFilesManager | None = None, timeout: int = 15) -> None: ...
    def repo(self, url: str, branch: str | None = None) -> GithubRepo: ...
    def create_repo(
        self,
        owner: str,
        name: str,
        *,
        private: bool = False,
        description: str | None = None,
        source: str | None = None,
    ) -> bool: ...
    def get_user_orgs(self) -> list[dict[str, Any]]: ...
    def get_authenticated_user_login(self) -> str: ...
    def push_initial_commit(
        self,
        repo_path: str | Path,
        owner: str,
        name: str,
        *,
        branch: str = "main",
        message: str = "init commit",
    ) -> None: ...
    @staticmethod
    def build_repo_url(owner: str, name: str) -> str: ...
    @staticmethod
    def sanitize_repo_name(name: str) -> str: ...
    @classmethod
    def require_gh(cls) -> str: ...

class GithubRepo:
    def __init__(self, api: GithubApi, *, url: str, branch: str | None = None) -> None: ...
    def clone_repo(
        self,
        dest_path: str | None = None,
        *,
        callback: Callable[[str], Any] | None = None,
        clone_args: list[str] | None = None,
    ) -> Any: ...
    def get_file(self, relative_path: str, *, encoding: str = "utf-8") -> str | None: ...
    def get_file_bytes(self, relative_path: str) -> bytes | None: ...
    def cleanup_temp(self, path: str) -> None: ...
```

## Notes
- All operations use the `gh` CLI via subprocess — no `requests` or `GitPython` needed.
- Provide either `dest_path` or `callback` to `clone_repo`; when both are set the callback receives the persistent path.
- `clone_args` defaults to `["--depth=1"]` for fast operations — pass an empty list for full history.
- `require_gh` caches the resolved path after the first successful check.

## Requirements & prerequisites
- GitHub CLI (`gh`) installed and authenticated against `github.com`
- logger-util
- exceptions-core
- temp-files-manager

## Troubleshooting
- **`ADHDError` referencing install/login** – run `gh auth status` or reinstall the CLI following steps in `url_utils.py`.
- **Clone returns `False`** – check repository permissions or branch names; stderr is logged with the failure.
- **`ValueError` from `_canonical_repo_name`** – the provided URL or slug is invalid or inaccessible; try full `owner/name` format.
- **`Failed to push initial commit`** – ensure the target path is a directory and you have push rights to the remote.
- **`get_file_bytes` returns `None`** – the file does not exist at the given path/branch; check the relative path and branch name.

## Module structure

```
github_api_core/
├─ __init__.py        # exports GithubApi and GithubRepo
├─ api.py             # CLI-backed GithubApi and GithubRepo implementation
├─ url_utils.py       # user guidance constants for gh install and login
├─ pyproject.toml     # package metadata and dependencies
└─ README.md          # this file
```

## See also
- Temp Files Manager – manages directories for ephemeral clones
- Creator Common Core – shared helpers that use GithubApi for cloning and pushing
- Module Creator Core – module scaffolding with repo automation
