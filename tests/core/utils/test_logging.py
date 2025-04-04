"""
Tests for logging utilities.

This module contains tests for the logging utilities.
Following TDD principles, these tests are written before implementing the actual code.

SRP-1: Tests logging utilities
"""
import unittest
import logging
from unittest.mock import patch, MagicMock

# Import the module to be tested (will be implemented after tests)
# from src.core.utils.logging import LoggingMixin, get_logger, configure_logging


class TestLoggingMixin(unittest.TestCase):
    """Tests for the LoggingMixin class."""

    def test_init_logger(self):
        """Test that __init_logger__ initializes the logger correctly."""
        # This test will pass once we implement the LoggingMixin
        # with the expected behavior
        try:
            from src.core.utils.logging import LoggingMixin
            
            class TestClass(LoggingMixin):
                pass
                
            test_obj = TestClass()
            test_obj.__init_logger__()
            
            self.assertTrue(hasattr(test_obj, '_logger'))
            self.assertIsInstance(test_obj._logger, logging.Logger)
            self.assertEqual(test_obj._logger.name, f"{TestClass.__module__}.{TestClass.__name__}")
        except ImportError:
            self.skipTest("LoggingMixin not implemented yet")
            
    def test_log_info(self):
        """Test that log_info logs an info message."""
        # This test will pass once we implement the LoggingMixin
        # with the expected behavior
        try:
            from src.core.utils.logging import LoggingMixin
            
            class TestClass(LoggingMixin):
                pass
                
            test_obj = TestClass()
            
            # Mock the logger
            test_obj._logger = MagicMock()
            
            # Call log_info
            test_obj.log_info("Test message")
            
            # Verify that info was called with the message
            test_obj._logger.info.assert_called_once_with("Test message")
        except ImportError:
            self.skipTest("LoggingMixin not implemented yet")
            
    def test_log_error(self):
        """Test that log_error logs an error message."""
        # This test will pass once we implement the LoggingMixin
        # with the expected behavior
        try:
            from src.core.utils.logging import LoggingMixin
            
            class TestClass(LoggingMixin):
                pass
                
            test_obj = TestClass()
            
            # Mock the logger
            test_obj._logger = MagicMock()
            
            # Call log_error without exception
            test_obj.log_error("Test message")
            
            # Verify that error was called with the message
            test_obj._logger.error.assert_called_once_with("Test message")
            
            # Reset the mock
            test_obj._logger.reset_mock()
            
            # Call log_error with exception
            exception = Exception("Test exception")
            test_obj.log_error("Test message", exception)
            
            # Verify that error was called with the message and exception
            test_obj._logger.error.assert_called_once_with("Test message: Test exception")
        except ImportError:
            self.skipTest("LoggingMixin not implemented yet")
            
    def test_log_warning(self):
        """Test that log_warning logs a warning message."""
        # This test will pass once we implement the LoggingMixin
        # with the expected behavior
        try:
            from src.core.utils.logging import LoggingMixin
            
            class TestClass(LoggingMixin):
                pass
                
            test_obj = TestClass()
            
            # Mock the logger
            test_obj._logger = MagicMock()
            
            # Call log_warning
            test_obj.log_warning("Test message")
            
            # Verify that warning was called with the message
            test_obj._logger.warning.assert_called_once_with("Test message")
        except ImportError:
            self.skipTest("LoggingMixin not implemented yet")
            
    def test_log_debug(self):
        """Test that log_debug logs a debug message."""
        # This test will pass once we implement the LoggingMixin
        # with the expected behavior
        try:
            from src.core.utils.logging import LoggingMixin
            
            class TestClass(LoggingMixin):
                pass
                
            test_obj = TestClass()
            
            # Mock the logger
            test_obj._logger = MagicMock()
            
            # Call log_debug
            test_obj.log_debug("Test message")
            
            # Verify that debug was called with the message
            test_obj._logger.debug.assert_called_once_with("Test message")
        except ImportError:
            self.skipTest("LoggingMixin not implemented yet")
            
    def test_auto_init_logger(self):
        """Test that logging methods auto-initialize the logger if needed."""
        # This test will pass once we implement the LoggingMixin
        # with the expected behavior
        try:
            from src.core.utils.logging import LoggingMixin
            
            class TestClass(LoggingMixin):
                pass
                
            test_obj = TestClass()
            
            # Call log_info without initializing the logger
            with patch.object(TestClass, '__init_logger__') as mock_init_logger:
                test_obj.log_info("Test message")
                mock_init_logger.assert_called_once()
                
            # Call log_error without initializing the logger
            test_obj = TestClass()
            with patch.object(TestClass, '__init_logger__') as mock_init_logger:
                test_obj.log_error("Test message")
                mock_init_logger.assert_called_once()
                
            # Call log_warning without initializing the logger
            test_obj = TestClass()
            with patch.object(TestClass, '__init_logger__') as mock_init_logger:
                test_obj.log_warning("Test message")
                mock_init_logger.assert_called_once()
                
            # Call log_debug without initializing the logger
            test_obj = TestClass()
            with patch.object(TestClass, '__init_logger__') as mock_init_logger:
                test_obj.log_debug("Test message")
                mock_init_logger.assert_called_once()
        except ImportError:
            self.skipTest("LoggingMixin not implemented yet")


class TestLoggingFunctions(unittest.TestCase):
    """Tests for the logging functions."""

    def test_get_logger(self):
        """Test that get_logger returns a logger with the given name."""
        # This test will pass once we implement the get_logger function
        # with the expected behavior
        try:
            from src.core.utils.logging import get_logger
            
            logger = get_logger("test_logger")
            
            self.assertIsInstance(logger, logging.Logger)
            self.assertEqual(logger.name, "test_logger")
        except ImportError:
            self.skipTest("get_logger not implemented yet")
            
    def test_configure_logging(self):
        """Test that configure_logging configures the root logger correctly."""
        # This test will pass once we implement the configure_logging function
        # with the expected behavior
        try:
            from src.core.utils.logging import configure_logging
            
            # Mock the root logger
            with patch('logging.getLogger') as mock_get_logger:
                mock_root_logger = MagicMock()
                mock_get_logger.return_value = mock_root_logger
                
                # Mock the handlers
                mock_stream_handler = MagicMock()
                mock_file_handler = MagicMock()
                
                with patch('logging.StreamHandler', return_value=mock_stream_handler):
                    with patch('logging.FileHandler', return_value=mock_file_handler):
                        # Call configure_logging without log_file
                        configure_logging(level=logging.DEBUG)
                        
                        # Verify that the root logger was configured correctly
                        mock_get_logger.assert_called_once_with()
                        mock_root_logger.setLevel.assert_called_once_with(logging.DEBUG)
                        mock_stream_handler.setLevel.assert_called_once_with(logging.DEBUG)
                        mock_root_logger.addHandler.assert_called_once_with(mock_stream_handler)
                        
                        # Reset the mocks
                        mock_get_logger.reset_mock()
                        mock_root_logger.reset_mock()
                        mock_stream_handler.reset_mock()
                        
                        # Call configure_logging with log_file
                        configure_logging(level=logging.INFO, log_file="test.log")
                        
                        # Verify that the root logger was configured correctly
                        mock_get_logger.assert_called_once_with()
                        mock_root_logger.setLevel.assert_called_once_with(logging.INFO)
                        mock_stream_handler.setLevel.assert_called_once_with(logging.INFO)
                        mock_file_handler.setLevel.assert_called_once_with(logging.INFO)
                        self.assertEqual(mock_root_logger.addHandler.call_count, 2)
        except ImportError:
            self.skipTest("configure_logging not implemented yet")


if __name__ == "__main__":
    unittest.main()
