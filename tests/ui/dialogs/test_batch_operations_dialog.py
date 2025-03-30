"""
Tests for the batch operations dialog.
SOLID: Single responsibility - testing batch operations dialog.
KISS: Simple tests for batch operations dialog functionality.
"""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk

from src.ui.dialogs.batch_operations_dialog import BatchOperationsDialog

class TestBatchOperationsDialog(unittest.TestCase):
    """Tests for the batch operations dialog."""
    
    def setUp(self):
        """Set up the test environment."""
        # Create a root window
        self.root = ctk.CTk()
        
        # Create a mock parent
        self.mock_parent = MagicMock()
        
        # Patch the wait_window method to avoid blocking
        self.wait_window_patcher = patch.object(BatchOperationsDialog, '_create_dialog')
        self.mock_create_dialog = self.wait_window_patcher.start()
        
        # Create the dialog
        self.dialog = BatchOperationsDialog(self.mock_parent)
        
        # Set up the dialog attributes manually
        self.dialog.operation_var = tk.StringVar(value="update_status")
        self.dialog.target_var = tk.StringVar(value="Inactive")
        self.dialog.new_var = tk.StringVar(value="Active")
    
    def tearDown(self):
        """Clean up after the test."""
        self.wait_window_patcher.stop()
        self.root.destroy()
    
    def test_init(self):
        """Test initialization."""
        # Verify the dialog was created with the correct parent
        self.assertEqual(self.dialog.parent, self.mock_parent)
        
        # Verify the result is initially False
        self.assertEqual(self.dialog.result, False)
        
        # Verify the operation, target status, and new status are None
        self.assertEqual(self.dialog.operation, None)
        self.assertEqual(self.dialog.target_status, None)
        self.assertEqual(self.dialog.new_status, None)
    
    def test_on_operation_changed_update(self):
        """Test operation changed to update."""
        # Set up the dialog
        self.dialog.operation_var.set("update_status")
        self.dialog.new_label = MagicMock()
        self.dialog.new_dropdown = MagicMock()
        self.dialog.warning_label = MagicMock()
        
        # Call the method
        self.dialog._on_operation_changed()
        
        # Verify the new status field is shown
        self.dialog.new_label.grid.assert_called_once()
        self.dialog.new_dropdown.grid.assert_called_once()
        
        # Verify the warning message is updated
        self.dialog.warning_label.configure.assert_called_once()
    
    def test_on_operation_changed_delete(self):
        """Test operation changed to delete."""
        # Set up the dialog
        self.dialog.operation_var.set("delete")
        self.dialog.new_label = MagicMock()
        self.dialog.new_dropdown = MagicMock()
        self.dialog.warning_label = MagicMock()
        
        # Call the method
        self.dialog._on_operation_changed()
        
        # Verify the new status field is hidden
        self.dialog.new_label.grid_remove.assert_called_once()
        self.dialog.new_dropdown.grid_remove.assert_called_once()
        
        # Verify the warning message is updated
        self.dialog.warning_label.configure.assert_called_once()
    
    def test_on_cancel(self):
        """Test cancel button click."""
        # Set up the dialog
        self.dialog.dialog = MagicMock()
        
        # Call the method
        self.dialog._on_cancel()
        
        # Verify the result is False
        self.assertEqual(self.dialog.result, False)
        
        # Verify the dialog was destroyed
        self.dialog.dialog.destroy.assert_called_once()
    
    def test_on_ok(self):
        """Test OK button click."""
        # Set up the dialog
        self.dialog.dialog = MagicMock()
        self.dialog.operation_var.set("update_status")
        self.dialog.target_var.set("Inactive")
        self.dialog.new_var.set("Active")
        
        # Call the method
        self.dialog._on_ok()
        
        # Verify the result is True
        self.assertEqual(self.dialog.result, True)
        
        # Verify the operation, target status, and new status are set
        self.assertEqual(self.dialog.operation, "update_status")
        self.assertEqual(self.dialog.target_status, "Inactive")
        self.assertEqual(self.dialog.new_status, "Active")
        
        # Verify the dialog was destroyed
        self.dialog.dialog.destroy.assert_called_once()

if __name__ == "__main__":
    unittest.main()
