"""For-each loop action for iterating over collections"""
from typing import Dict, Any, List, Optional, Iterable

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory


@ActionFactory.register("for_each")
class ForEachAction(BaseAction):
    """Action that executes a sequence of actions for each item in a collection"""

    def __init__(
        self,
        description: str,
        collection_variable: str,
        item_variable: str,
        actions: List[BaseAction],
        action_id: Optional[str] = None
    ):
        """
        Initialize the for-each loop action

        Args:
            description: Human-readable description of the action
            collection_variable: Name of the variable containing the collection
            item_variable: Name of the variable to store the current item
            actions: Actions to execute for each item
            action_id: Optional unique identifier (generated if not provided)
        """
        super().__init__(description, action_id)
        self.collection_variable = collection_variable
        self.item_variable = item_variable
        self.actions = actions

    @property
    def type(self) -> str:
        """Get the action type"""
        return "for_each"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the action

        Args:
            context: Execution context containing variables, browser, etc.

        Returns:
            Result of the action execution
        """
        # Get the collection from the context
        collection = context.get(self.collection_variable)
        if collection is None:
            return ActionResult.create_failure(
                f"Collection variable not found: {self.collection_variable}"
            )

        # Ensure the collection is iterable
        if not isinstance(collection, Iterable):
            return ActionResult.create_failure(
                f"Collection variable is not iterable: {self.collection_variable}"
            )

        # Initialize loop variables
        all_results = []
        index = 0
        
        # Add loop control variables to context
        context["loop_index"] = index
        context["loop_break"] = False
        context["loop_continue"] = False

        # Iterate over the collection
        for item in collection:
            # Store the current item in the context
            context[self.item_variable] = item
            context["loop_index"] = index

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
                        f"For-each loop failed at index {index}: {result.message}",
                        {"index": index, "results": all_results, "failed_result": result}
                    )

            # Add the results from this iteration
            all_results.append(iteration_results)

            # Check for break after all actions
            if context.get("loop_break", False):
                return ActionResult.create_success(
                    f"For-each loop exited with break after {index + 1} iterations",
                    {"iterations": index + 1, "results": all_results}
                )

            # Increment the index
            index += 1

        # Remove the item variable from the context
        if self.item_variable in context:
            del context[self.item_variable]

        return ActionResult.create_success(
            f"For-each loop completed with {index} iterations",
            {"iterations": index, "results": all_results}
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "collection_variable": self.collection_variable,
            "item_variable": self.item_variable,
            "actions": [action.to_dict() for action in self.actions]
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ForEachAction':
        """
        Create an action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        from src.core.actions.action_factory import ActionFactory

        # Create actions
        actions_data = data.get("actions", [])
        actions = [
            ActionFactory.get_instance().create_from_dict(action_data)
            for action_data in actions_data
        ]

        return cls(
            description=data.get("description", ""),
            collection_variable=data.get("collection_variable", ""),
            item_variable=data.get("item_variable", ""),
            actions=actions,
            action_id=data.get("id")
        )
