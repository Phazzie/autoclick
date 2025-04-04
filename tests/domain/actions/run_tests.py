"""
Script to run the action tests.
"""
import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import the test modules
from test_action_service import TestActionService

if __name__ == "__main__":
    unittest.main()
