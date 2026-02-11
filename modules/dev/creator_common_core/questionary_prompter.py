"""Questionary Prompter - Interactive prompt wrapper using questionary.

Extracted from creator_common_core.py so that other dev-layer modules
(e.g., module_lifecycle_core) can import it without pulling in git/template helpers.
"""

from __future__ import annotations

from typing import Iterable, Sequence

import questionary


class QuestionaryCore:
    """Wrapper around the questionary prompts with project config wiring."""

    def __init__(self) -> None:
        pass

    def multiple_choice(
        self,
        message: str,
        choices: Sequence[str],
        default: str | None = None,
    ) -> str:
        """Render a select prompt and return the chosen option."""
        if not choices:
            raise ValueError("choices must contain at least one option")
        if default is not None and default not in choices:
            raise ValueError("default must be one of the provided choices")
        result = questionary.select(
            message,
            choices=list(choices),
            default=default,
            use_indicator=True,
            use_jk_keys=False,
            use_search_filter=True,
        ).ask()
        if result is None:
            raise KeyboardInterrupt("Multiple choice prompt aborted")
        return result

    def multiple_select(
        self,
        message: str,
        choices: Sequence[str],
        default: Sequence[str] | None = None,
    ) -> list[str]:
        """Render a checkbox prompt and return the selected options."""
        if not choices:
            raise ValueError("choices must contain at least one option")
        if default is not None:
            invalid = set(default) - set(choices)
            if invalid:
                raise ValueError(f"default contains invalid choices: {invalid}")
        result = questionary.checkbox(
            message,
            choices=list(choices),
            default=list(default) if default else None,
            use_jk_keys=False,
            use_search_filter=True,
        ).ask()
        if result is None:
            raise KeyboardInterrupt("Multiple select prompt aborted")
        return result

    def path_input(self, message: str, *, default: str | None = None, only_directories: bool = False) -> str:
        """Collect a filesystem path with tab completion support."""
        result = questionary.path(
            message,
            default=default or "",
            only_directories=only_directories,
        ).ask()
        if result is None:
            raise KeyboardInterrupt("Path prompt aborted")
        return result

    def autocomplete_input(
        self,
        message: str,
        choices: Iterable[str],
        *,
        default: str | None = None,
        match_middle: bool = True,
    ) -> str:
        """Collect free text with inline completion suggestions."""
        values = list(dict.fromkeys(choices))
        if default is not None and default not in values:
            values.append(default)
        result = questionary.autocomplete(
            message,
            choices=values,
            default=default,
            match_middle=match_middle,
        ).ask()
        if result is None:
            raise KeyboardInterrupt("Autocomplete prompt aborted")
        return result

    def confirm(self, message: str, *, default: bool = False) -> bool:
        """Ask a yes/no question and return the boolean answer."""
        result = questionary.confirm(
            message,
            default=default,
        ).ask()
        if result is None:
            raise KeyboardInterrupt("Confirm prompt aborted")
        return result

    def text_input(self, message: str, *, default: str = "") -> str:
        """Collect free text input."""
        result = questionary.text(
            message,
            default=default,
        ).ask()
        if result is None:
            raise KeyboardInterrupt("Text prompt aborted")
        return result
