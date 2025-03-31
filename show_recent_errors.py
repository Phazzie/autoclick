#!/usr/bin/env python
"""
Show Recent Errors for AUTOCLICK

This script displays the most recent errors from the AUTOCLICK log files.
It checks both the system-level logs and the error-specific logs.

Usage:
    python show_recent_errors.py [num_lines]

    num_lines: Optional. Number of lines to display from the end of each log file.
               Default is 50.
"""
import os
import sys
import json
from datetime import datetime
import glob

def find_log_files():
    """Find all log files in the application."""
    log_files = []

    # Check for logs directory
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if os.path.exists(logs_dir):
        # Find all .log files in the logs directory
        log_files.extend(glob.glob(os.path.join(logs_dir, '*.log')))

    # Check for error logs in the src/core/errors directory
    error_logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'core', 'errors', 'logs')
    if os.path.exists(error_logs_dir):
        # Find all .log and .json files in the error logs directory
        log_files.extend(glob.glob(os.path.join(error_logs_dir, '*.log')))
        log_files.extend(glob.glob(os.path.join(error_logs_dir, '*.json')))

    # Also check for the error_logger.py log file
    try:
        from error_logger import log_file
        if os.path.exists(log_file):
            log_files.append(log_file)
    except ImportError:
        pass

    return log_files

def get_recent_errors_from_file(file_path, num_lines=50):
    """
    Get the most recent errors from a log file.

    Args:
        file_path: Path to the log file
        num_lines: Number of lines to retrieve from the end of the log file

    Returns:
        A list of the most recent log lines
    """
    if not os.path.exists(file_path):
        return [f"File not found: {file_path}"]

    try:
        # Check if this is a JSON file
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                # Read the JSON file and format each entry
                entries = []
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        timestamp = entry.get('log_timestamp', entry.get('timestamp', 'Unknown time'))
                        message = entry.get('message', 'No message')
                        error_type = entry.get('error_type', 'Unknown error')
                        severity = entry.get('severity', 'Unknown severity')
                        entries.append(f"{timestamp} - {severity} - {error_type}: {message}")
                    except json.JSONDecodeError:
                        entries.append(line.strip())

                # Return the last num_lines entries
                return entries[-num_lines:] if len(entries) > num_lines else entries
        else:
            # Regular log file
            with open(file_path, 'r') as f:
                # Read all lines and get the last num_lines
                lines = f.readlines()
                return lines[-num_lines:] if len(lines) > num_lines else lines
    except Exception as e:
        return [f"Error reading file {file_path}: {str(e)}"]

def main():
    """Main function to display recent errors."""
    # Get the number of lines to display
    num_lines = 50
    if len(sys.argv) > 1:
        try:
            num_lines = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number of lines: {sys.argv[1]}. Using default: 50.")

    print("\n" + "=" * 80)
    print(f"AUTOCLICK Recent Errors (Last {num_lines} Lines Per Log)".center(80))
    print("=" * 80 + "\n")

    # Find all log files
    log_files = find_log_files()

    if not log_files:
        print("No log files found.")
        return 0

    # Display recent errors from each log file
    for log_file in log_files:
        print(f"\nLog file: {log_file}")
        print("-" * 80)

        recent_errors = get_recent_errors_from_file(log_file, num_lines)
        for line in recent_errors:
            if isinstance(line, str):
                print(line.strip())

if __name__ == "__main__":
    sys.exit(main())
