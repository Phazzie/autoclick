"""Tests for the Tooltip class"""
import unittest
from unittest.mock import MagicMock, patch

from src.ui.components.tooltip import Tooltip


class TestTooltip(unittest.TestCase):
    """Test cases for the Tooltip class"""

    def setUp(self) -> None:
        """Set up test fixtures"""
        self.widget = MagicMock()
        self.tooltip = Tooltip(self.widget, "Test tooltip")

    def test_initialization(self) -> None:
        """Test initialization"""
        # Verify widget bindings
        self.widget.bind.assert_any_call("<Enter>", self.tooltip._on_enter)
        self.widget.bind.assert_any_call("<Leave>", self.tooltip._on_leave)
        self.widget.bind.assert_any_call("<ButtonPress>", self.tooltip._on_leave)

        # Verify initial state
        self.assertEqual(self.tooltip.text, "Test tooltip")
        self.assertEqual(self.tooltip.delay, 500)
        self.assertEqual(self.tooltip.wrap_length, 180)
        self.assertEqual(self.tooltip.background, "#ffffe0")
        self.assertEqual(self.tooltip.foreground, "black")
        self.assertEqual(self.tooltip.font, ("TkDefaultFont", 9, "normal"))
        self.assertIsNone(self.tooltip.tooltip_window)
        self.assertIsNone(self.tooltip.scheduled_id)

    def test_on_enter(self) -> None:
        """Test mouse enter event"""
        # Mock after method
        self.widget.after.return_value = 123

        # Trigger enter event
        self.tooltip._on_enter()

        # Verify scheduled ID
        self.assertEqual(self.tooltip.scheduled_id, 123)

        # Verify after was called with correct delay
        self.widget.after.assert_called_once_with(
            500,
            self.tooltip._show_tooltip
        )

    def test_on_leave(self) -> None:
        """Test mouse leave event"""
        # Set up scheduled ID
        self.tooltip.scheduled_id = 123

        # Mock tooltip window
        tooltip_window_mock = MagicMock()
        self.tooltip.tooltip_window = tooltip_window_mock

        # Trigger leave event
        self.tooltip._on_leave()

        # Verify scheduled ID was cancelled
        self.widget.after_cancel.assert_called_once_with(123)
        self.assertIsNone(self.tooltip.scheduled_id)

        # Verify tooltip window was destroyed
        tooltip_window_mock.destroy.assert_called_once()
        self.assertIsNone(self.tooltip.tooltip_window)

    def test_cancel_scheduled(self) -> None:
        """Test cancelling scheduled tooltip"""
        # Set up scheduled ID
        self.tooltip.scheduled_id = 123

        # Cancel scheduled tooltip
        self.tooltip._cancel_scheduled()

        # Verify scheduled ID was cancelled
        self.widget.after_cancel.assert_called_once_with(123)
        self.assertIsNone(self.tooltip.scheduled_id)

    @patch("tkinter.Toplevel")
    @patch("tkinter.Label")
    def test_show_tooltip(
        self,
        mock_label: MagicMock,
        mock_toplevel: MagicMock
    ) -> None:
        """Test showing tooltip"""
        # Mock widget position
        self.widget.bbox.return_value = (10, 20, 30, 40)
        self.widget.winfo_rootx.return_value = 100
        self.widget.winfo_rooty.return_value = 200

        # Show tooltip
        self.tooltip._show_tooltip()

        # Verify tooltip window was created
        mock_toplevel.assert_called_once_with(self.widget)

        # Verify tooltip window properties
        toplevel_instance = mock_toplevel.return_value
        toplevel_instance.wm_overrideredirect.assert_called_once_with(True)
        toplevel_instance.wm_geometry.assert_called_once_with("+135+245")

        # Verify label was created with correct properties
        mock_label.assert_called_once_with(
            toplevel_instance,
            text="Test tooltip",
            justify=unittest.mock.ANY,
            background="#ffffe0",
            foreground="black",
            relief=unittest.mock.ANY,
            borderwidth=1,
            wraplength=180,
            font=("TkDefaultFont", 9, "normal")
        )

        # Verify label was packed
        label_instance = mock_label.return_value
        label_instance.pack.assert_called_once_with(padx=3, pady=3)

    def test_hide_tooltip(self) -> None:
        """Test hiding tooltip"""
        # Mock tooltip window
        tooltip_window_mock = MagicMock()
        self.tooltip.tooltip_window = tooltip_window_mock

        # Hide tooltip
        self.tooltip._hide_tooltip()

        # Verify tooltip window was destroyed
        tooltip_window_mock.destroy.assert_called_once()
        self.assertIsNone(self.tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
