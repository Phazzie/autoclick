"""Tests for the CredentialPresenter class."""
import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import os

from src.ui.presenters.credential_presenter import CredentialPresenter
from src.ui.adapters.credential_adapter import CredentialAdapter
from src.core.models import CredentialRecord

class TestCredentialPresenter(unittest.TestCase):
    """Test cases for the CredentialPresenter class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create mock objects
        self.mock_view = MagicMock()
        self.mock_app = MagicMock()
        self.mock_service = MagicMock(spec=CredentialAdapter)

        # Create the presenter
        self.presenter = CredentialPresenter(
            view=self.mock_view,
            app=self.mock_app,
            service=self.mock_service
        )

        # Set up mock data
        self.mock_credentials = [
            CredentialRecord(
                id="user1",
                name="Test User 1",
                username="user1",
                password="password1",
                status="Active",
                last_used=None,
                category="Test",
                tags=["test", "user"],
                notes="Test notes 1"
            ),
            CredentialRecord(
                id="user2",
                name="Test User 2",
                username="user2",
                password="password2",
                status="Success",
                last_used=datetime.now(),
                category="Production",
                tags=["prod"],
                notes="Test notes 2"
            ),
            CredentialRecord(
                id="user3",
                name="Test User 3",
                username="user3",
                password="password3",
                status="Failure",
                last_used=datetime.now(),
                category="Development",
                tags=["dev"],
                notes="Test notes 3"
            )
        ]

        # Configure mock service
        self.mock_service.get_all_credentials.return_value = self.mock_credentials

    def test_initialize_view(self):
        """Test initializing the view."""
        # Call the method
        self.presenter.initialize_view()

        # Verify the service was called
        self.mock_service.get_all_credentials.assert_called_once()

        # Verify the view was updated
        self.mock_view.update_credential_list.assert_called_once_with(self.mock_credentials)

        # Verify the status was updated
        self.mock_app.update_status.assert_called()

    def test_load_credentials(self):
        """Test loading credentials."""
        # Call the method
        self.presenter.load_credentials()

        # Verify the service was called
        self.mock_service.get_all_credentials.assert_called_once()

        # Verify the view was updated
        self.mock_view.update_credential_list.assert_called_once_with(self.mock_credentials)

    def test_filter_credentials_all(self):
        """Test filtering credentials by 'All' status."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials

        # Call the method
        self.presenter.filter_credentials("All", "All", "")

        # Verify the view was updated with all credentials
        self.mock_view.update_credential_list.assert_called_once_with(self.mock_credentials)

    def test_filter_credentials_specific_status(self):
        """Test filtering credentials by a specific status."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials

        # Call the method
        self.presenter.filter_credentials("Success", "All", "")

        # Verify the view was updated with only Success credentials
        expected_filtered = [self.mock_credentials[1]]  # Only the "Success" credential
        self.mock_view.update_credential_list.assert_called_once_with(expected_filtered)

    def test_filter_credentials_by_category(self):
        """Test filtering credentials by category."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials

        # Call the method
        self.presenter.filter_credentials("All", "Production", "")

        # Verify the view was updated with only Production credentials
        expected_filtered = [self.mock_credentials[1]]  # Only the "Production" credential
        self.mock_view.update_credential_list.assert_called_once_with(expected_filtered)

    def test_filter_credentials_by_search(self):
        """Test filtering credentials by search text."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials

        # Call the method
        self.presenter.filter_credentials("All", "All", "User 1")

        # Verify the view was updated with only matching credentials
        expected_filtered = [self.mock_credentials[0]]  # Only the credential with "User 1" in the name
        self.mock_view.update_credential_list.assert_called_once_with(expected_filtered)

    def test_select_credential(self):
        """Test selecting a credential."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials

        # Call the method
        self.presenter.select_credential("user2")

        # Verify the view was updated with the selected credential
        self.mock_view.populate_editor.assert_called_once_with(self.mock_credentials[1])

    def test_select_credential_not_found(self):
        """Test selecting a credential that doesn't exist."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials

        # Call the method
        self.presenter.select_credential("nonexistent_user")

        # Verify the view was cleared
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(False)

    def test_save_credential_new(self):
        """Test saving a new credential."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials.copy()

        # Set up mock service
        new_credential = CredentialRecord(
            id="new_user",
            name="New User",
            username="new_user",
            password="new_password",
            status="Active",
            last_used=None,
            category="Test",
            tags=["test"],
            notes="New user notes"
        )
        self.mock_service.add_credential.return_value = new_credential

        # Call the method
        self.presenter.save_credential({
            "id": "",  # Empty ID indicates a new credential
            "name": "New User",
            "username": "new_user",
            "password": "new_password",
            "status": "Active",
            "category": "Test",
            "tags": ["test"],
            "notes": "New user notes"
        })

        # Verify the service was called
        self.mock_service.add_credential.assert_called_once_with(
            name="New User",
            username="new_user",
            password="new_password",
            category="Test",
            tags=["test"],
            notes="New user notes"
        )

        # Verify credentials were reloaded
        self.mock_service.get_all_credentials.assert_called_once()

    def test_save_credential_update(self):
        """Test updating an existing credential."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials.copy()

        # Set up mock service
        updated_credential = CredentialRecord(
            id="user1",
            name="Updated User",
            username="user1",
            password="updated_password",
            status="Active",
            last_used=None,
            category="Updated",
            tags=["updated"],
            notes="Updated notes"
        )
        self.mock_service.update_credential.return_value = updated_credential

        # Call the method
        self.presenter.save_credential({
            "id": "user1",
            "name": "Updated User",
            "username": "user1",
            "password": "updated_password",
            "status": "Active",
            "category": "Updated",
            "tags": ["updated"],
            "notes": "Updated notes"
        })

        # Verify the service was called
        self.mock_service.update_credential.assert_called_once_with(
            cid="user1",
            name="Updated User",
            username="user1",
            password="updated_password",
            status="Active",
            category="Updated",
            tags=["updated"],
            notes="Updated notes"
        )

        # Verify credentials were reloaded
        self.mock_service.get_all_credentials.assert_called_once()

    def test_save_credential_validation_error(self):
        """Test saving a credential with validation errors."""
        # Call the method with empty username
        self.presenter.save_credential({
            "id": "",
            "name": "Test User",
            "username": "",  # Empty username
            "password": "password",
            "status": "Active",
            "category": "Test",
            "tags": ["test"],
            "notes": "Test notes"
        })

        # Verify validation error was shown
        self.mock_view.show_validation_error.assert_called_once()

        # Verify the service was not called
        self.mock_service.add_credential.assert_not_called()
        self.mock_service.update_credential.assert_not_called()

    def test_delete_credential_confirmed(self):
        """Test deleting a credential with confirmation."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials.copy()

        # Set up mock view to confirm deletion
        self.mock_view.ask_yes_no.return_value = True

        # Set up mock service
        self.mock_service.delete_credential.return_value = True

        # Call the method
        self.presenter.delete_credential("user1")

        # Verify the service was called
        self.mock_service.delete_credential.assert_called_once_with("user1")

        # Verify credentials were reloaded
        self.mock_service.get_all_credentials.assert_called_once()

        # Verify the view was cleared
        self.mock_view.clear_editor.assert_called_once()
        self.mock_view.set_editor_state.assert_called_once_with(False)

    def test_delete_credential_cancelled(self):
        """Test cancelling credential deletion."""
        # Set up mock view to cancel deletion
        self.mock_view.ask_yes_no.return_value = False

        # Call the method
        self.presenter.delete_credential("user1")

        # Verify the service was not called
        self.mock_service.delete_credential.assert_not_called()

    def test_delete_credential_failed(self):
        """Test failed credential deletion."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials.copy()

        # Set up mock view to confirm deletion
        self.mock_view.ask_yes_no.return_value = True

        # Set up mock service to fail
        self.mock_service.delete_credential.return_value = False

        # Call the method
        self.presenter.delete_credential("user1")

        # Verify the service was called
        self.mock_service.delete_credential.assert_called_once_with("user1")

        # Verify error was displayed
        self.mock_view.display_error.assert_called_once()

    def test_sort_credentials(self):
        """Test sorting credentials."""
        # Set up the presenter with credentials
        self.presenter.credentials = self.mock_credentials.copy()

        # Call the method
        self.presenter.sort_credentials("name", False)

        # Verify the view was updated
        self.mock_view.update_credential_list.assert_called_once()

        # Verify the app status was updated
        self.mock_app.update_status.assert_called_with("Sorted credentials by name (ascending)")

    @patch("tkinter.filedialog.askopenfilename")
    def test_import_credentials_csv(self, mock_askopenfilename):
        """Test importing credentials from a CSV file."""
        # Set up the mock dialog
        mock_askopenfilename.return_value = "test.csv"

        # Set up the mock service
        self.mock_service.import_from_csv.return_value = 3

        # Call the method
        self.presenter.import_credentials()

        # Verify the service was called
        self.mock_service.import_from_csv.assert_called_once_with("test.csv")

        # Verify the view was updated
        self.mock_view.display_info.assert_called_once()

        # Verify the app status was updated
        self.mock_app.update_status.assert_called()

    @patch("tkinter.filedialog.asksaveasfilename")
    def test_export_credentials_csv(self, mock_asksaveasfilename):
        """Test exporting credentials to a CSV file."""
        # Set up the mock dialog
        mock_asksaveasfilename.return_value = "test.csv"

        # Set up the mock service
        self.mock_service.export_to_csv.return_value = 2

        # Call the method
        self.presenter.export_credentials()

        # Verify the service was called
        self.mock_service.export_to_csv.assert_called_once_with("test.csv")

        # Verify the view was updated
        self.mock_view.display_info.assert_called_once()

        # Verify the app status was updated
        self.mock_app.update_status.assert_called()

    @patch("src.ui.dialogs.batch_operations_dialog.BatchOperationsDialog")
    def test_show_batch_operations_update(self, mock_dialog_class):
        """Test showing batch operations dialog for update."""
        # Set up the mock dialog
        mock_dialog = MagicMock()
        mock_dialog.result = True
        mock_dialog.operation = "update_status"
        mock_dialog.target_status = "Inactive"
        mock_dialog.new_status = "Active"
        mock_dialog_class.return_value = mock_dialog

        # Set up the mock service
        self.mock_service.update_credentials_status.return_value = 2

        # Call the method
        self.presenter.show_batch_operations()

        # Verify the service was called
        self.mock_service.update_credentials_status.assert_called_once_with("Inactive", "Active")

        # Verify the view was updated
        self.mock_view.display_info.assert_called_once()

    @patch("src.ui.dialogs.batch_operations_dialog.BatchOperationsDialog")
    def test_show_batch_operations_delete(self, mock_dialog_class):
        """Test showing batch operations dialog for delete."""
        # Set up the mock dialog
        mock_dialog = MagicMock()
        mock_dialog.result = True
        mock_dialog.operation = "delete"
        mock_dialog.target_status = "Inactive"
        mock_dialog_class.return_value = mock_dialog

        # Set up the mock service
        self.mock_service.delete_credentials_by_status.return_value = 2

        # Call the method
        self.presenter.show_batch_operations()

        # Verify the service was called
        self.mock_service.delete_credentials_by_status.assert_called_once_with("Inactive")

        # Verify the view was updated
        self.mock_view.display_info.assert_called_once()

if __name__ == "__main__":
    unittest.main()
