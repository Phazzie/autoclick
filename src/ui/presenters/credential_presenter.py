"""
Credential Management Presenter for handling credential operations.
SOLID: Single responsibility - business logic for credential management.
KISS: Simple operations with clear error handling.
"""
import os
from datetime import datetime
from tkinter import filedialog, messagebox
from typing import Dict, List, Any, Optional, TYPE_CHECKING

from ..presenters.base_presenter import BasePresenter
from ..adapters.credential_adapter import CredentialAdapter
from ..dialogs.batch_operations_dialog import BatchOperationsDialog

if TYPE_CHECKING:
    from ..views.credential_view import CredentialView
    from app import AutoClickApp

class CredentialPresenter(BasePresenter[CredentialAdapter]):
    """Presenter for the Credential Management view."""

    # Type hints for view and app
    view: 'CredentialView'
    app: 'AutoClickApp'

    def __init__(self, view: 'CredentialView', app: 'AutoClickApp', service: CredentialAdapter):
        """
        Initialize the credential presenter.

        Args:
            view: The credential view
            app: The main application
            service: The credential adapter
        """
        super().__init__(view=view, app=app, service=service)
        self.credentials = []  # Cache of credentials

    def initialize_view(self):
        """Initialize the view with data."""
        try:
            self.load_credentials()
            self.update_app_status("Credential management initialized")
        except Exception as e:
            self._handle_error("initializing credential management", e)

    def load_credentials(self):
        """Load credentials from the service and update the view."""
        try:
            # Get all credentials from the service
            self.credentials = self.service.get_all_credentials()

            # Update the view
            self.view.update_credential_list(self.credentials)
            self.update_app_status("Credentials loaded")
        except Exception as e:
            self._handle_error("loading credentials", e)

    def filter_credentials(self, status: str, category: str = "All", search_text: str = ""):
        """
        Filter credentials by status, category, and search text.

        Args:
            status: Status to filter by ("All", "Active", "Success", "Failure", "Inactive")
            category: Category to filter by ("All" or a specific category)
            search_text: Text to search for in name, username, or notes
        """
        try:
            # Start with all credentials
            filtered_credentials = self.credentials

            # Filter by status
            if status != "All":
                filtered_credentials = [
                    cred for cred in filtered_credentials
                    if cred.status == status
                ]

            # Filter by category
            if category != "All":
                filtered_credentials = [
                    cred for cred in filtered_credentials
                    if cred.category == category
                ]

            # Filter by search text
            if search_text:
                search_text = search_text.lower()
                filtered_credentials = [
                    cred for cred in filtered_credentials
                    if (search_text in cred.name.lower() or
                        search_text in cred.username.lower() or
                        search_text in cred.notes.lower())
                ]

            # Update the view
            self.view.update_credential_list(filtered_credentials)

            # Update status message
            filters = []
            if status != "All":
                filters.append(f"status={status}")
            if category != "All":
                filters.append(f"category={category}")
            if search_text:
                filters.append(f"search='{search_text}'")

            if filters:
                self.update_app_status(f"Filtered credentials by {', '.join(filters)}")
            else:
                self.update_app_status("Showing all credentials")
        except Exception as e:
            self._handle_error(f"filtering credentials", e)

    def select_credential(self, credential_id: str):
        """
        Handle credential selection.

        Args:
            credential_id: ID of the selected credential
        """
        try:
            # Find the credential in the cache
            credential = None
            for cred in self.credentials:
                if cred.id == credential_id:
                    credential = cred
                    break

            if credential:
                # Populate the editor with the credential data
                self.view.populate_editor(credential)
                self.update_app_status(f"Selected credential: {credential.name}")
            else:
                # Credential not found
                self.view.clear_editor()
                self.view.set_editor_state(False)
                self.update_app_status(f"Credential not found: {credential_id}")
        except Exception as e:
            self._handle_error(f"selecting credential {credential_id}", e)

    def save_credential(self, credential_data: Dict[str, Any]):
        """
        Save a credential.

        Args:
            credential_data: Dictionary containing the credential data
        """
        try:
            # Validate the credential data
            username = credential_data.get("username", "").strip()
            if not username:
                self.view.show_validation_error("Username is required")
                return

            password = credential_data.get("password", "").strip()
            if not password:
                self.view.show_validation_error("Password is required")
                return

            name = credential_data.get("name", "").strip()
            if not name:
                # Use username as name if not provided
                name = username

            # Check if this is a new credential or an update
            credential_id = credential_data.get("id", "")

            # Prepare tags
            tags = credential_data.get("tags", [])

            # Save the credential
            if not credential_id:
                # Create a new credential
                self.service.add_credential(
                    name=name,
                    username=username,
                    password=password,
                    category=credential_data.get("category", "Other"),
                    tags=tags,
                    notes=credential_data.get("notes", "")
                )
                self.update_app_status(f"Created credential: {name}")
            else:
                # Update an existing credential
                self.service.update_credential(
                    cid=credential_id,
                    name=name,
                    username=username,
                    password=password,
                    status=credential_data.get("status", "Active"),
                    category=credential_data.get("category", "Other"),
                    tags=tags,
                    notes=credential_data.get("notes", "")
                )
                self.update_app_status(f"Updated credential: {name}")

            # Reload credentials to refresh the view
            self.load_credentials()

            # Select the saved credential
            if not credential_id:
                # For new credentials, find by username
                for cred in self.credentials:
                    if cred.username == username:
                        self.select_credential(cred.id)
                        break
            else:
                # For updates, use the existing ID
                self.select_credential(credential_id)
        except Exception as e:
            self._handle_error(f"saving credential {credential_data.get('name', '')}", e)

    def delete_credential(self, credential_id: str):
        """
        Delete a credential.

        Args:
            credential_id: ID of the credential to delete
        """
        try:
            # Find the credential in the cache
            credential_name = credential_id
            for cred in self.credentials:
                if cred.id == credential_id:
                    credential_name = cred.name
                    break

            # Confirm deletion
            if not self.view.ask_yes_no("Confirm Delete", f"Are you sure you want to delete the credential '{credential_name}'?"):
                return

            # Delete the credential
            success = self.service.delete_credential(credential_id)

            if success:
                self.update_app_status(f"Deleted credential: {credential_name}")

                # Reload credentials to refresh the view
                self.load_credentials()

                # Clear the editor
                self.view.clear_editor()
                self.view.set_editor_state(False)
            else:
                self.view.display_error("Delete Failed", f"Failed to delete credential: {credential_name}")
        except Exception as e:
            self._handle_error(f"deleting credential {credential_id}", e)

    def sort_credentials(self, column: str, reverse: bool = False):
        """
        Sort credentials by column.

        Args:
            column: Column to sort by
            reverse: Whether to sort in reverse order
        """
        try:
            # Create a copy of the credentials list
            sorted_credentials = list(self.credentials)

            # Define a key function based on the column
            def get_sort_key(cred):
                if column == "name":
                    return cred.name.lower()
                elif column == "username":
                    return cred.username.lower()
                elif column == "status":
                    return cred.status
                elif column == "category":
                    return cred.category.lower()
                elif column == "last_used":
                    # Handle None values for last_used
                    return cred.last_used or datetime.min
                else:
                    return ""

            # Sort the credentials
            sorted_credentials.sort(key=get_sort_key, reverse=reverse)

            # Update the view
            self.view.update_credential_list(sorted_credentials)

            # Update status message
            direction = "descending" if reverse else "ascending"
            self.update_app_status(f"Sorted credentials by {column} ({direction})")
        except Exception as e:
            self._handle_error(f"sorting credentials by {column}", e)

    def import_credentials(self):
        """
        Import credentials from a file.
        """
        try:
            # Show file dialog to select import file
            file_path = filedialog.askopenfilename(
                title="Import Credentials",
                filetypes=[
                    ("CSV Files", "*.csv"),
                    ("JSON Files", "*.json"),
                    ("All Files", "*.*")
                ]
            )

            if not file_path:
                return  # User canceled

            # Determine file type from extension
            file_ext = os.path.splitext(file_path)[1].lower()

            # Import based on file type
            imported_count = 0
            skipped_rows = []

            try:
                if file_ext == ".csv":
                    imported_count, skipped_rows = self.service.import_from_csv(file_path)
                elif file_ext == ".json":
                    imported_count, skipped_rows = self.service.import_from_json(file_path)
                else:
                    self.view.display_error("Error", f"Unsupported file type: {file_ext}")
                    return
            except ValueError as e:
                self.view.display_error("Import Error", str(e))
                return
            except FileNotFoundError as e:
                self.view.display_error("Import Error", str(e))
                return

            # Reload credentials
            self.load_credentials()

            # Show success message with warning about skipped rows if any
            if skipped_rows:
                message = f"Successfully imported {imported_count} credentials.\n\n"
                message += f"Warning: {len(skipped_rows)} rows were skipped during import."

                # Show up to 5 skipped row messages
                if len(skipped_rows) <= 5:
                    message += "\n\nSkipped rows:\n" + "\n".join(skipped_rows)
                else:
                    message += "\n\nFirst 5 skipped rows:\n" + "\n".join(skipped_rows[:5])
                    message += f"\n\n...and {len(skipped_rows) - 5} more."

                self.view.display_warning("Import Complete with Warnings", message)
            else:
                self.view.display_info("Import Complete", f"Successfully imported {imported_count} credentials.")

            self.update_app_status(f"Imported {imported_count} credentials from {file_path}")
        except Exception as e:
            self.view.display_error("Import Error", str(e))
            self._handle_error(f"importing credentials", e)

    def export_credentials(self):
        """
        Export credentials to a file.
        """
        try:
            # Show file dialog to select export file
            file_path = filedialog.asksaveasfilename(
                title="Export Credentials",
                filetypes=[
                    ("CSV Files", "*.csv"),
                    ("JSON Files", "*.json")
                ],
                defaultextension=".csv"
            )

            if not file_path:
                return  # User canceled

            # Determine file type from extension
            file_ext = os.path.splitext(file_path)[1].lower()

            # Export based on file type
            if file_ext == ".csv":
                exported_count = self.service.export_to_csv(file_path)
            elif file_ext == ".json":
                exported_count = self.service.export_to_json(file_path)
            else:
                self.view.display_error("Error", f"Unsupported file type: {file_ext}")
                return

            # Show success message
            self.view.display_info("Export Complete", f"Successfully exported {exported_count} credentials.")
            self.update_app_status(f"Exported {exported_count} credentials to {file_path}")
        except Exception as e:
            self.view.display_error("Export Error", str(e))
            self._handle_error(f"exporting credentials", e)

    def show_batch_operations(self):
        """
        Show batch operations dialog.
        """
        try:
            # Create a dialog for batch operations
            dialog = BatchOperationsDialog(self.view)

            # If the user confirmed the operation
            if dialog.result:
                operation = dialog.operation
                target_status = dialog.target_status
                new_status = dialog.new_status

                # Perform the operation
                if operation == "update_status":
                    # Update status of credentials
                    count = self.service.update_credentials_status(target_status, new_status)
                    self.view.display_info("Batch Operation", f"Updated {count} credentials from {target_status} to {new_status}.")
                elif operation == "delete":
                    # Delete credentials by status
                    count = self.service.delete_credentials_by_status(target_status)
                    self.view.display_info("Batch Operation", f"Deleted {count} credentials with status {target_status}.")

                # Reload credentials
                self.load_credentials()
        except Exception as e:
            self.view.display_error("Batch Operation Error", str(e))
            self._handle_error(f"performing batch operation", e)
