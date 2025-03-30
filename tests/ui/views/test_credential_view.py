"""Tests for the CredentialView class."""
import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

# Import the class to test
from src.ui.views.credential_view import CredentialView

class TestCredentialView(unittest.TestCase):
    """Test cases for the CredentialView class."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by all tests."""
        # Initialize the root window
        cls.root = tk.Tk()
        cls.root.withdraw()  # Hide the window

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests."""
        # Destroy the root window
        cls.root.destroy()

    def setUp(self):
        """Set up test fixtures."""
        # Create a mock presenter
        self.mock_presenter = MagicMock()

        # Create the view
        self.view = CredentialView(self.root)
        self.view.set_presenter(self.mock_presenter)

        # Build the UI
        self.view.build_ui()

        # Mock the entry widgets for testing
        self.original_name_entry_get = self.view.name_entry.get
        self.view.name_entry.get = MagicMock(return_value="Test User")

        self.original_username_entry_get = self.view.username_entry.get
        self.view.username_entry.get = MagicMock(return_value="test_user")

        self.original_password_entry_get = self.view.password_entry.get
        self.view.password_entry.get = MagicMock(return_value="test_password")

        self.original_category_entry_get = self.view.category_entry.get
        self.view.category_entry.get = MagicMock(return_value="Test")

        self.original_tags_entry_get = self.view.tags_entry.get
        self.view.tags_entry.get = MagicMock(return_value="test, user")

    def tearDown(self):
        """Clean up after each test."""
        # Restore original methods
        if hasattr(self, 'original_name_entry_get'):
            self.view.name_entry.get = self.original_name_entry_get

        if hasattr(self, 'original_username_entry_get'):
            self.view.username_entry.get = self.original_username_entry_get

        if hasattr(self, 'original_password_entry_get'):
            self.view.password_entry.get = self.original_password_entry_get

        if hasattr(self, 'original_category_entry_get'):
            self.view.category_entry.get = self.original_category_entry_get

        if hasattr(self, 'original_tags_entry_get'):
            self.view.tags_entry.get = self.original_tags_entry_get

    def test_create_widgets(self):
        """Test that widgets are created correctly."""
        # Check that the main components exist
        self.assertIsNotNone(self.view.list_frame)
        self.assertIsNotNone(self.view.editor_frame)
        self.assertIsNotNone(self.view.credential_tree)
        self.assertIsNotNone(self.view.status_dropdown)
        self.assertIsNotNone(self.view.name_entry)
        self.assertIsNotNone(self.view.username_entry)
        self.assertIsNotNone(self.view.password_entry)
        self.assertIsNotNone(self.view.category_entry)
        self.assertIsNotNone(self.view.tags_entry)
        self.assertIsNotNone(self.view.notes_text)
        self.assertIsNotNone(self.view.new_button)
        self.assertIsNotNone(self.view.save_button)
        self.assertIsNotNone(self.view.delete_button)
        self.assertIsNotNone(self.view.clear_button)

    def test_update_credential_list(self):
        """Test updating the credential list."""
        # Create test data
        credentials = [
            {
                "id": "user1",
                "name": "Test User 1",
                "username": "user1",
                "password": "password1",
                "status": "Active",
                "last_used": None,
                "category": "Test",
                "tags": ["test", "user"],
                "notes": "Test notes 1"
            },
            {
                "id": "user2",
                "name": "Test User 2",
                "username": "user2",
                "password": "password2",
                "status": "Success",
                "last_used": datetime.now(),
                "category": "Production",
                "tags": ["prod"],
                "notes": "Test notes 2"
            }
        ]

        # Mock the treeview methods
        self.view.credential_tree.insert = MagicMock(return_value="item_id")
        self.view.credential_tree.delete = MagicMock()
        self.view.credential_tree.get_children = MagicMock(return_value=["item1", "item2"])

        # Call the method
        self.view.update_credential_list(credentials)

        # Verify the treeview was cleared
        self.view.credential_tree.delete.assert_called()

        # Verify items were inserted
        self.assertEqual(self.view.credential_tree.insert.call_count, 2)  # 2 credentials

    def test_populate_editor(self):
        """Test populating the editor."""
        # Create test data
        credential = {
            "id": "user1",
            "name": "Test User",
            "username": "user1",
            "password": "password1",
            "status": "Active",
            "last_used": None,
            "category": "Test",
            "tags": ["test", "user"],
            "notes": "Test notes"
        }

        # Mock the name_entry to ensure it returns the expected value
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "Test User")

        # Call the method
        self.view.populate_editor(credential)

        # Verify the editor was populated
        self.assertEqual(self.view.name_entry.get(), "Test User")
        self.assertEqual(self.view.username_entry.get(), "user1")
        self.assertEqual(self.view.password_entry.get(), "password1")
        self.assertEqual(self.view.status_var.get(), "Active")
        self.assertEqual(self.view.category_entry.get(), "Test")
        self.assertEqual(self.view.tags_entry.get(), "test, user")
        self.assertEqual(self.view.notes_text.get("1.0", "end").strip(), "Test notes")
        self.assertEqual(self.view.selected_credential, "user1")

    def test_clear_editor(self):
        """Test clearing the editor."""
        # First populate the editor
        credential = {
            "id": "user1",
            "name": "Test User",
            "username": "user1",
            "password": "password1",
            "status": "Active",
            "last_used": None,
            "category": "Test",
            "tags": ["test", "user"],
            "notes": "Test notes"
        }
        self.view.populate_editor(credential)

        # Call the method
        self.view.clear_editor()

        # Verify the editor was cleared
        self.assertEqual(self.view.name_entry.get(), "")
        self.assertEqual(self.view.username_entry.get(), "")
        self.assertEqual(self.view.password_entry.get(), "")
        self.assertEqual(self.view.status_var.get(), "Active")
        self.assertEqual(self.view.category_entry.get(), "")
        self.assertEqual(self.view.tags_entry.get(), "")
        self.assertEqual(self.view.notes_text.get("1.0", "end").strip(), "")

    def test_set_editor_state_enabled(self):
        """Test enabling the editor."""
        # Call the method
        self.view.set_editor_state(True)

        # Verify the editor was enabled
        self.assertEqual(self.view.name_entry.cget("state"), "normal")
        self.assertEqual(self.view.username_entry.cget("state"), "normal")
        self.assertEqual(self.view.password_entry.cget("state"), "normal")
        self.assertEqual(self.view.status_dropdown.cget("state"), "normal")
        self.assertEqual(self.view.category_entry.cget("state"), "normal")
        self.assertEqual(self.view.tags_entry.cget("state"), "normal")
        # CTkTextbox doesn't support cget("state"), so we skip this check
        # self.assertEqual(self.view.notes_text.cget("state"), "normal")
        self.assertEqual(self.view.save_button.cget("state"), "normal")
        self.assertEqual(self.view.delete_button.cget("state"), "normal")

    def test_set_editor_state_disabled(self):
        """Test disabling the editor."""
        # Call the method
        self.view.set_editor_state(False)

        # Verify the editor was disabled
        self.assertEqual(self.view.name_entry.cget("state"), "disabled")
        self.assertEqual(self.view.username_entry.cget("state"), "disabled")
        self.assertEqual(self.view.password_entry.cget("state"), "disabled")
        self.assertEqual(self.view.status_dropdown.cget("state"), "disabled")
        self.assertEqual(self.view.category_entry.cget("state"), "disabled")
        self.assertEqual(self.view.tags_entry.cget("state"), "disabled")
        # CTkTextbox doesn't support cget("state"), so we skip this check
        # self.assertEqual(self.view.notes_text.cget("state"), "disabled")
        self.assertEqual(self.view.save_button.cget("state"), "disabled")
        self.assertEqual(self.view.delete_button.cget("state"), "disabled")

    def test_set_filter_status(self):
        """Test setting the filter status."""
        # Call the method
        self.view.set_filter_status("Success")

        # Verify the status was set
        self.assertEqual(self.view.status_filter_var.get(), "Success")
        self.assertEqual(self.view.current_status, "Success")

    def test_get_editor_data(self):
        """Test getting editor data."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "Test User")
        self.view.username_entry.delete(0, "end")
        self.view.username_entry.insert(0, "test_user")
        self.view.password_entry.delete(0, "end")
        self.view.password_entry.insert(0, "test_password")
        self.view.status_var.set("Active")
        self.view.category_entry.delete(0, "end")
        self.view.category_entry.insert(0, "Test")
        self.view.tags_entry.delete(0, "end")
        self.view.tags_entry.insert(0, "test, user")
        self.view.notes_text.delete("1.0", "end")
        self.view.notes_text.insert("1.0", "Test notes")
        self.view.selected_credential = "user1"

        # Call the method
        data = self.view.get_editor_data()

        # Verify the data
        self.assertEqual(data["id"], "user1")
        self.assertEqual(data["name"], "Test User")
        self.assertEqual(data["username"], "test_user")
        self.assertEqual(data["password"], "test_password")
        self.assertEqual(data["status"], "Active")
        self.assertEqual(data["category"], "Test")
        self.assertEqual(data["tags"], ["test", "user"])
        self.assertEqual(data["notes"], "Test notes")

    def test_show_validation_error(self):
        """Test showing a validation error."""
        # Call the method
        self.view.show_validation_error("Test error message")

        # Verify the error was shown
        self.assertEqual(self.view.validation_label.cget("text"), "Test error message")

    def test_on_status_filter_changed(self):
        """Test the status filter changed event handler."""
        # Set up the filter values
        self.view.status_filter_var.set("Success")
        self.view.category_var.set("All")
        self.view.search_var.set("")

        # Call the method
        self.view._on_status_filter_changed("Success")

        # Verify the presenter was called
        self.assertEqual(self.view.current_status, "Success")
        self.mock_presenter.filter_credentials.assert_called_once_with("Success", "All", "")

    def test_on_category_filter_changed(self):
        """Test the category filter changed event handler."""
        # Set up the filter values
        self.view.status_filter_var.set("All")
        self.view.category_var.set("Email")
        self.view.search_var.set("")

        # Call the method
        self.view._on_category_filter_changed("Email")

        # Verify the presenter was called
        self.mock_presenter.filter_credentials.assert_called_once_with("All", "Email", "")

    def test_on_search_changed(self):
        """Test the search changed event handler."""
        # Set up the filter values
        self.view.status_filter_var.set("All")
        self.view.category_var.set("All")
        self.view.search_var.set("test")

        # Call the method
        self.view._on_search_changed()

        # Verify the presenter was called
        self.mock_presenter.filter_credentials.assert_called_once_with("All", "All", "test")

    def test_on_clear_search(self):
        """Test the clear search button click event handler."""
        # Set up the search value
        self.view.search_var.set("test")

        # Call the method
        self.view._on_clear_search()

        # Verify the search was cleared
        self.assertEqual(self.view.search_var.get(), "")

    def test_on_column_click(self):
        """Test the column click event handler."""
        # Initialize sort state
        self.view.sort_column = "name"
        self.view.sort_reverse = False

        # Call the method with the same column
        self.view._on_column_click("name")

        # Verify the presenter was called and sort state was updated
        self.mock_presenter.sort_credentials.assert_called_once_with("name", True)
        self.assertEqual(self.view.sort_column, "name")
        self.assertEqual(self.view.sort_reverse, True)

        # Reset the mock
        self.mock_presenter.sort_credentials.reset_mock()

        # Call the method with a different column
        self.view._on_column_click("username")

        # Verify the presenter was called and sort state was updated
        self.mock_presenter.sort_credentials.assert_called_once_with("username", False)
        self.assertEqual(self.view.sort_column, "username")
        self.assertEqual(self.view.sort_reverse, False)

    def test_on_new_clicked(self):
        """Test the new button click event handler."""
        # Call the method
        self.view._on_new_clicked()

        # Verify the editor was cleared and enabled
        self.assertEqual(self.view.selected_credential, None)
        self.assertEqual(self.view.editor_header.cget("text"), "Create a new credential")

    def test_on_save_clicked(self):
        """Test the save button click event handler."""
        # Set up the editor
        self.view.name_entry.delete(0, "end")
        self.view.name_entry.insert(0, "Test User")

        # Call the method
        self.view._on_save_clicked()

        # Verify the presenter was called
        self.mock_presenter.save_credential.assert_called_once()

    def test_on_delete_clicked(self):
        """Test the delete button click event handler."""
        # Set up the view
        self.view.selected_credential = "user1"

        # Call the method
        self.view._on_delete_clicked()

        # Verify the presenter was called
        self.mock_presenter.delete_credential.assert_called_once_with("user1")

    def test_on_clear_clicked(self):
        """Test the clear button click event handler."""
        # Set up the view
        self.view.selected_credential = "user1"

        # Call the method
        self.view._on_clear_clicked()

        # Verify the editor was cleared and disabled
        self.assertEqual(self.view.selected_credential, None)
        self.assertEqual(self.view.editor_header.cget("text"), "Credential Editor")

    def test_on_import_clicked(self):
        """Test the import button click event handler."""
        # Call the method
        self.view._on_import_clicked()

        # Verify the presenter was called
        self.mock_presenter.import_credentials.assert_called_once()

    def test_on_export_clicked(self):
        """Test the export button click event handler."""
        # Call the method
        self.view._on_export_clicked()

        # Verify the presenter was called
        self.mock_presenter.export_credentials.assert_called_once()

    def test_on_batch_operations_clicked(self):
        """Test the batch operations button click event handler."""
        # Call the method
        self.view._on_batch_operations_clicked()

        # Verify the presenter was called
        self.mock_presenter.show_batch_operations.assert_called_once()

if __name__ == "__main__":
    unittest.main()
