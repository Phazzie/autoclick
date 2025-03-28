"""Model for element selection"""
from typing import Dict, Any, Optional


class ElementModel:
    """Model for element selection"""
    
    def __init__(self) -> None:
        """Initialize the element model"""
        self.url: str = ""
        self.selected_element: Optional[Dict[str, Any]] = None
        self.browser_type: str = "chrome"
        self.headless: bool = False
    
    def set_url(self, url: str) -> None:
        """
        Set the URL
        
        Args:
            url: The URL to navigate to
        """
        self.url = url
    
    def get_url(self) -> str:
        """
        Get the URL
        
        Returns:
            The URL
        """
        return self.url
    
    def set_selected_element(self, element: Dict[str, Any]) -> None:
        """
        Set the selected element
        
        Args:
            element: The selected element properties
        """
        self.selected_element = element
    
    def get_selected_element(self) -> Optional[Dict[str, Any]]:
        """
        Get the selected element
        
        Returns:
            The selected element properties, or None if no element is selected
        """
        return self.selected_element.copy() if self.selected_element else None
    
    def clear_selected_element(self) -> None:
        """Clear the selected element"""
        self.selected_element = None
    
    def set_browser_type(self, browser_type: str) -> None:
        """
        Set the browser type
        
        Args:
            browser_type: The browser type (chrome, firefox, edge)
        """
        self.browser_type = browser_type
    
    def set_headless(self, headless: bool) -> None:
        """
        Set headless mode
        
        Args:
            headless: Whether to use headless mode
        """
        self.headless = headless
