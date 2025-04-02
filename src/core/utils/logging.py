"""
Logging utilities for the application.

This module provides utilities for logging across the application.
Part of the error handling refactoring to standardize logging.

SRP-1: Provides logging utilities
"""
import logging
from typing import Optional


class LoggingMixin:
    """
    Mixin for classes that need logging.

    Part of the error handling refactoring to standardize
    logging across the application.

    SRP Analysis: This mixin adds logging responsibility to classes,
    but since logging is a cross-cutting concern, it doesn't violate SRP.
    It standardizes how logging is handled without adding business logic.
    """

    def __init_logger__(self):
        """Initialize the logger for this class."""
        self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def _ensure_logger(self):
        """Ensure that the logger is initialized."""
        if not hasattr(self, '_logger'):
            self.__init_logger__()
            if not hasattr(self, '_logger'):
                # Fallback if __init_logger__ doesn't set _logger
                import logging
                self._logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

    def log_info(self, message: str):
        """Log an info message."""
        self._ensure_logger()
        self._logger.info(message)

    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log an error message."""
        self._ensure_logger()

        if exception:
            self._logger.error(f"{message}: {str(exception)}")
        else:
            self._logger.error(message)

    def log_warning(self, message: str):
        """Log a warning message."""
        self._ensure_logger()
        self._logger.warning(message)

    def log_debug(self, message: str):
        """Log a debug message."""
        self._ensure_logger()
        self._logger.debug(message)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.

    Args:
        name: Name of the logger

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def create_formatter() -> logging.Formatter:
    """
    Create a standard formatter for log messages.

    Returns:
        Formatter instance
    """
    return logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def configure_logging(level: int = logging.INFO, log_file: Optional[str] = None):
    """
    Configure logging for the application.

    Args:
        level: Logging level
        log_file: Optional log file path
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Create formatter
    formatter = create_formatter()

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Add console handler to root logger
    root_logger.addHandler(console_handler)

    # Add file handler if log_file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
