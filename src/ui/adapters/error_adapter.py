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
        self._load_default_configs()
    
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
