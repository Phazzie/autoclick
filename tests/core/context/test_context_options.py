"""Tests for the ContextOptions class"""
import unittest

from src.core.context.context_options import ContextOptions


class TestContextOptions(unittest.TestCase):
    """Test cases for the ContextOptions class"""

    def test_default_options(self):
        """Test default option values"""
        # Arrange & Act
        options = ContextOptions()

        # Assert
        self.assertTrue(options.inherit_variables)
        self.assertTrue(options.track_variable_changes)
        self.assertTrue(options.track_state_changes)
        self.assertEqual(options.max_state_history, 100)
        self.assertEqual(options.max_variable_history, 100)
        self.assertEqual(options.metadata, {})

    def test_custom_options(self):
        """Test setting custom option values"""
        # Arrange & Act
        options = ContextOptions(
            inherit_variables=False,
            track_variable_changes=False,
            track_state_changes=False,
            max_state_history=50,
            max_variable_history=50,
            metadata={"test": "value"}
        )

        # Assert
        self.assertFalse(options.inherit_variables)
        self.assertFalse(options.track_variable_changes)
        self.assertFalse(options.track_state_changes)
        self.assertEqual(options.max_state_history, 50)
        self.assertEqual(options.max_variable_history, 50)
        self.assertEqual(options.metadata, {"test": "value"})

    def test_serialization(self):
        """Test serializing and deserializing options"""
        # Arrange
        options = ContextOptions(
            inherit_variables=False,
            track_variable_changes=False,
            track_state_changes=False,
            max_state_history=50,
            max_variable_history=50,
            metadata={"test": "value"}
        )

        # Act
        serialized = options.to_dict()
        deserialized = ContextOptions.from_dict(serialized)

        # Assert
        self.assertEqual(deserialized.inherit_variables, options.inherit_variables)
        self.assertEqual(deserialized.track_variable_changes, options.track_variable_changes)
        self.assertEqual(deserialized.track_state_changes, options.track_state_changes)
        self.assertEqual(deserialized.max_state_history, options.max_state_history)
        self.assertEqual(deserialized.max_variable_history, options.max_variable_history)
        self.assertEqual(deserialized.metadata, options.metadata)

    def test_metadata_isolation(self):
        """Test that metadata is properly isolated"""
        # Arrange
        metadata = {"test": "value"}
        options = ContextOptions(metadata=metadata)

        # Act - Modify the original metadata
        metadata["test"] = "modified"

        # Assert - Options metadata should not be affected
        self.assertEqual(options.metadata["test"], "value")

        # Act - Modify the options metadata
        options.metadata["test"] = "modified_in_options"

        # Assert - Original metadata should not be affected
        self.assertEqual(metadata["test"], "modified")


if __name__ == "__main__":
    unittest.main()
