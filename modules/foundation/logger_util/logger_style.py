import logging
from abc import ABC, abstractmethod

__all__ = [
    "LoggerStyle",
    "NormalStyle",
]


class LoggerStyle(ABC):
    """Abstract base class for logger style/formatting."""

    @abstractmethod
    def create_formatter(self) -> logging.Formatter:
        """Return a logging.Formatter configured for this style."""
        raise NotImplementedError

    def apply(self, handler: logging.Handler) -> None:
        """Apply this style to a handler by setting its formatter."""
        handler.setFormatter(self.create_formatter())


class NormalStyle(LoggerStyle):
    """Standard verbose logging style for console output."""

    def __init__(self, *, datefmt: str = "%Y-%m-%d %H:%M:%S") -> None:
        self._datefmt = datefmt

    def create_formatter(self) -> logging.Formatter:
        return logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt=self._datefmt,
        )
