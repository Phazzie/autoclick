"""Tests for the ElementModel class"""
import unittest
from src.ui.models.element_model import ElementModel


class TestElementModel(unittest.TestCase):
    """Test cases for the ElementModel class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.model = ElementModel()
        self.test_element = {
            "tag_name": "button",
            "id": "submit-button",
            "class": "btn btn-primary",
            "text": "Submit"
        }

    def test_set_url(self) -> None:
        """Test setting URL"""
        # Set URL
        self.model.set_url("https://example.com")
        
        # Verify URL
        self.assertEqual(self.model.url, "https://example.com")

    def test_get_url(self) -> None:
        """Test getting URL"""
        # Set URL
        self.model.url = "https://example.com"
        
        # Get URL
        url = self.model.get_url()
        
        # Verify URL
        self.assertEqual(url, "https://example.com")

    def test_set_selected_element(self) -> None:
        """Test setting selected element"""
        # Set selected element
        self.model.set_selected_element(self.test_element)
        
        # Verify selected element
        self.assertEqual(self.model.selected_element, self.test_element)

    def test_get_selected_element(self) -> None:
        """Test getting selected element"""
        # Set selected element
        self.model.selected_element = self.test_element
        
        # Get selected element
        element = self.model.get_selected_element()
        
        # Verify selected element
        self.assertEqual(element, self.test_element)
        
        # Verify that modifying the returned element doesn't affect the original
        element["tag_name"] = "div"
        self.assertEqual(self.model.selected_element["tag_name"], "button")

    def test_get_selected_element_none(self) -> None:
        """Test getting selected element when none is selected"""
        # Get selected element
        element = self.model.get_selected_element()
        
        # Verify selected element is None
        self.assertIsNone(element)

    def test_clear_selected_element(self) -> None:
        """Test clearing selected element"""
        # Set selected element
        self.model.selected_element = self.test_element
        
        # Clear selected element
        self.model.clear_selected_element()
        
        # Verify selected element is None
        self.assertIsNone(self.model.selected_element)

    def test_set_browser_type(self) -> None:
        """Test setting browser type"""
        # Set browser type
        self.model.set_browser_type("firefox")
        
        # Verify browser type
        self.assertEqual(self.model.browser_type, "firefox")

    def test_set_headless(self) -> None:
        """Test setting headless mode"""
        # Set headless mode
        self.model.set_headless(True)
        
        # Verify headless mode
        self.assertTrue(self.model.headless)


if __name__ == "__main__":
    unittest.main()
