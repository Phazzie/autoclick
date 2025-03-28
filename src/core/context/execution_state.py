"""Execution state management for the automation system"""
from enum import Enum, auto
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime


class StateChangeEvent:
    """Event raised when the execution state changes"""

    def __init__(self, old_state: 'ExecutionStateEnum', new_state: 'ExecutionStateEnum', timestamp: Optional[datetime] = None):
        """
        Initialize the state change event

        Args:
            old_state: Previous execution state
            new_state: New execution state
            timestamp: Time of the state change (defaults to now)
        """
        self.old_state = old_state
        self.new_state = new_state
        self.timestamp = timestamp or datetime.now()

    def __str__(self) -> str:
        """String representation of the state change event"""
        return f"StateChangeEvent: {self.old_state.name} -> {self.new_state.name} at {self.timestamp}"


class ExecutionStateEnum(Enum):
    """Enumeration of possible execution states"""
    CREATED = auto()    # Initial state when context is created
    RUNNING = auto()    # Execution is in progress
    PAUSED = auto()     # Execution is temporarily paused
    COMPLETED = auto()  # Execution completed successfully
    FAILED = auto()     # Execution failed with an error
    ABORTED = auto()    # Execution was manually aborted


# Define valid state transitions
VALID_TRANSITIONS = {
    ExecutionStateEnum.CREATED: [ExecutionStateEnum.RUNNING],
    ExecutionStateEnum.RUNNING: [ExecutionStateEnum.PAUSED, ExecutionStateEnum.COMPLETED, ExecutionStateEnum.FAILED, ExecutionStateEnum.ABORTED],
    ExecutionStateEnum.PAUSED: [ExecutionStateEnum.RUNNING, ExecutionStateEnum.ABORTED],
    ExecutionStateEnum.COMPLETED: [],  # Terminal state
    ExecutionStateEnum.FAILED: [],     # Terminal state
    ExecutionStateEnum.ABORTED: []     # Terminal state
}


class ExecutionState:
    """Manages the execution state and transitions"""

    def __init__(self, initial_state: ExecutionStateEnum = ExecutionStateEnum.CREATED):
        """
        Initialize the execution state

        Args:
            initial_state: Starting state (default: CREATED)
        """
        self._current_state = initial_state
        self._state_history: List[StateChangeEvent] = []
        self._state_change_listeners: List[Callable[[StateChangeEvent], None]] = []

    @property
    def current_state(self) -> ExecutionStateEnum:
        """Get the current execution state"""
        return self._current_state

    @property
    def state_history(self) -> List[StateChangeEvent]:
        """Get the history of state changes (copy to prevent modification)"""
        return self._state_history.copy()

    def can_transition_to(self, new_state: ExecutionStateEnum) -> bool:
        """
        Check if a transition to the given state is valid

        Args:
            new_state: Target state to check

        Returns:
            True if the transition is valid, False otherwise
        """
        return new_state in VALID_TRANSITIONS.get(self._current_state, [])

    def transition_to(self, new_state: ExecutionStateEnum) -> bool:
        """
        Attempt to transition to a new state

        Args:
            new_state: Target state

        Returns:
            True if the transition was successful, False otherwise

        Raises:
            ValueError: If the transition is invalid
        """
        if not self.can_transition_to(new_state):
            raise ValueError(
                f"Invalid state transition: {self._current_state.name} -> {new_state.name}. "
                f"Valid transitions from {self._current_state.name} are: "
                f"{[s.name for s in VALID_TRANSITIONS.get(self._current_state, [])]}"
            )

        # Create state change event
        old_state = self._current_state
        event = StateChangeEvent(old_state, new_state)

        # Update state
        self._current_state = new_state
        self._state_history.append(event)

        # Notify listeners
        self._notify_state_change(event)

        return True

    def add_state_change_listener(self, listener: Callable[[StateChangeEvent], None]) -> None:
        """
        Add a listener for state change events

        Args:
            listener: Callback function that will be called when state changes
        """
        if listener not in self._state_change_listeners:
            self._state_change_listeners.append(listener)

    def remove_state_change_listener(self, listener: Callable[[StateChangeEvent], None]) -> None:
        """
        Remove a state change listener

        Args:
            listener: Listener to remove
        """
        if listener in self._state_change_listeners:
            self._state_change_listeners.remove(listener)

    def _notify_state_change(self, event: StateChangeEvent) -> None:
        """
        Notify all listeners of a state change

        Args:
            event: State change event
        """
        for listener in self._state_change_listeners:
            try:
                listener(event)
            except Exception as e:
                # In a real application, you might want to log this error
                print(f"Error in state change listener: {str(e)}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the execution state to a dictionary

        Returns:
            Dictionary representation of the execution state
        """
        return {
            "current_state": self._current_state.name,
            "state_history": [
                {
                    "old_state": event.old_state.name,
                    "new_state": event.new_state.name,
                    "timestamp": event.timestamp.isoformat()
                }
                for event in self._state_history
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExecutionState':
        """
        Create an execution state from a dictionary

        Args:
            data: Dictionary representation of the execution state

        Returns:
            Instantiated execution state
        """
        # Create instance with the current state
        current_state_name = data.get("current_state", ExecutionStateEnum.CREATED.name)
        current_state = ExecutionStateEnum[current_state_name]
        instance = cls(initial_state=current_state)

        # Reconstruct state history
        state_history = data.get("state_history", [])
        for event_data in state_history:
            old_state = ExecutionStateEnum[event_data["old_state"]]
            new_state = ExecutionStateEnum[event_data["new_state"]]
            timestamp = datetime.fromisoformat(event_data["timestamp"])
            instance._state_history.append(StateChangeEvent(old_state, new_state, timestamp))

        return instance
