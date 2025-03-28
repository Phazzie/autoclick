"""While loop action for repeating actions while a condition is true"""
from typing import Dict, Any, List, Optional

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.conditions.condition_interface import ConditionInterface
from src.core.actions.action_factory import ActionFactory


@ActionFactory.register("while_loop")
class WhileLoopAction(BaseAction):
    """Action that executes a sequence of actions while a condition is true"""

    def __init__(
        self,
        description: str,
        condition: ConditionInterface,
        actions: List[BaseAction],
        max_iterations: Optional[int] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the while loop action

        Args:
            description: Human-readable description of the action
            condition: Condition to evaluate for each iteration
            actions: Actions to execute in each iteration
            max_iterations: Maximum number of iterations (None for unlimited)
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.condition = condition
        self.actions = actions
        self.max_iterations = max_iterations

    @property
    def type(self) -> str:
        """Get the action type"""
        return "while_loop"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        iteration = 0
        all_results = []
        
        # Add loop control variables to context
        context["loop_iteration"] = iteration
        context["loop_break"] = False
        context["loop_continue"] = False

        # Execute the loop
        while True:
            # Check if we've reached the maximum number of iterations
            if self.max_iterations is not None and iteration >= self.max_iterations:
                return ActionResult.create_success(
                    f"While loop completed after reaching maximum iterations ({self.max_iterations})",
                    {"iterations": iteration, "results": all_results}
                )

            # Evaluate the condition
            condition_result = self.condition.evaluate(context)
            if not condition_result:
                # Condition is false, exit the loop
                return ActionResult.create_success(
                    f"While loop completed after {iteration} iterations",
                    {"iterations": iteration, "results": all_results}
                )

            # Execute the actions
            iteration_results = []
            for action in self.actions:
                # Check for break
                if context.get("loop_break", False):
                    break

                # Check for continue
                if context.get("loop_continue", False):
                    context["loop_continue"] = False
                    break

                # Execute the action
                result = action.execute(context)
                iteration_results.append(result)

                # If an action fails, exit the loop
                if not result.success:
                    return ActionResult.create_failure(
                        f"While loop failed in iteration {iteration}: {result.message}",
                        {"iterations": iteration, "results": all_results, "failed_result": result}
                    )

            # Add the results from this iteration
            all_results.append(iteration_results)

            # Check for break after all actions
            if context.get("loop_break", False):
                return ActionResult.create_success(
                    f"While loop exited with break after {iteration + 1} iterations",
                    {"iterations": iteration + 1, "results": all_results}
                )

            # Increment the iteration counter
            iteration += 1
            context["loop_iteration"] = iteration

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "condition": self.condition.to_dict() if hasattr(self.condition, "to_dict") else {"type": "unknown"},
            "actions": [action.to_dict() for action in self.actions],
            "max_iterations": self.max_iterations
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'WhileLoopAction':
        """
        Create an action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory

        # Get the condition factory
        from src.core.conditions.condition_factory import ConditionFactory
        condition_data = data.get("condition", {})
        condition = ConditionFactory.create_condition(condition_data)

        # Create actions
        actions_data = data.get("actions", [])
        actions = [
            ActionFactory.get_instance().create_from_dict(action_data)
            for action_data in actions_data
        ]

        return cls(
            description=data.get("description", ""),
            condition=condition,
            actions=actions,
            max_iterations=data.get("max_iterations"),
            action_id=data.get("id")
        )
