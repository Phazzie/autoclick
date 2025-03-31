"""
Main entry point for the AUTOCLICK application.
SOLID: Single responsibility - application startup.
KISS: Simple initialization and error handling.
"""
import sys
import traceback
import tkinter as tk
from tkinter import messagebox

def global_exception_handler(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions globally."""
    # Log the error
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"FATAL ERROR: Unhandled exception:\n{error_msg}")

    # Show error dialog
    try:
        messagebox.showerror(
            "Fatal Error",
            f"An unhandled error occurred:\n\n{exc_value}\n\nThe application will now close."
        )
    except:
        # If messagebox fails, at least try to print to console
        print("Could not display error dialog. Application will exit.")

    # Exit the application
    sys.exit(1)

def main():
    """Main entry point for the application."""
    print("DEBUG: Starting application...")

    # Set up global exception handler
    sys.excepthook = global_exception_handler
    print("DEBUG: Exception handler set up")

    # Import app here to avoid circular imports
    from app import AutoClickApp
    print("DEBUG: Imported AutoClickApp")

    # Create and run the application
    root = tk.Tk()
    root.withdraw()  # Hide the root window initially
    print("DEBUG: Created root Tk window")

    # Create the app instance
    print("DEBUG: Creating AutoClickApp instance...")
    app = AutoClickApp(root)
    print("DEBUG: AutoClickApp instance created")

    # Configure Tk exception handler
    root.report_callback_exception = global_exception_handler
    print("DEBUG: Configured Tk exception handler")

    # Start the application
    print("DEBUG: Starting app.run()...")
    app.run()
    print("DEBUG: app.run() completed")

if __name__ == "__main__":
    main()
