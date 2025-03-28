"""GUI command for the AUTOCLICK CLI"""
import argparse
import logging
from typing import Any

# Use the refactored GUI implementation
try:
    from src.ui.simple_gui_refactored import SimpleGUI
except ImportError:
    # Fall back to the original implementation if the refactored one is not available
    from src.ui.simple_gui import SimpleGUI


def gui_command(args: argparse.Namespace) -> int:
    """
    Launch the AUTOCLICK GUI

    Args:
        args: Command-line arguments

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting AUTOCLICK GUI")

    try:
        # Create the GUI
        gui = SimpleGUI(theme=args.theme)

        # Start the GUI
        gui.start()

        return 0
    except Exception as e:
        logger.error(f"Error starting GUI: {str(e)}")
        return 1
