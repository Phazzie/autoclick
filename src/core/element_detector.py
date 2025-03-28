"""Element detection and interaction for web automation"""
import logging
import re
import time
from typing import Any, Dict, List, Optional, Tuple, Union

from src.utils.debug_utils import debug_trace, exception_handler
from src.utils.selenium_utils import (
    SELENIUM_AVAILABLE,
    check_selenium_availability,
    require_selenium,
)

# This is a placeholder until we add the selenium dependency
try:
    from selenium.common.exceptions import (
        NoSuchElementException,
        StaleElementReferenceException,
        TimeoutException,
    )
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait
except ImportError:
    # These will be handled by the selenium_utils module
    pass


class ElementDetector:
    """Detects and interacts with web elements"""

    # Supported selector types
    SELECTOR_TYPES = {
        "css": By.CSS_SELECTOR,
        "xpath": By.XPATH,
        "id": By.ID,
        "name": By.NAME,
        "tag": By.TAG_NAME,
        "class": By.CLASS_NAME,
        "link_text": By.LINK_TEXT,
        "partial_link_text": By.PARTIAL_LINK_TEXT,
    }

    def __init__(self, driver: Any, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the element detector

        Args:
            driver: WebDriver instance
            config: Configuration dictionary
        """
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.config = config or {}
        self.default_timeout = self.config.get("timeout", 10)

        # Check if Selenium is available
        check_selenium_availability(self.logger)

    @debug_trace
    def find_element(self, selector: str, timeout: Optional[int] = None) -> Any:
        """
        Find an element using the selector

        Args:
            selector: Element selector (format: "type:value")
            timeout: Timeout in seconds (default: from config)

        Returns:
            WebElement if found, None otherwise

        Raises:
            ValueError: If selector format is invalid
            TimeoutException: If element is not found within timeout
        """
        # Ensure Selenium is available
        require_selenium()

        selector_type, selector_value = self._parse_selector(selector)
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((selector_type, selector_value))
            )
            return element
        except TimeoutException:
            self.logger.warning(
                f"Element not found with selector {selector} "
                f"within {timeout} seconds"
            )
            raise

    @debug_trace
    def find_elements(self, selector: str, timeout: Optional[int] = None) -> List[Any]:
        """
        Find all elements matching the selector

        Args:
            selector: Element selector (format: "type:value")
            timeout: Timeout in seconds (default: from config)

        Returns:
            List of WebElements

        Raises:
            ValueError: If selector format is invalid
        """
        if not SELENIUM_AVAILABLE:
            raise RuntimeError(
                "Selenium is required but not installed. "
                "Please install it with: pip install selenium"
            )

        selector_type, selector_value = self._parse_selector(selector)
        timeout = timeout or self.default_timeout

        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((selector_type, selector_value))
            )
            return elements
        except TimeoutException:
            self.logger.warning(
                f"No elements found with selector {selector} "
                f"within {timeout} seconds"
            )
            return []

    @debug_trace
    def wait_for_element_visible(
        self, selector: str, timeout: Optional[int] = None
    ) -> Any:
        """
        Wait for an element to be visible

        Args:
            selector: Element selector (format: "type:value")
            timeout: Timeout in seconds (default: from config)

        Returns:
            WebElement if visible, None otherwise

        Raises:
            ValueError: If selector format is invalid
            TimeoutException: If element is not visible within timeout
        """
        if not SELENIUM_AVAILABLE:
            raise RuntimeError(
                "Selenium is required but not installed. "
                "Please install it with: pip install selenium"
            )

        selector_type, selector_value = self._parse_selector(selector)
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((selector_type, selector_value))
            )
            return element
        except TimeoutException:
            self.logger.warning(
                f"Element not visible with selector {selector} "
                f"within {timeout} seconds"
            )
            raise

    @debug_trace
    def wait_for_element_clickable(
        self, selector: str, timeout: Optional[int] = None
    ) -> Any:
        """
        Wait for an element to be clickable

        Args:
            selector: Element selector (format: "type:value")
            timeout: Timeout in seconds (default: from config)

        Returns:
            WebElement if clickable, None otherwise

        Raises:
            ValueError: If selector format is invalid
            TimeoutException: If element is not clickable within timeout
        """
        if not SELENIUM_AVAILABLE:
            raise RuntimeError(
                "Selenium is required but not installed. "
                "Please install it with: pip install selenium"
            )

        selector_type, selector_value = self._parse_selector(selector)
        timeout = timeout or self.default_timeout

        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((selector_type, selector_value))
            )
            return element
        except TimeoutException:
            self.logger.warning(
                f"Element not clickable with selector {selector} "
                f"within {timeout} seconds"
            )
            raise

    def _parse_selector(self, selector: str) -> Tuple[str, str]:
        """
        Parse a selector string into type and value

        Args:
            selector: Selector string (format: "type:value")

        Returns:
            Tuple of (selector_type, selector_value)

        Raises:
            ValueError: If selector format is invalid
        """
        if ":" not in selector:
            # Default to CSS selector if type not specified
            return By.CSS_SELECTOR, selector

        parts = selector.split(":", 1)
        selector_type = parts[0].lower()
        selector_value = parts[1]

        if selector_type not in self.SELECTOR_TYPES:
            raise ValueError(
                f"Invalid selector type: {selector_type}. "
                f"Supported types: {', '.join(self.SELECTOR_TYPES.keys())}"
            )

        return self.SELECTOR_TYPES[selector_type], selector_value
