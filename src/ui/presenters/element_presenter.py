"""Element presenter implementation"""
import logging
from typing import Any, Dict, Optional

from src.ui.models.element_model import ElementModel
from src.ui.interfaces.view_interface import ElementSelectorViewInterface


class ElementPresenter:
    """Presenter for element selector tab"""
    
    def __init__(self, model: ElementModel, view: Optional[ElementSelectorViewInterface] = None) -> None:
        """
        Initialize the element presenter
        
        Args:
            model: Element model
            view: Element selector view
        """
        self.logger = logging.getLogger(__name__)
        self.model = model
        self.view = view
    
    def set_view(self, view: ElementSelectorViewInterface) -> None:
        """
        Set the view
        
        Args:
            view: Element selector view
        """
        self.view = view
    
    def select_element(self) -> None:
        """Select an element on a webpage"""
        self.logger.info("Selecting element")
        
        if not self.view:
            return
        
        try:
            # Get the URL from the view
            url = self.view.get_url()
            
            if not url:
                self.view.show_message("Please enter a URL")
                return
            
            # Update the model
            self.model.set_url(url)
            
            # In a real implementation, this would launch a browser and select an element
            # For now, we'll just simulate selecting an element
            element = {
                "tag_name": "button",
                "id": "submit-button",
                "class": "btn btn-primary",
                "text": "Submit",
                "attributes": {
                    "type": "submit",
                    "name": "submit",
                    "data-test": "submit-button"
                }
            }
            
            # Update the model
            self.model.set_selected_element(element)
            
            # Refresh the view
            self.refresh_view()
            
            self.view.show_message("Element selected")
        except Exception as e:
            self.logger.error(f"Error selecting element: {str(e)}")
            self.view.show_message(f"Error selecting element: {str(e)}")
    
    def clear_selected_element(self) -> None:
        """Clear the selected element"""
        self.logger.info("Clearing selected element")
        
        self.model.clear_selected_element()
        self.refresh_view()
        
        if self.view:
            self.view.show_message("Selected element cleared")
    
    def set_browser_type(self, browser_type: str) -> None:
        """
        Set the browser type
        
        Args:
            browser_type: The browser type (chrome, firefox, edge)
        """
        self.logger.info(f"Setting browser type to {browser_type}")
        
        self.model.set_browser_type(browser_type)
        
        if self.view:
            self.view.show_message(f"Browser type set to {browser_type}")
    
    def set_headless(self, headless: bool) -> None:
        """
        Set headless mode
        
        Args:
            headless: Whether to use headless mode
        """
        self.logger.info(f"Setting headless mode to {headless}")
        
        self.model.set_headless(headless)
        
        if self.view:
            self.view.show_message(f"Headless mode {'enabled' if headless else 'disabled'}")
    
    def refresh_view(self) -> None:
        """Refresh the view with current model data"""
        self.logger.debug("Refreshing element selector view")
        
        if not self.view:
            return
        
        element = self.model.get_selected_element()
        
        if element:
            # Convert element to properties dictionary
            properties = {}
            
            # Add basic properties
            for key, value in element.items():
                if key != "attributes":
                    properties[key] = value
            
            # Add attributes
            if "attributes" in element:
                for key, value in element["attributes"].items():
                    properties[f"attribute:{key}"] = value
            
            # Update the view
            self.view.display_element_properties(properties)
        else:
            # Clear the view
            self.view.display_element_properties({})
