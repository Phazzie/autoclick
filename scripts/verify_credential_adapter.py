"""
Script to verify the CredentialAdapter integration with UI components.

This script initializes the CredentialAdapter in clean architecture mode and
verifies that the UI components correctly access it.
"""
import sys
import os
import tkinter as tk
from tkinter import messagebox

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.domain.credentials.impl.credential_service import CredentialService
from src.ui.adapters.impl.credential_adapter import CredentialAdapter
from src.ui.views.credential_view import CredentialView
from src.ui.presenters.credential_presenter import CredentialPresenter


class MockApp:
    """Mock application for testing."""

    def __init__(self):
        """Initialize the mock app."""
        self.status_messages = []

    def update_status(self, message):
        """Update the application status."""
        print(f"Status: {message}")
        self.status_messages.append(message)


def verify_credential_adapter():
    """Verify the CredentialAdapter integration with UI components."""
    print("Verifying CredentialAdapter integration with UI components...")

    # Create a root window
    root = tk.Tk()
    root.title("Credential Adapter Verification")
    root.geometry("800x600")

    try:
        # Create the credential service
        credential_service = CredentialService()

        # Create the adapter with the service
        credential_adapter = CredentialAdapter(credential_service=credential_service)

        # Create the view
        credential_view = CredentialView(root)

        # Create the mock app
        mock_app = MockApp()

        # Pack the view to ensure it's initialized
        credential_view.pack(fill=tk.BOTH, expand=True)

        # Create widgets
        credential_view._create_widgets()
        credential_view._setup_layout()

        # Create the presenter
        credential_presenter = CredentialPresenter(
            view=credential_view,
            app=mock_app,
            service=credential_adapter
        )

        # Set the presenter for the view
        credential_view.set_presenter(credential_presenter)

        # Initialize the view
        credential_presenter.initialize_view()

        # Add a test credential
        test_credential = {
            "name": "Test Credential",
            "username": "testuser",
            "password": "testpassword",
            "category": "Test",
            "tags": ["test", "verification"],
            "notes": "This is a test credential created by the verification script."
        }

        # Create a button to add a test credential
        add_button = tk.Button(
            root,
            text="Add Test Credential",
            command=lambda: credential_presenter.save_credential(test_credential)
        )
        add_button.pack(pady=10)

        # Create a button to refresh the view
        refresh_button = tk.Button(
            root,
            text="Refresh Credentials",
            command=credential_presenter.load_credentials
        )
        refresh_button.pack(pady=10)

        # Create a button to exit
        exit_button = tk.Button(
            root,
            text="Exit",
            command=root.destroy
        )
        exit_button.pack(pady=10)

        # Start the main loop
        print("UI initialized. Please interact with the UI to verify functionality.")
        print("- Click 'Add Test Credential' to add a test credential")
        print("- Click 'Refresh Credentials' to refresh the credential list")
        print("- Click 'Exit' to close the application")

        root.mainloop()

        print("Verification complete.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    verify_credential_adapter()
