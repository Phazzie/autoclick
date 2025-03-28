"""Tests for the GUI command"""
import unittest
from unittest.mock import patch, MagicMock
import argparse

# We'll implement this module next
from src.cli.commands.gui import gui_command


class TestGuiCommand(unittest.TestCase):
    """Test cases for the GUI command"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.args = argparse.Namespace(
            verbose=False,
            quiet=False,
            theme="default"
        )

    @patch("src.cli.commands.gui.SimpleGUI")
    def test_gui_command(self, mock_simple_gui: MagicMock) -> None:
        """Test the GUI command"""
        # Create a mock GUI instance
        mock_gui_instance = MagicMock()
        mock_simple_gui.return_value = mock_gui_instance
        
        # Call the GUI command
        result = gui_command(self.args)
        
        # Verify the GUI was created
        mock_simple_gui.assert_called_once_with(theme="default")
        
        # Verify the GUI was started
        mock_gui_instance.start.assert_called_once()
        
        # Verify the command returned success
        self.assertEqual(result, 0)

    @patch("src.cli.commands.gui.SimpleGUI")
    def test_gui_command_with_theme(self, mock_simple_gui: MagicMock) -> None:
        """Test the GUI command with a custom theme"""
        # Set a custom theme
        self.args.theme = "dark"
        
        # Create a mock GUI instance
        mock_gui_instance = MagicMock()
        mock_simple_gui.return_value = mock_gui_instance
        
        # Call the GUI command
        result = gui_command(self.args)
        
        # Verify the GUI was created with the custom theme
        mock_simple_gui.assert_called_once_with(theme="dark")
        
        # Verify the GUI was started
        mock_gui_instance.start.assert_called_once()
        
        # Verify the command returned success
        self.assertEqual(result, 0)

    @patch("src.cli.commands.gui.SimpleGUI")
    def test_gui_command_exception(self, mock_simple_gui: MagicMock) -> None:
        """Test the GUI command with an exception"""
        # Make the GUI raise an exception
        mock_simple_gui.side_effect = Exception("Test exception")
        
        # Call the GUI command
        result = gui_command(self.args)
        
        # Verify the command returned an error
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
