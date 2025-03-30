"""
Tests for the context menu component.
SOLID: Single responsibility - testing context menu.
KISS: Simple tests for context menu functionality.
"""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk

from src.ui.components.context_menu import ContextMenu

class TestContextMenu(unittest.TestCase):
    """Tests for the context menu component."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a root window
        self.root = tk.Tk()
        
        # Create a context menu
        self.context_menu = ContextMenu(self.root)
    
    def tearDown(self):
        """Clean up after the test."""
        self.root.destroy()
    
    def test_add_command(self):
        """Test adding a command to the context menu."""
        # Create a mock command
        mock_command = MagicMock()
        
        # Add a command
        self.context_menu.add_command("Test Command", mock_command)
        
        # Check that the command was added
        self.assertEqual(len(self.context_menu.items), 1)
        self.assertEqual(self.context_menu.items[0]["type"], "command")
        self.assertEqual(self.context_menu.items[0]["label"], "Test Command")
        self.assertEqual(self.context_menu.items[0]["command"], mock_command)
        self.assertEqual(self.context_menu.items[0]["enabled"], True)
        self.assertEqual(self.context_menu.items[0]["icon"], None)
    
    def test_add_separator(self):
        """Test adding a separator to the context menu."""
        # Add a separator
        self.context_menu.add_separator()
        
        # Check that the separator was added
        self.assertEqual(len(self.context_menu.items), 1)
        self.assertEqual(self.context_menu.items[0]["type"], "separator")
    
    def test_add_submenu(self):
        """Test adding a submenu to the context menu."""
        # Create a submenu
        submenu = ContextMenu(self.root)
        submenu.add_command("Submenu Command", MagicMock())
        
        # Add the submenu
        self.context_menu.add_submenu("Test Submenu", submenu)
        
        # Check that the submenu was added
        self.assertEqual(len(self.context_menu.items), 1)
        self.assertEqual(self.context_menu.items[0]["type"], "submenu")
        self.assertEqual(self.context_menu.items[0]["label"], "Test Submenu")
        self.assertEqual(self.context_menu.items[0]["submenu"], submenu)
        self.assertEqual(self.context_menu.items[0]["enabled"], True)
        self.assertEqual(self.context_menu.items[0]["icon"], None)
    
    def test_clear(self):
        """Test clearing the context menu."""
        # Add some items
        self.context_menu.add_command("Test Command", MagicMock())
        self.context_menu.add_separator()
        
        # Clear the menu
        self.context_menu.clear()
        
        # Check that the menu was cleared
        self.assertEqual(len(self.context_menu.items), 0)
    
    @patch('tkinter.Menu.tk_popup')
    def test_show(self, mock_tk_popup):
        """Test showing the context menu."""
        # Add a command
        self.context_menu.add_command("Test Command", MagicMock())
        
        # Show the menu
        self.context_menu.show(100, 100)
        
        # Check that tk_popup was called
        mock_tk_popup.assert_called_once_with(100, 100)

if __name__ == "__main__":
    unittest.main()
