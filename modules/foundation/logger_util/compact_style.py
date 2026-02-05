import logging
import os
import sys
from typing import Optional
from .logger_style import LoggerStyle

__all__ = [
    "CompactStyle",
    "apply_style",
]


class CompactStyle(LoggerStyle):
    """
    Compact console style:
      "HH:MM:SS L Name: message"
    where L is 1-letter level: D/I/W/E/C.
    Name is truncated to keep line width readable.
    Optional ANSI colors.
    """

    class _Formatter(logging.Formatter):
        LEVEL_CHAR = {
            logging.DEBUG: "D",
            logging.INFO: "I",
            logging.WARNING: "W",
            logging.ERROR: "E",
            logging.CRITICAL: "C",
        }

        COLORS = {
            logging.DEBUG: "\033[90m",   # bright black
            logging.INFO: "\033[37m",    # white
            logging.WARNING: "\033[33m", # yellow
            logging.ERROR: "\033[31m",   # red
            logging.CRITICAL: "\033[35m" # magenta
        }
        RESET = "\033[0m"

        def __init__(self, time_fmt: str = "%H:%M:%S", use_color: bool = False, name_width: int = 18):
            fmt = "%(asctime)s %(levelchar)s %(shortname)s: %(message)s"
            super().__init__(fmt=fmt, datefmt=time_fmt)
            self.use_color = use_color
            self.name_width = max(6, int(name_width))

        def _shorten_name(self, name: str) -> str:
            base = name.split(".")[-1]
            if len(base) <= self.name_width:
                return base
            keep = self.name_width - 1
            left = keep // 2
            right = keep - left
            return f"{base[:left]}…{base[-right:]}"

        def format(self, record: logging.LogRecord) -> str:
            record.levelchar = self.LEVEL_CHAR.get(record.levelno, "?")
            record.shortname = self._shorten_name(record.name)
            line = super().format(record)
            if self.use_color and sys.stdout.isatty():
                color = self.COLORS.get(record.levelno)
                if color:
                    prefix = f"{record.levelchar} {record.shortname}:"
                    colored = f"{color}{record.levelchar}{self.RESET} {color}{record.shortname}{self.RESET}:"
                    line = line.replace(prefix, colored, 1)
            return line

    def __init__(self, *, time_fmt: str = "%H:%M:%S", use_color: Optional[bool] = None, name_width: int = 18) -> None:
        if use_color is None:
            use_color = os.getenv("LOGGER_COLOR", "1") not in ("0", "false", "False")
        self._time_fmt = time_fmt
        self._use_color = use_color
        self._name_width = name_width

    def create_formatter(self) -> logging.Formatter:
        return CompactStyle._Formatter(
            time_fmt=self._time_fmt,
            use_color=self._use_color,
            name_width=self._name_width,
        )


def apply_style(logger: logging.Logger, style: LoggerStyle) -> None:
    """Apply a style to all stream handlers on this logger (and create one if missing)."""
    # Find or create a StreamHandler
    stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    if not stream_handlers:
        h = logging.StreamHandler(stream=sys.stdout)
        logger.addHandler(h)
        stream_handlers = [h]
    for h in stream_handlers:
        style.apply(h)
