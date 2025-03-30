"""
Adapter for error handling to provide the interface expected by the UI.
SOLID: Single responsibility - adapting error handling operations.
KISS: Simple implementation with basic error configuration.
"""
import uuid
from typing import List, Dict, Any, Optional

from src.core.models import ErrorConfig as UIErrorConfig

class ErrorAdapter:
    """Adapter for error handling to provide the interface expected by the UI."""

    def __init__(self):
        """Initialize the adapter."""
        self.error_configs: Dict[str, UIErrorConfig] = {}
        self.recovery_strategies: List[Dict[str, Any]] = []
        self._load_default_configs()
        self._load_default_strategies()

    def _load_default_configs(self):
        """Load default error configurations."""
        default_configs = [
            UIErrorConfig(error_type="connection.timeout", severity="Warning", action="Retry"),
            UIErrorConfig(error_type="connection.failed", severity="Error", action="Stop"),
            UIErrorConfig(error_type="element.notfound", severity="Warning", action="Skip"),
            UIErrorConfig(error_type="credentials.invalid", severity="Error", action="Stop"),
            UIErrorConfig(error_type="browser.crashed", severity="Critical", action="Restart")
        ]

        for config in default_configs:
            self.error_configs[config.error_type] = config

    def _load_default_strategies(self):
        """Load default recovery strategies."""
        default_strategies = [
            {
                "id": str(uuid.uuid4()),
                "name": "Network Retry",
                "error_type": "Network",
                "action": "Retry",
                "max_retries": 3,
                "retry_delay": 1000
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Authentication Abort",
                "error_type": "Authentication",
                "action": "Abort",
                "max_retries": 0,
                "retry_delay": 0
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Timeout Skip",
                "error_type": "Timeout",
                "action": "Skip",
                "max_retries": 0,
                "retry_delay": 0
            }
        ]

        for strategy in default_strategies:
            self.recovery_strategies.append(strategy)

    def get_all_error_configs(self) -> List[UIErrorConfig]:
        """
        Get all error configurations.

        Returns:
            List of error configurations in the UI-expected format.
        """
        return list(self.error_configs.values())

    def get_error_config(self, error_type: str) -> Optional[UIErrorConfig]:
        """
        Get an error configuration by type.

        Args:
            error_type: Error type identifier

        Returns:
            Error configuration in the UI-expected format, or None if not found.
        """
        return self.error_configs.get(error_type)

    def add_error_config(self, error_type: str, severity: str = "Warning", action: str = "Ignore", custom_action: Optional[str] = None) -> UIErrorConfig:
        """
        Add a new error configuration.

        Args:
            error_type: Error type identifier
            severity: Error severity (Info, Warning, Error, Critical, Fatal)
            action: Error action (Ignore, Log, Retry, Skip, Stop, Custom)
            custom_action: Custom action script or command

        Returns:
            The new error configuration in the UI-expected format.
        """
        config = UIErrorConfig(
            error_type=error_type,
            severity=severity,
            action=action,
            custom_action=custom_action
        )

        self.error_configs[error_type] = config
        return config

    def update_error_config(self, error_type: str, severity: Optional[str] = None, action: Optional[str] = None, custom_action: Optional[str] = None) -> Optional[UIErrorConfig]:
        """
        Update an existing error configuration.

        Args:
            error_type: Error type identifier
            severity: Error severity (Info, Warning, Error, Critical, Fatal)
            action: Error action (Ignore, Log, Retry, Skip, Stop, Custom)
            custom_action: Custom action script or command

        Returns:
            The updated error configuration in the UI-expected format, or None if not found.
        """
        config = self.error_configs.get(error_type)
        if not config:
            return None

        if severity is not None:
            config.severity = severity

        if action is not None:
            config.action = action

        if custom_action is not None:
            config.custom_action = custom_action

        return config

    def delete_error_config(self, error_type: str) -> bool:
        """
        Delete an error configuration.

        Args:
            error_type: Error type identifier

        Returns:
            True if the error configuration was deleted, False if not found.
        """
        if error_type in self.error_configs:
            del self.error_configs[error_type]
            return True
        return False

    def get_error_hierarchy(self) -> Dict[str, Dict]:
        """
        Get the error type hierarchy.

        Returns:
            Dictionary representing the hierarchical structure of error types.
        """
        hierarchy = {}

        for error_type in self.error_configs:
            parts = error_type.split('.')
            current = hierarchy

            for i, part in enumerate(parts):
                if part not in current:
                    current[part] = {}

                if i < len(parts) - 1:
                    current = current[part]

        return hierarchy

    # === Recovery Strategy Methods ===

    def get_recovery_strategies(self) -> List[Dict[str, Any]]:
        """
        Get all recovery strategies.

        Returns:
            List of recovery strategies.
        """
        return self.recovery_strategies

    def get_recovery_strategy(self, strategy_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a recovery strategy by ID.

        Args:
            strategy_id: Strategy ID

        Returns:
            Recovery strategy, or None if not found.
        """
        return next((s for s in self.recovery_strategies if s["id"] == strategy_id), None)

    def add_recovery_strategy(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new recovery strategy.

        Args:
            strategy: Recovery strategy data

        Returns:
            The added strategy.
        """
        if "id" not in strategy:
            strategy["id"] = str(uuid.uuid4())

        self.recovery_strategies.append(strategy)
        return strategy

    def update_recovery_strategy(self, strategy_id: str, strategy_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing recovery strategy.

        Args:
            strategy_id: Strategy ID
            strategy_data: New strategy data

        Returns:
            The updated strategy, or None if not found.
        """
        strategy_index = next((i for i, s in enumerate(self.recovery_strategies) if s["id"] == strategy_id), -1)

        if strategy_index == -1:
            return None

        self.recovery_strategies[strategy_index] = strategy_data
        return strategy_data

    def delete_recovery_strategy(self, strategy_id: str) -> bool:
        """
        Delete a recovery strategy.

        Args:
            strategy_id: Strategy ID

        Returns:
            True if the strategy was deleted, False if not found.
        """
        strategy_index = next((i for i, s in enumerate(self.recovery_strategies) if s["id"] == strategy_id), -1)

        if strategy_index == -1:
            return False

        del self.recovery_strategies[strategy_index]
        return True
