"""Tests for the VariableStorage class"""
import unittest
from unittest.mock import MagicMock

from src.core.context.variable_storage import VariableStorage, VariableScope, VariableChangeEvent


class TestVariableStorage(unittest.TestCase):
    """Test cases for the VariableStorage class"""

    def test_set_and_get_variable(self):
        """Test setting and getting a variable"""
        # Arrange
        storage = VariableStorage()

        # Act
        storage.set("test_var", "test_value", VariableScope.WORKFLOW)
        value = storage.get("test_var")

        # Assert
        self.assertEqual(value, "test_value")

    def test_variable_scoping(self):
        """Test variable scoping priority (local > workflow > global)"""
        # Arrange
        storage = VariableStorage()

        # Act
        storage.set("var", "global_value", VariableScope.GLOBAL)
        storage.set("var", "workflow_value", VariableScope.WORKFLOW)
        storage.set("var", "local_value", VariableScope.LOCAL)

        # Assert
        self.assertEqual(storage.get("var"), "local_value")

        # Delete local variable
        storage.delete("var", VariableScope.LOCAL)
        self.assertEqual(storage.get("var"), "workflow_value")

        # Delete workflow variable
        storage.delete("var", VariableScope.WORKFLOW)
        self.assertEqual(storage.get("var"), "global_value")

    def test_parent_inheritance(self):
        """Test inheriting variables from parent storage"""
        # Arrange
        parent = VariableStorage()
        parent.set("parent_var", "parent_value", VariableScope.WORKFLOW)

        child = VariableStorage(parent=parent)
        child.set("child_var", "child_value", VariableScope.WORKFLOW)

        # Act & Assert
        self.assertEqual(child.get("parent_var"), "parent_value")
        self.assertEqual(child.get("child_var"), "child_value")
        self.assertIsNone(parent.get("child_var"))

        # Override parent variable in child
        child.set("parent_var", "overridden_value", VariableScope.WORKFLOW)
        self.assertEqual(child.get("parent_var"), "overridden_value")
        self.assertEqual(parent.get("parent_var"), "parent_value")

    def test_variable_change_listener(self):
        """Test variable change listener notification"""
        # Arrange
        storage = VariableStorage()
        mock_listener = MagicMock()
        storage.add_variable_change_listener(mock_listener)

        # Act
        storage.set("test_var", "test_value", VariableScope.WORKFLOW)

        # Assert
        mock_listener.assert_called_once()
        event = mock_listener.call_args[0][0]
        self.assertEqual(event.name, "test_var")
        self.assertIsNone(event.old_value)
        self.assertEqual(event.new_value, "test_value")
        self.assertEqual(event.scope, VariableScope.WORKFLOW)

        # Update the variable
        mock_listener.reset_mock()
        storage.set("test_var", "updated_value", VariableScope.WORKFLOW)

        # Assert
        mock_listener.assert_called_once()
        event = mock_listener.call_args[0][0]
        self.assertEqual(event.name, "test_var")
        self.assertEqual(event.old_value, "test_value")
        self.assertEqual(event.new_value, "updated_value")

    def test_remove_variable_change_listener(self):
        """Test removing a variable change listener"""
        # Arrange
        storage = VariableStorage()
        mock_listener = MagicMock()
        storage.add_variable_change_listener(mock_listener)
        storage.remove_variable_change_listener(mock_listener)

        # Act
        storage.set("test_var", "test_value", VariableScope.WORKFLOW)

        # Assert
        mock_listener.assert_not_called()

    def test_clear_scope(self):
        """Test clearing all variables in a scope"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.WORKFLOW)
        storage.set("var3", "value3", VariableScope.GLOBAL)

        # Act
        storage.clear_scope(VariableScope.WORKFLOW)

        # Assert
        self.assertIsNone(storage.get("var1"))
        self.assertIsNone(storage.get("var2"))
        self.assertEqual(storage.get("var3"), "value3")

    def test_clear_all(self):
        """Test clearing all variables in all scopes"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.GLOBAL)
        storage.set("var3", "value3", VariableScope.LOCAL)

        # Act
        storage.clear_all()

        # Assert
        self.assertIsNone(storage.get("var1"))
        self.assertIsNone(storage.get("var2"))
        self.assertIsNone(storage.get("var3"))

    def test_get_all(self):
        """Test getting all variables"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.GLOBAL)
        storage.set("var3", "value3", VariableScope.LOCAL)

        # Act
        all_vars = storage.get_all()

        # Assert
        self.assertEqual(len(all_vars), 3)
        self.assertEqual(all_vars["var1"], "value1")
        self.assertEqual(all_vars["var2"], "value2")
        self.assertEqual(all_vars["var3"], "value3")

        # Get variables from specific scope
        workflow_vars = storage.get_all(VariableScope.WORKFLOW)
        self.assertEqual(len(workflow_vars), 1)
        self.assertEqual(workflow_vars["var1"], "value1")

    def test_get_names(self):
        """Test getting all variable names"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.GLOBAL)
        storage.set("var3", "value3", VariableScope.LOCAL)

        # Act
        all_names = storage.get_names()

        # Assert
        self.assertEqual(len(all_names), 3)
        self.assertIn("var1", all_names)
        self.assertIn("var2", all_names)
        self.assertIn("var3", all_names)

        # Get names from specific scope
        workflow_names = storage.get_names(VariableScope.WORKFLOW)
        self.assertEqual(len(workflow_names), 1)
        self.assertIn("var1", workflow_names)

    def test_has(self):
        """Test checking if a variable exists"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)

        # Act & Assert
        self.assertTrue(storage.has("var1"))
        self.assertFalse(storage.has("nonexistent"))

        # Check in specific scope
        self.assertTrue(storage.has("var1", VariableScope.WORKFLOW))
        self.assertFalse(storage.has("var1", VariableScope.GLOBAL))

    def test_get_scope(self):
        """Test getting the scope of a variable"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.GLOBAL)
        storage.set("var3", "value3", VariableScope.LOCAL)

        # Act & Assert
        self.assertEqual(storage.get_scope("var1"), VariableScope.WORKFLOW)
        self.assertEqual(storage.get_scope("var2"), VariableScope.GLOBAL)
        self.assertEqual(storage.get_scope("var3"), VariableScope.LOCAL)
        self.assertIsNone(storage.get_scope("nonexistent"))

    def test_variable_name_validation(self):
        """Test variable name validation"""
        # Arrange
        storage = VariableStorage()

        # Act & Assert
        with self.assertRaises(ValueError):
            storage.set("", "value")  # Empty name

        with self.assertRaises(ValueError):
            storage.set("123var", "value")  # Starts with number

        with self.assertRaises(ValueError):
            storage.set("var-name", "value")  # Contains invalid character

        # Valid names
        storage.set("var", "value")
        storage.set("_var", "value")
        storage.set("var123", "value")
        storage.set("var_name", "value")

    def test_clone(self):
        """Test cloning a variable storage"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.GLOBAL)

        # Act
        clone = storage.clone()

        # Assert
        self.assertEqual(clone.get("var1"), "value1")
        self.assertEqual(clone.get("var2"), "value2")

        # Modify original, clone should not change
        storage.set("var1", "modified")
        self.assertEqual(storage.get("var1"), "modified")
        self.assertEqual(clone.get("var1"), "value1")

    def test_serialization(self):
        """Test serializing and deserializing variable storage"""
        # Arrange
        storage = VariableStorage()
        storage.set("var1", "value1", VariableScope.WORKFLOW)
        storage.set("var2", "value2", VariableScope.GLOBAL)
        storage.set("var3", "value3", VariableScope.LOCAL)

        # Act
        serialized = storage.to_dict()
        deserialized = VariableStorage.from_dict(serialized)

        # Assert
        self.assertEqual(deserialized.get("var1"), "value1")
        self.assertEqual(deserialized.get("var2"), "value2")
        self.assertEqual(deserialized.get("var3"), "value3")


if __name__ == "__main__":
    unittest.main()
