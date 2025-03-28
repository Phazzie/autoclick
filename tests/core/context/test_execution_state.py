"""Tests for the ExecutionState class"""
import unittest
from datetime import datetime
from unittest.mock import MagicMock

from src.core.context.execution_state import ExecutionState, ExecutionStateEnum, StateChangeEvent, VALID_TRANSITIONS


class TestExecutionState(unittest.TestCase):
    """Test cases for the ExecutionState class"""

    def test_initial_state(self):
        """Test the initial state of ExecutionState"""
        # Arrange & Act
        state = ExecutionState()

        # Assert
        self.assertEqual(state.current_state, ExecutionStateEnum.CREATED)
        self.assertEqual(len(state.state_history), 0)

    def test_valid_transition(self):
        """Test a valid state transition"""
        # Arrange
        state = ExecutionState()

        # Act
        result = state.transition_to(ExecutionStateEnum.RUNNING)

        # Assert
        self.assertTrue(result)
        self.assertEqual(state.current_state, ExecutionStateEnum.RUNNING)
        self.assertEqual(len(state.state_history), 1)
        self.assertEqual(state.state_history[0].old_state, ExecutionStateEnum.CREATED)
        self.assertEqual(state.state_history[0].new_state, ExecutionStateEnum.RUNNING)

    def test_invalid_transition(self):
        """Test an invalid state transition"""
        # Arrange
        state = ExecutionState()

        # Act & Assert
        with self.assertRaises(ValueError):
            state.transition_to(ExecutionStateEnum.COMPLETED)

    def test_multiple_transitions(self):
        """Test multiple state transitions"""
        # Arrange
        state = ExecutionState()

        # Act
        state.transition_to(ExecutionStateEnum.RUNNING)
        state.transition_to(ExecutionStateEnum.PAUSED)
        state.transition_to(ExecutionStateEnum.RUNNING)
        state.transition_to(ExecutionStateEnum.COMPLETED)

        # Assert
        self.assertEqual(state.current_state, ExecutionStateEnum.COMPLETED)
        self.assertEqual(len(state.state_history), 4)

    def test_terminal_state(self):
        """Test that terminal states cannot transition further"""
        # Arrange
        state = ExecutionState()
        state.transition_to(ExecutionStateEnum.RUNNING)
        state.transition_to(ExecutionStateEnum.COMPLETED)

        # Act & Assert
        with self.assertRaises(ValueError):
            state.transition_to(ExecutionStateEnum.RUNNING)

    def test_state_change_listener(self):
        """Test state change listener notification"""
        # Arrange
        state = ExecutionState()
        mock_listener = MagicMock()
        state.add_state_change_listener(mock_listener)

        # Act
        state.transition_to(ExecutionStateEnum.RUNNING)

        # Assert
        mock_listener.assert_called_once()
        event = mock_listener.call_args[0][0]
        self.assertEqual(event.old_state, ExecutionStateEnum.CREATED)
        self.assertEqual(event.new_state, ExecutionStateEnum.RUNNING)

    def test_remove_state_change_listener(self):
        """Test removing a state change listener"""
        # Arrange
        state = ExecutionState()
        mock_listener = MagicMock()
        state.add_state_change_listener(mock_listener)
        state.remove_state_change_listener(mock_listener)

        # Act
        state.transition_to(ExecutionStateEnum.RUNNING)

        # Assert
        mock_listener.assert_not_called()

    def test_serialization(self):
        """Test serializing and deserializing state"""
        # Arrange
        state = ExecutionState()
        state.transition_to(ExecutionStateEnum.RUNNING)
        state.transition_to(ExecutionStateEnum.PAUSED)

        # Act
        serialized = state.to_dict()
        deserialized = ExecutionState.from_dict(serialized)

        # Assert
        self.assertEqual(deserialized.current_state, state.current_state)
        self.assertEqual(len(deserialized.state_history), len(state.state_history))

    def test_can_transition_to(self):
        """Test checking if a transition is valid"""
        # Arrange
        state = ExecutionState()

        # Act & Assert
        self.assertTrue(state.can_transition_to(ExecutionStateEnum.RUNNING))
        self.assertFalse(state.can_transition_to(ExecutionStateEnum.COMPLETED))

        # Transition to RUNNING
        state.transition_to(ExecutionStateEnum.RUNNING)

        # Now we can transition to COMPLETED
        self.assertTrue(state.can_transition_to(ExecutionStateEnum.COMPLETED))

    def test_valid_transitions_completeness(self):
        """Test that all states have valid transitions defined"""
        # Arrange & Act & Assert
        for state in ExecutionStateEnum:
            self.assertIn(state, VALID_TRANSITIONS)


if __name__ == "__main__":
    unittest.main()
