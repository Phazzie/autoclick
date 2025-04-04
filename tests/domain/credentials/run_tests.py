"""
Script to run the credential tests.
"""
import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# Import the test modules
from test_credential_validator import TestCredentialValidator
from test_credential_formatter import TestCredentialFormatter
from test_credential_utils import TestCredentialUtils

if __name__ == "__main__":
    unittest.main()
