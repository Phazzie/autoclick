"""Options for configuring the execution context"""
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class ContextOptions:
    """Configuration options for the execution context"""

    # Whether to inherit variables from parent context
    inherit_variables: bool = True

    # Whether to track variable changes
    track_variable_changes: bool = True

    # Whether to track state changes
    track_state_changes: bool = True

    # Maximum number of state changes to track (0 = unlimited)
    max_state_history: int = 100

    # Maximum number of variable changes to track (0 = unlimited)
    max_variable_history: int = 100

    # Custom metadata for the context
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Ensure metadata is a copy to prevent shared references"""
        self.metadata = self.metadata.copy()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert options to a dictionary

        Returns:
            Dictionary representation of the options
        """
        return {
            "inherit_variables": self.inherit_variables,
            "track_variable_changes": self.track_variable_changes,
            "track_state_changes": self.track_state_changes,
            "max_state_history": self.max_state_history,
            "max_variable_history": self.max_variable_history,
            "metadata": self.metadata.copy()
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContextOptions':
        """
        Create options from a dictionary

        Args:
            data: Dictionary representation of the options

        Returns:
            Instantiated options
        """
        return cls(
            inherit_variables=data.get("inherit_variables", True),
            track_variable_changes=data.get("track_variable_changes", True),
            track_state_changes=data.get("track_state_changes", True),
            max_state_history=data.get("max_state_history", 100),
            max_variable_history=data.get("max_variable_history", 100),
            metadata=data.get("metadata", {}).copy()
        )
