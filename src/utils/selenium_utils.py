"""Utility functions for Selenium WebDriver"""
import logging
from typing import Any, Optional

# This is a placeholder until we add the selenium dependency
try:
    from selenium import webdriver

    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False


def check_selenium_availability(logger: Optional[logging.Logger] = None) -> None:
    """
    Check if Selenium is available and log a warning if not

    Args:
        logger: Logger to use for warnings (optional)
    """
    if not SELENIUM_AVAILABLE and logger:
        logger.warning(
            "Selenium not available. Please install it with: pip install selenium"
        )


def require_selenium() -> None:
    """
    Raise an error if Selenium is not available

    Raises:
        RuntimeError: If Selenium is not installed
    """
    if not SELENIUM_AVAILABLE:
        raise RuntimeError(
            "Selenium is required but not installed. "
            "Please install it with: pip install selenium"
        )
