# Creator Common Core

Shared utilities for project and module creators covering template cloning, GitHub repo provisioning, name normalization, and interactive prompts.

## Overview
- Provides `RepoCreationOptions` dataclass reused by wizards and creators
- Clones template repositories and strips git metadata via `clone_template`
- Creates remote GitHub repos and pushes initial commits via `create_remote_repo`
- Wraps questionary prompts in `QuestionaryCore` for interactive CLI flows
- Offers `to_snake_case` for name normalization and `list_templates` for YAML catalog parsing

## Features
- **Sanitized cloning** – clones any template repo and removes `.git` to avoid history reuse
- **Repo provisioning** – wraps `GithubApi` for repo creation and push with consistent error handling
- **Template catalog** – converts YAML dicts into `TemplateInfo` objects for wizard consumption
- **Interactive prompts** – `QuestionaryCore` provides select, checkbox, path, autocomplete, confirm, and text prompts
- **Name normalization** – `to_snake_case` converts arbitrary strings to valid snake_case identifiers

## Quickstart

Clone a template and provision a repo:

```python
from pathlib import Path
from creator_common_core import RepoCreationOptions, clone_template, create_remote_repo
from github_api_core import GithubApi
from logger_util import Logger

api = GithubApi()
logger = Logger("CreatorCommon")

dest = clone_template(api, "https://github.com/org/python-template", Path("./tmp/template"))

create_remote_repo(
    repo_name="My Service",
    local_path=dest,
    options=RepoCreationOptions(owner="my-org", visibility="private"),
    logger=logger,
)
```

Use interactive prompts:

```python
from creator_common_core import QuestionaryCore

prompter = QuestionaryCore()
choice = prompter.multiple_choice("Pick a layer", ["foundation", "runtime", "dev"], default="runtime")
```

## API

```python
@dataclass
class RepoCreationOptions:
    owner: str
    visibility: str                    # "public" | "private"
    repo_url: Optional[str] = None

@dataclass
class TemplateInfo:
    name: str
    description: str
    url: str

def clone_template(api: GithubApi, template_url: str, target: Path) -> Path: ...
def create_remote_repo(
    repo_name: str,
    local_path: Path,
    options: RepoCreationOptions,
    logger,
) -> None: ...
def remove_git_dir(path: Path) -> None: ...
def list_templates(template_dict: dict) -> list[TemplateInfo]: ...
def to_snake_case(value: str) -> str: ...

class QuestionaryCore:
    def __init__(self) -> None: ...
    def multiple_choice(self, message: str, choices: Sequence[str], default: str | None = None) -> str: ...
    def multiple_select(self, message: str, choices: Sequence[str], default: Sequence[str] | None = None) -> list[str]: ...
    def path_input(self, message: str, *, default: str | None = None, only_directories: bool = False) -> str: ...
    def autocomplete_input(self, message: str, choices: Iterable[str], *, default: str | None = None) -> str: ...
    def confirm(self, message: str, *, default: bool = False) -> bool: ...
    def text_input(self, message: str, *, default: str = "") -> str: ...
```

## Notes
- `create_remote_repo` creates a `GithubApi` internally; it does not accept one as a parameter.
- `clone_template` requires an existing `GithubApi` instance for the underlying clone operation.
- All `QuestionaryCore` methods raise `KeyboardInterrupt` when the user aborts a prompt.
- `list_templates` ignores entries missing a `url`, preventing incomplete templates from leaking into menus.

## Requirements & prerequisites
- exceptions-core
- github-api-core
- questionary (>=2.0)

## Troubleshooting
- **Template clone returns `False`** – the GitHub CLI failed; check auth and repo URL in the logs.
- **`ADHDError: Remote repository creation failed`** – verify `options.visibility` is `public` or `private` and you have push rights.
- **`ValueError` from `list_templates`** – ensure the YAML resolves to a dict with `description` and `url` keys per entry.
- **`KeyboardInterrupt` from prompts** – the user pressed Ctrl+C; catch this in the calling wizard.
- **`to_snake_case` returns `"unnamed"`** – the input was empty or contained only special characters.

## Module structure

```
creator_common_core/
├─ __init__.py                # exports all public symbols
├─ creator_common_core.py     # RepoCreationOptions, clone/repo helpers, to_snake_case, TemplateInfo
├─ questionary_prompter.py    # QuestionaryCore interactive prompt wrapper
├─ pyproject.toml             # package metadata and dependencies
└─ README.md                  # this file
```

## See also
- Module Creator Core – module scaffolding that consumes these helpers
- Project Creator Core – project scaffolding built on the same utilities
- GitHub API Core – underlying gh CLI wrapper used by clone and repo functions