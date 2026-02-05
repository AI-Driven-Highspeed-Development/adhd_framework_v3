import logging
import os
import sys
import threading
import fcntl
import atexit
import queue
from logging.handlers import QueueHandler, QueueListener
from typing import Optional, Dict
from datetime import datetime
from .logger_style import LoggerStyle, NormalStyle
from .compact_style import CompactStyle, apply_style as apply_style_to_logger

"""
Internal registry to ensure one Logger wrapper per name.
"""
_LOGGER_REGISTRY: Dict[str, "Logger"] = {}
_REGISTRY_LOCK = threading.Lock()

DEFAULT_LOG_DIR = "logs"  # Default directory for log files; can be overridden via LOG_FILE_PATH_OVERRIDE
LOG_TO_FILE_OVERRIDE = False  # Set to True to force all loggers to log to file, False to respect individual settings
LOG_FILE_PATH_OVERRIDE: Optional[str] = None  # Set to a file path string to override all loggers' file paths
LEVEL_OVERRIDE: Optional[str] = None  # Set to a logging level string (e.g., "DEBUG") to override all loggers' levels

class ConcurrentFileHandler(logging.FileHandler):
    """
    FileHandler that uses fcntl to ensure process safety on Linux.
    Acquires an exclusive lock before writing and releases it immediately after.
    """
    def __init__(self, filename, mode='a', encoding=None, delay=False, use_lock=True):
        super().__init__(filename, mode, encoding, delay)
        self.use_lock = use_lock

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            
            # Acquire process lock (blocking)
            if self.use_lock:
                fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
            try:
                stream.write(msg + self.terminator)
                self.flush()
            finally:
                # Release process lock
                if self.use_lock:
                    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
        except Exception:
            self.handleError(record)

class Logger:
    """
    A centralized logger utility with pluggable styles (NormalStyle, CompactStyle).
    Per-name singleton: Logger(name="X") always returns the same wrapper.
    """
    
    def __new__(cls,
                name: str = "Logger",
                *args,
                **kwargs):
        """Return an existing wrapper for the same name, or create one."""
        # Determine registry key from provided name
        key = name
        with _REGISTRY_LOCK:
            inst = _LOGGER_REGISTRY.get(key)
            if inst is None:
                inst = super().__new__(cls)
                _LOGGER_REGISTRY[key] = inst
            return inst

    def __init__(self, 
                 name: str = "Logger",
                 level: Optional[str] = None, 
                 log_to_file: Optional[bool] = None,
                 log_file_path: Optional[str] = None,
                 verbose: Optional[bool] = None,
                 style: Optional[LoggerStyle] = None):
        """
        First construction initializes internals.
        Subsequent constructions with same name reuse the instance and, if any params are provided,
        reconfigure it via configure(...).
        """
        first_init = not hasattr(self, "_initialized")
        if first_init:
            # Immutable identity
            self.name = name
            # Defaults
            self.level = logging.INFO 
            self.log_to_file = False
            self.log_file_path = f"{DEFAULT_LOG_DIR}/{name}_{datetime.now().strftime('%Y%m%d')}.log"
            self.style = CompactStyle()
            # Underlying stdlib logger
            self.logger = logging.getLogger(self.name)
            self.logger.propagate = False  # Prevent duplicate logs from parent/root handlers
            self._initialized = True

        # Apply configuration on first init or when any parameters are provided
        if any(p is not None for p in (level, log_to_file, log_file_path, verbose, style)) or first_init:
            self.configure(level=level,
                           log_to_file=log_to_file,
                           log_file_path=log_file_path,
                           verbose=verbose,
                           style=style)

    def configure(self,
                  *,
                  level: Optional[str] = None,
                  log_to_file: Optional[bool] = None,
                  log_file_path: Optional[str] = None,
                  verbose: Optional[bool] = None,
                  style: Optional[LoggerStyle] = None) -> None:
        """Reconfigure logger settings and rebuild handlers."""
        # Resolve effective level
        self.level = self._effective_level(current=self.level, level=level, verbose=verbose)
        self.logger.setLevel(self.level)

        # Update other settings only if provided
        if log_to_file is not None:
            self.log_to_file = log_to_file
        if log_file_path is not None:
            self.log_file_path = log_file_path
        if style is not None:
            self.style = style

        # Rebuild handlers to reflect new config
        self._rebuild_handlers()

    @staticmethod
    def _effective_level(current: int, level: Optional[str], verbose: Optional[bool]) -> int:
        """Resolve new level from current, level string, and verbose flag."""
        if LEVEL_OVERRIDE:
            return getattr(logging, LEVEL_OVERRIDE.upper(), logging.INFO)

        eff = current
        if level is not None:
            eff = getattr(logging, level.upper(), logging.INFO)
        if verbose is True:
            eff = logging.DEBUG
        return eff

    def _rebuild_handlers(self) -> None:
        """Clear handlers, apply console style, and optional file handler."""
        # Stop existing listener if it exists to prevent resource leaks
        if hasattr(self, "_listener") and self._listener:
            self._listener.stop()
            self._listener = None

        self.logger.handlers.clear()
        self._setup_console_handler()
        if self.log_to_file or LOG_TO_FILE_OVERRIDE:
            self._setup_file_handler()
    
    def _setup_console_handler(self):
        """Setup console handler for logging to stdout and apply style."""
        # A stream handler will be created by apply_style_to_logger if missing
        apply_style_to_logger(self.logger, self.style)
        
    def _setup_file_handler(self):
        """Setup file handler for logging to file with normal verbose formatter."""
        target_path = LOG_FILE_PATH_OVERRIDE if LOG_FILE_PATH_OVERRIDE else self.log_file_path

        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(target_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        # 1. Create the blocking file handler (but don't attach it to logger directly)
        file_handler = ConcurrentFileHandler(target_path, use_lock=True)
        file_handler.setLevel(self.level)
        formatter = NormalStyle().create_formatter()
        file_handler.setFormatter(formatter)
        
        # 2. Create a Queue and a QueueHandler
        log_queue = queue.Queue(-1) # Infinite queue
        queue_handler = QueueHandler(log_queue)
        queue_handler.setLevel(self.level)
        
        # 3. Create and start the listener in a background thread
        # The listener reads from queue -> writes to file_handler (blocking happens here)
        self._listener = QueueListener(log_queue, file_handler)
        self._listener.start()
        
        # 4. Ensure listener stops on exit to flush logs
        atexit.register(self._listener.stop)
        
        # 5. Attach the non-blocking QueueHandler to the logger
        self.logger.addHandler(queue_handler)
    
    def get_logger(self) -> logging.Logger:
        """
        Get the underlying standard logging.Logger instance.
        
        Returns:
            logging.Logger: The underlying logger
        """
        return self.logger

    def set_style(self, style: LoggerStyle) -> None:
        """Change the console style at runtime for this logger."""
        self.style = style
        apply_style_to_logger(self.logger, self.style)
    
    def debug(self, message: str):
        """Log a debug message."""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log an error message."""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log a critical message."""
        self.logger.critical(message)
    
    def set_level(self, level: str):
        """
        Change the logging level.
        
        Args:
            level (str): New logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        self.configure(level=level)
    
    def add_custom_handler(self, handler: logging.Handler):
        """
        Add a custom handler to the logger.
        
        Args:
            handler (logging.Handler): Custom handler to add
        """
        self.logger.addHandler(handler)
    
    def remove_all_handlers(self):
        """Remove all handlers from the logger."""
        self.logger.handlers.clear()


# Global centralized logger instance for debugging and special purposes
_central_logger = None

def get_central_logger(verbose: bool = False, log_to_file: bool = True) -> logging.Logger:
    """
    Get the centralized "mother of all loggers" for debugging and special purposes.
    This is a singleton logger that you can throw anything at.
    
    Args:
        verbose (bool): Enable verbose logging
        log_to_file (bool): Enable file logging (default True for central logger)
        
    Returns:
        logging.Logger: The centralized logger instance
    """
    global _central_logger
    if _central_logger is None:
        logger_instance = Logger(
            name="CENTRAL",
            verbose=verbose,
            log_to_file=log_to_file,
            log_file_path=f"{DEFAULT_LOG_DIR}/central_{datetime.now().strftime('%Y%m%d')}.log"
        )
        _central_logger = logger_instance.get_logger()
    return _central_logger


def set_logger_style(logger, style: Optional[LoggerStyle] = None) -> None:
    """Apply a console style to a logger (wrapper or std logging.Logger). Defaults to CompactStyle."""
    target = logger
    # Allow passing our Logger wrapper or a std logging.Logger
    if isinstance(logger, Logger):
        target = logger.get_logger()
    apply_style_to_logger(target, style or CompactStyle())

# Convenience functions for central logger - no-brainer logging
def log_debug(message: str):
    """Quick debug logging to central logger."""
    get_central_logger(verbose=True).debug(message)

def log_info(message: str):
    """Quick info logging to central logger."""
    get_central_logger().info(message)

def log_warning(message: str):
    """Quick warning logging to central logger."""
    get_central_logger().warning(message)

def log_error(message: str):
    """Quick error logging to central logger."""
    get_central_logger().error(message)

def log_critical(message: str):
    """Quick critical logging to central logger."""
    get_central_logger().critical(message)