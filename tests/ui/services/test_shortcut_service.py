"""Tests for the ShortcutService class"""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.services.shortcut_service import ShortcutService


class TestShortcutService(unittest.TestCase):
    """Test cases for the ShortcutService class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.root = MagicMock()
        self.service = ShortcutService(self.root)
        self.test_callback = MagicMock()

    def test_register_shortcut(self) -> None:
        """Test registering a shortcut"""
        # Register a shortcut
        self.service.register_shortcut(
            "Control-s",
            self.test_callback,
            "Save"
        )
        
        # Verify the shortcut was registered
        self.assertIn("Control-s", self.service.shortcuts)
        self.assertEqual(
            self.service.shortcuts["Control-s"]["callback"],
            self.test_callback
        )
        self.assertEqual(
            self.service.shortcuts["Control-s"]["description"],
            "Save"
        )
        
        # Verify the shortcut was bound to the root window
        self.root.bind.assert_called_once_with(
            "<Control-s>",
            unittest.mock.ANY
        )

    def test_unregister_shortcut(self) -> None:
        """Test unregistering a shortcut"""
        # Register a shortcut
        self.service.register_shortcut(
            "Control-s",
            self.test_callback,
            "Save"
        )
        
        # Unregister the shortcut
        self.service.unregister_shortcut("Control-s")
        
        # Verify the shortcut was unregistered
        self.assertNotIn("Control-s", self.service.shortcuts)
        
        # Verify the shortcut was unbound from the root window
        self.root.unbind.assert_called_once_with("<Control-s>")

    def test_get_all_shortcuts(self) -> None:
        """Test getting all shortcuts"""
        # Register shortcuts
        self.service.register_shortcut(
            "Control-s",
            self.test_callback,
            "Save"
        )
        self.service.register_shortcut(
            "Control-o",
            self.test_callback,
            "Open"
        )
        
        # Get all shortcuts
        shortcuts = self.service.get_all_shortcuts()
        
        # Verify shortcuts
        self.assertEqual(len(shortcuts), 2)
        self.assertEqual(shortcuts["Control-s"], "Save")
        self.assertEqual(shortcuts["Control-o"], "Open")

    @patch("tkinter.Toplevel")
    @patch("tkinter.Frame")
    @patch("tkinter.Label")
    @patch("tkinter.Listbox")
    @patch("tkinter.Button")
    def test_show_shortcuts_dialog(
        self,
        mock_button: MagicMock,
        mock_listbox: MagicMock,
        mock_label: MagicMock,
        mock_frame: MagicMock,
        mock_toplevel: MagicMock
    ) -> None:
        """Test showing shortcuts dialog"""
        # Register shortcuts
        self.service.register_shortcut(
            "Control-s",
            self.test_callback,
            "Save"
        )
        self.service.register_shortcut(
            "Control-o",
            self.test_callback,
            "Open"
        )
        
        # Show shortcuts dialog
        self.service.show_shortcuts_dialog()
        
        # Verify dialog was created
        mock_toplevel.assert_called_once_with(self.root)
        
        # Verify listbox was populated
        mock_listbox_instance = mock_listbox.return_value
        self.assertEqual(mock_listbox_instance.insert.call_count, 2)


if __name__ == "__main__":
    unittest.main()
