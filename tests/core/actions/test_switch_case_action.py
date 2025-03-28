"""Tests for the switch-case action"""
import unittest
from unittest.mock import MagicMock
from typing import Dict, Any

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.switch_case_action import SwitchCaseAction, CaseBranch
from src.core.conditions.condition_interface import ConditionInterface, ConditionResult


# Test condition for switch-case action tests
class TestCondition(ConditionInterface):
    """Test condition for switch-case action tests"""

    def __init__(self, return_value: bool = True, success: bool = True, message: str = ""):
        """Initialize the test condition"""
        self.return_value = return_value
        self.success = success
        self.message = message
        self.evaluated = False

    def evaluate(self, context: Dict[str, Any]) -> ConditionResult[bool]:
        """Evaluate the condition"""
        self.evaluated = True
        if self.success:
            return ConditionResult.create_success(self.return_value, self.message)
        else:
            return ConditionResult.create_failure(self.message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the condition to a dictionary"""
        return {
            "type": "test_condition",
            "return_value": self.return_value,
            "success": self.success,
            "message": self.message
        }


# Test action for switch-case action tests
class TestAction(BaseAction):
    """Test action for switch-case action tests"""

    def __init__(self, success: bool = True, description: str = None, action_id: str = None):
        """Initialize the test action"""
        super().__init__(description or "Test action", action_id)
        self.success = success
        self.executed = False

    @property
    def type(self) -> str:
        """Get the action type"""
        return "test_action"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        self.executed = True
        if self.success:
            return ActionResult.create_success(f"Executed: {self.description}")
        else:
            return ActionResult.create_failure(f"Failed: {self.description}")


class TestSwitchCaseAction(unittest.TestCase):
    """Test cases for the switch-case action"""

    def test_execute_first_case_matches(self):
        """Test executing when the first case matches"""
        # Arrange
        case1_condition = TestCondition(True)
        case1_action = TestAction()
        case1 = CaseBranch(case1_condition, [case1_action], "Case 1")

        case2_condition = TestCondition(True)
        case2_action = TestAction()
        case2 = CaseBranch(case2_condition, [case2_action], "Case 2")

        default_action = TestAction()

        action = SwitchCaseAction(
            description="Test switch-case",
            cases=[case1, case2],
            default_actions=[default_action]
        )

        # Act
        result = action.execute({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(case1_condition.evaluated)
        self.assertFalse(case2_condition.evaluated)  # Second case should not be evaluated
        self.assertTrue(case1_action.executed)
        self.assertFalse(case2_action.executed)
        self.assertFalse(default_action.executed)
        self.assertIn("Case 1", result.message)

    def test_execute_second_case_matches(self):
        """Test executing when the second case matches"""
        # Arrange
        case1_condition = TestCondition(False)
        case1_action = TestAction()
        case1 = CaseBranch(case1_condition, [case1_action], "Case 1")

        case2_condition = TestCondition(True)
        case2_action = TestAction()
        case2 = CaseBranch(case2_condition, [case2_action], "Case 2")

        default_action = TestAction()

        action = SwitchCaseAction(
            description="Test switch-case",
            cases=[case1, case2],
            default_actions=[default_action]
        )

        # Act
        result = action.execute({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(case1_condition.evaluated)
        self.assertTrue(case2_condition.evaluated)
        self.assertFalse(case1_action.executed)
        self.assertTrue(case2_action.executed)
        self.assertFalse(default_action.executed)
        self.assertIn("Case 2", result.message)

    def test_execute_default_case(self):
        """Test executing when no case matches"""
        # Arrange
        case1_condition = TestCondition(False)
        case1_action = TestAction()
        case1 = CaseBranch(case1_condition, [case1_action], "Case 1")

        case2_condition = TestCondition(False)
        case2_action = TestAction()
        case2 = CaseBranch(case2_condition, [case2_action], "Case 2")

        default_action = TestAction()

        action = SwitchCaseAction(
            description="Test switch-case",
            cases=[case1, case2],
            default_actions=[default_action]
        )

        # Act
        result = action.execute({})

        # Assert
        self.assertTrue(result.success)
        self.assertTrue(case1_condition.evaluated)
        self.assertTrue(case2_condition.evaluated)
        self.assertFalse(case1_action.executed)
        self.assertFalse(case2_action.executed)
        self.assertTrue(default_action.executed)
        self.assertIn("default", result.message)

    def test_execute_action_failure(self):
        """Test executing when an action fails"""
        # Arrange
        case1_condition = TestCondition(True)
        case1_action = TestAction(success=False)
        case1 = CaseBranch(case1_condition, [case1_action], "Case 1")

        action = SwitchCaseAction(
            description="Test switch-case",
            cases=[case1]
        )

        # Act
        result = action.execute({})

        # Assert
        self.assertFalse(result.success)
        self.assertTrue(case1_condition.evaluated)
        self.assertTrue(case1_action.executed)
        self.assertIn("failed", result.message.lower())

    def test_serialization(self):
        """Test serializing a SwitchCaseAction to dict"""
        # Arrange
        case1_condition = TestCondition(True)
        case1_action = TestAction()
        case1 = CaseBranch(case1_condition, [case1_action], "Case 1")

        case2_condition = TestCondition(False)
        case2_action = TestAction()
        case2 = CaseBranch(case2_condition, [case2_action], "Case 2")

        default_action = TestAction()

        action = SwitchCaseAction(
            description="Test switch-case",
            cases=[case1, case2],
            default_actions=[default_action],
            action_id="test-id"
        )

        # Act
        serialized = action.to_dict()

        # Assert
        self.assertEqual(serialized["id"], "test-id")
        self.assertEqual(serialized["type"], "switch_case")
        self.assertEqual(serialized["description"], "Test switch-case")
        self.assertEqual(len(serialized["cases"]), 2)
        self.assertEqual(serialized["cases"][0]["description"], "Case 1")
        self.assertEqual(serialized["cases"][1]["description"], "Case 2")
        self.assertEqual(len(serialized["default_actions"]), 1)

    def test_deserialization(self):
        """Test deserializing a dict to SwitchCaseAction"""
        # Arrange - Create a mock for the factories
        action_factory = MagicMock()
        condition_factory = MagicMock()

        # Mock the create_condition method
        condition_factory.create_condition.return_value = TestCondition(True)

        # Mock the create_action method
        action_factory.create_action.return_value = TestAction()

        # Create serialized data
        data = {
            "id": "test-id",
            "type": "switch_case",
            "description": "Test switch-case",
            "cases": [
                {
                    "condition": {"type": "test_condition"},
                    "actions": [{"type": "test_action"}],
                    "description": "Case 1"
                },
                {
                    "condition": {"type": "test_condition"},
                    "actions": [{"type": "test_action"}],
                    "description": "Case 2"
                }
            ],
            "default_actions": [
                {"type": "test_action"}
            ]
        }

        # Mock the get_instance methods
        with unittest.mock.patch('src.core.actions.action_factory.ActionFactory.get_instance',
                                return_value=action_factory):
            with unittest.mock.patch('src.core.conditions.condition_factory.ConditionFactory.get_instance',
                                    return_value=condition_factory):
                # Act
                action = SwitchCaseAction.from_dict(data)

        # Assert
        self.assertEqual(action.id, "test-id")
        self.assertEqual(action.description, "Test switch-case")
        self.assertEqual(len(action.cases), 2)
        self.assertEqual(action.cases[0].description, "Case 1")
        self.assertEqual(action.cases[1].description, "Case 2")
        self.assertEqual(len(action.default_actions), 1)


if __name__ == "__main__":
    unittest.main()
