#!/usr/bin/env python
"""
Enhanced Error Logger for AUTOCLICK

This module provides robust error logging functionality:
- Logs errors to both console and file
- Creates timestamped log files
- Captures full stack traces
- Provides different log levels
- Rotates log files to prevent excessive disk usage

Usage:
    from error_logger import logger
    
    # Log different levels of messages
    logger.debug("Debug information")
    logger.info("Information message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical error message")
    
    # Log exceptions with traceback
    try:
        # Some code that might raise an exception
        result = 1 / 0
    except Exception as e:
        logger.exception("An error occurred: %s", str(e))
"""
import os
import sys
import logging
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(logs_dir, exist_ok=True)

# Configure the logger
logger = logging.getLogger('AUTOCLICK')
logger.setLevel(logging.DEBUG)

# Create a formatter that includes timestamp, level, and message
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler for the log file with rotation (max 5MB, keep 5 backup files)
log_file = os.path.join(logs_dir, 'autoclick.log')
file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Create a function to log uncaught exceptions
def log_uncaught_exception(exc_type, exc_value, exc_traceback):
    """Log uncaught exceptions to the log file."""
    if issubclass(exc_type, KeyboardInterrupt):
        # Don't log keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Format the exception and traceback
    exception_details = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    
    # Log the exception
    logger.critical("Uncaught exception:\n%s", exception_details)
    
    # Call the default exception handler
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

# Set the uncaught exception handler
sys.excepthook = log_uncaught_exception

# Log startup message
logger.info("AUTOCLICK Error Logger initialized")

def get_recent_errors(num_lines=50):
    """
    Get the most recent errors from the log file.
    
    Args:
        num_lines: Number of lines to retrieve from the end of the log file
        
    Returns:
        A list of the most recent log lines
    """
    if not os.path.exists(log_file):
        return ["No log file found."]
    
    try:
        with open(log_file, 'r') as f:
            # Read all lines and get the last num_lines
            lines = f.readlines()
            return lines[-num_lines:] if len(lines) > num_lines else lines
    except Exception as e:
        return [f"Error reading log file: {str(e)}"]

if __name__ == "__main__":
    # If this script is run directly, display recent errors
    print("\n" + "=" * 80)
    print("AUTOCLICK Recent Errors".center(80))
    print("=" * 80 + "\n")
    
    recent_errors = get_recent_errors()
    for line in recent_errors:
        print(line.strip())
