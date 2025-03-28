"""Execution context for the automation system"""
import uuid
from typing import Dict, Any, Optional, List, Set, Callable

from src.core.context.execution_state import ExecutionState, ExecutionStateEnum, StateChangeEvent
from src.core.context.variable_storage import VariableStorage, VariableScope, VariableChangeEvent
from src.core.context.context_options import ContextOptions


class ExecutionContext:
    """Context for executing actions with variable storage and state tracking"""

    def __init__(
        self,
        parent: Optional['ExecutionContext'] = None,
        options: Optional[ContextOptions] = None,
        context_id: Optional[str] = None
    ):
        """
        Initialize the execution context

        Args:
            parent: Optional parent context for inheritance
            options: Configuration options
            context_id: Optional unique identifier (generated if not provided)
        """
        self.id = context_id or str(uuid.uuid4())
        self.options = options or ContextOptions()
        self.parent = parent

        # Initialize variable storage with parent if needed
        parent_storage = parent.variables if parent and self.options.inherit_variables else None
        self.variables = VariableStorage(parent=parent_storage)

        # Initialize execution state
        self.state = ExecutionState()

        # Track child contexts
        self._children: List['ExecutionContext'] = []

        # Add this context as a child of the parent
        if parent:
            parent._add_child(self)

        # Set up event forwarding if tracking is enabled
        if self.options.track_variable_changes:
            self.variables.add_variable_change_listener(self._on_variable_change)

        if self.options.track_state_changes:
            self.state.add_state_change_listener(self._on_state_change)

        # Event history
        self._variable_change_history: List[VariableChangeEvent] = []
        self._state_change_history: List[StateChangeEvent] = []

    def _add_child(self, child: 'ExecutionContext') -> None:
        """
        Add a child context

        Args:
            child: Child context to add
        """
        if child not in self._children:
            self._children.append(child)

    def _remove_child(self, child: 'ExecutionContext') -> None:
        """
        Remove a child context

        Args:
            child: Child context to remove
        """
        if child in self._children:
            self._children.remove(child)

    def create_child(self, options: Optional[ContextOptions] = None) -> 'ExecutionContext':
        """
        Create a child context

        Args:
            options: Optional configuration options for the child

        Returns:
            New child context
        """
        return ExecutionContext(parent=self, options=options)

    def dispose(self) -> None:
        """
        Dispose of the context and clean up resources

        This removes the context from its parent and clears all variables
        """
        # Remove from parent
        if self.parent:
            self.parent._remove_child(self)
            self.parent = None

        # Clear variables
        self.variables.clear_all()

        # Dispose of children
        for child in list(self._children):
            child.dispose()

    def _on_variable_change(self, event: VariableChangeEvent) -> None:
        """
        Handle variable change events

        Args:
            event: Variable change event
        """
        # Add to history
        self._variable_change_history.append(event)

        # Trim history if needed
        if (
            self.options.max_variable_history > 0
            and len(self._variable_change_history) > self.options.max_variable_history
        ):
            self._variable_change_history = self._variable_change_history[-self.options.max_variable_history:]

    def _on_state_change(self, event: StateChangeEvent) -> None:
        """
        Handle state change events

        Args:
            event: State change event
        """
        # Add to history
        self._state_change_history.append(event)

        # Trim history if needed
        if (
            self.options.max_state_history > 0
            and len(self._state_change_history) > self.options.max_state_history
        ):
            self._state_change_history = self._state_change_history[-self.options.max_state_history:]

    def get_variable_change_history(self) -> List[VariableChangeEvent]:
        """
        Get the history of variable changes

        Returns:
            List of variable change events
        """
        return self._variable_change_history.copy()

    def get_state_change_history(self) -> List[StateChangeEvent]:
        """
        Get the history of state changes

        Returns:
            List of state change events
        """
        return self._state_change_history.copy()

    def clone(self, include_children: bool = False) -> 'ExecutionContext':
        """
        Create a clone of this context

        Args:
            include_children: Whether to clone child contexts

        Returns:
            New context with the same state and variables
        """
        # Create new context with same options but no parent
        clone = ExecutionContext(options=self.options)

        # Copy variables
        clone.variables = self.variables.clone()

        # Copy state
        clone.state = ExecutionState.from_dict(self.state.to_dict())

        # Clone children if requested
        if include_children:
            for child in self._children:
                child_clone = child.clone(include_children=True)
                child_clone.parent = clone
                clone._children.append(child_clone)

        return clone

    def to_dict(self, include_children: bool = False) -> Dict[str, Any]:
        """
        Convert the context to a dictionary

        Args:
            include_children: Whether to include child contexts

        Returns:
            Dictionary representation of the context
        """
        result = {
            "id": self.id,
            "options": self.options.to_dict(),
            "variables": self.variables.to_dict(),
            "state": self.state.to_dict()
        }

        if include_children:
            result["children"] = [child.to_dict(include_children=True) for child in self._children]

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any], parent: Optional['ExecutionContext'] = None) -> 'ExecutionContext':
        """
        Create a context from a dictionary

        Args:
            data: Dictionary representation of the context
            parent: Optional parent context

        Returns:
            Instantiated context
        """
        # Create options
        options_data = data.get("options", {})
        options = ContextOptions.from_dict(options_data)

        # Create context
        context_id = data.get("id")

        # Create context without parent to avoid automatic child registration
        context = cls(
            parent=None,  # Will set parent later if needed
            options=options,
            context_id=context_id
        )

        # Restore variables
        variables_data = data.get("variables", {})
        context.variables = VariableStorage.from_dict(
            variables_data,
            parent=parent.variables if parent and options.inherit_variables else None
        )

        # Restore state
        state_data = data.get("state", {})
        context.state = ExecutionState.from_dict(state_data)

        # Set parent after initialization to avoid automatic child registration
        if parent:
            context.parent = parent
            parent._add_child(context)

        # Restore children
        children_data = data.get("children", [])
        for child_data in children_data:
            # Create child without setting parent
            child = cls.from_dict(child_data, parent=None)
            # Manually set parent and add to children
            child.parent = context
            context._children.append(child)

        return context
