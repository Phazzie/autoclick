"""Tests for the ExecutionContext class"""
import unittest
from unittest.mock import MagicMock

from src.core.context.execution_context import ExecutionContext
from src.core.context.context_options import ContextOptions
from src.core.context.execution_state import ExecutionStateEnum
from src.core.context.variable_storage import VariableScope


class TestExecutionContext(unittest.TestCase):
    """Test cases for the ExecutionContext class"""

    def test_context_initialization(self):
        """Test initializing an execution context"""
        # Arrange & Act
        context = ExecutionContext()

        # Assert
        self.assertIsNotNone(context.id)
        self.assertEqual(context.state.current_state, ExecutionStateEnum.CREATED)
        self.assertIsNotNone(context.variables)
        self.assertIsNone(context.parent)

    def test_context_with_options(self):
        """Test initializing a context with options"""
        # Arrange
        options = ContextOptions(
            inherit_variables=False,
            track_variable_changes=False,
            track_state_changes=False
        )

        # Act
        context = ExecutionContext(options=options)

        # Assert
        self.assertEqual(context.options.inherit_variables, False)
        self.assertEqual(context.options.track_variable_changes, False)
        self.assertEqual(context.options.track_state_changes, False)

    def test_parent_child_relationship(self):
        """Test parent-child context relationship"""
        # Arrange
        parent = ExecutionContext()

        # Act
        child = ExecutionContext(parent=parent)

        # Assert
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent._children)

    def test_create_child(self):
        """Test creating a child context"""
        # Arrange
        parent = ExecutionContext()

        # Act
        child = parent.create_child()

        # Assert
        self.assertEqual(child.parent, parent)
        self.assertIn(child, parent._children)

    def test_variable_inheritance(self):
        """Test variable inheritance from parent to child"""
        # Arrange
        parent = ExecutionContext()
        parent.variables.set("parent_var", "parent_value", VariableScope.WORKFLOW)

        # Act
        child = parent.create_child()
        child.variables.set("child_var", "child_value", VariableScope.WORKFLOW)

        # Assert
        self.assertEqual(child.variables.get("parent_var"), "parent_value")
        self.assertEqual(child.variables.get("child_var"), "child_value")
        self.assertIsNone(parent.variables.get("child_var"))

    def test_disable_variable_inheritance(self):
        """Test disabling variable inheritance"""
        # Arrange
        parent = ExecutionContext()
        parent.variables.set("parent_var", "parent_value", VariableScope.WORKFLOW)

        options = ContextOptions(inherit_variables=False)

        # Act
        child = parent.create_child(options=options)

        # Assert
        self.assertIsNone(child.variables.get("parent_var"))

    def test_state_transitions(self):
        """Test state transitions in context"""
        # Arrange
        context = ExecutionContext()

        # Act
        context.state.transition_to(ExecutionStateEnum.RUNNING)
        context.state.transition_to(ExecutionStateEnum.COMPLETED)

        # Assert
        self.assertEqual(context.state.current_state, ExecutionStateEnum.COMPLETED)

    def test_variable_change_tracking(self):
        """Test tracking variable changes"""
        # Arrange
        context = ExecutionContext()

        # Act
        context.variables.set("var1", "value1", VariableScope.WORKFLOW)
        context.variables.set("var1", "value2", VariableScope.WORKFLOW)

        # Assert
        history = context.get_variable_change_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].name, "var1")
        self.assertEqual(history[0].new_value, "value1")
        self.assertEqual(history[1].name, "var1")
        self.assertEqual(history[1].new_value, "value2")

    def test_state_change_tracking(self):
        """Test tracking state changes"""
        # Arrange
        context = ExecutionContext()

        # Act
        context.state.transition_to(ExecutionStateEnum.RUNNING)
        context.state.transition_to(ExecutionStateEnum.PAUSED)

        # Assert
        history = context.get_state_change_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0].old_state, ExecutionStateEnum.CREATED)
        self.assertEqual(history[0].new_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(history[1].old_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(history[1].new_state, ExecutionStateEnum.PAUSED)

    def test_disable_change_tracking(self):
        """Test disabling change tracking"""
        # Arrange
        options = ContextOptions(
            track_variable_changes=False,
            track_state_changes=False
        )
        context = ExecutionContext(options=options)

        # Act
        context.variables.set("var1", "value1", VariableScope.WORKFLOW)
        context.state.transition_to(ExecutionStateEnum.RUNNING)

        # Assert
        self.assertEqual(len(context.get_variable_change_history()), 0)
        self.assertEqual(len(context.get_state_change_history()), 0)

    def test_history_limits(self):
        """Test limiting history size"""
        # Arrange
        options = ContextOptions(
            max_variable_history=2,
            max_state_history=2
        )
        context = ExecutionContext(options=options)

        # Act - Add more changes than the limit
        context.variables.set("var1", "value1", VariableScope.WORKFLOW)
        context.variables.set("var2", "value2", VariableScope.WORKFLOW)
        context.variables.set("var3", "value3", VariableScope.WORKFLOW)

        context.state.transition_to(ExecutionStateEnum.RUNNING)
        context.state.transition_to(ExecutionStateEnum.PAUSED)
        context.state.transition_to(ExecutionStateEnum.RUNNING)

        # Assert - Only the most recent changes should be kept
        var_history = context.get_variable_change_history()
        state_history = context.get_state_change_history()

        self.assertEqual(len(var_history), 2)
        self.assertEqual(var_history[0].name, "var2")
        self.assertEqual(var_history[1].name, "var3")

        self.assertEqual(len(state_history), 2)
        self.assertEqual(state_history[0].new_state, ExecutionStateEnum.PAUSED)
        self.assertEqual(state_history[1].new_state, ExecutionStateEnum.RUNNING)

    def test_context_disposal(self):
        """Test disposing of a context"""
        # Arrange
        parent = ExecutionContext()
        child = parent.create_child()
        child.variables.set("var", "value", VariableScope.WORKFLOW)

        # Act
        child.dispose()

        # Assert
        self.assertNotIn(child, parent._children)
        self.assertIsNone(child.parent)
        self.assertFalse(child.variables.has("var"))

    def test_context_cloning(self):
        """Test cloning a context"""
        # Arrange
        context = ExecutionContext()
        context.variables.set("var", "value", VariableScope.WORKFLOW)
        context.state.transition_to(ExecutionStateEnum.RUNNING)

        # Create a child
        child = context.create_child()
        child.variables.set("child_var", "child_value", VariableScope.WORKFLOW)

        # Act
        clone = context.clone(include_children=True)

        # Assert
        self.assertNotEqual(clone.id, context.id)
        self.assertEqual(clone.variables.get("var"), "value")
        self.assertEqual(clone.state.current_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(len(clone._children), 1)
        self.assertEqual(clone._children[0].variables.get("child_var"), "child_value")

        # Clone without children
        clone_no_children = context.clone(include_children=False)
        self.assertEqual(len(clone_no_children._children), 0)

    def test_basic_serialization(self):
        """Test basic serialization without children"""
        # Arrange
        context_id = "test-basic-serialization"
        context = ExecutionContext(context_id=context_id)
        context.variables.set("var", "value", VariableScope.WORKFLOW)
        context.state.transition_to(ExecutionStateEnum.RUNNING)

        # Act
        serialized = context.to_dict(include_children=False)
        deserialized = ExecutionContext.from_dict(serialized)

        # Assert
        self.assertEqual(deserialized.id, context_id)
        self.assertEqual(deserialized.variables.get("var"), "value")
        self.assertEqual(deserialized.state.current_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(len(deserialized._children), 0)

    def test_child_context_properties(self):
        """Test child context properties after serialization"""
        # Arrange
        parent = ExecutionContext(context_id="parent-context")
        child = ExecutionContext(parent=parent, context_id="child-context")
        child.variables.set("child_var", "child_value", VariableScope.WORKFLOW)

        # Act - Just test the child properties directly
        serialized_child = child.to_dict()
        deserialized_child = ExecutionContext.from_dict(serialized_child)

        # Assert
        self.assertEqual(deserialized_child.id, "child-context")
        self.assertEqual(deserialized_child.variables.get("child_var"), "child_value")


if __name__ == "__main__":
    unittest.main()
