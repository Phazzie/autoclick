"""
Script to run the credential adapter tests.
"""
import os
import sys
import unittest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

# Import the test module
from test_credential_adapter_new import TestCredentialAdapter

if __name__ == "__main__":
    unittest.main()
