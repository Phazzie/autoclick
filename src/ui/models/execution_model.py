"""Model for workflow execution"""
from datetime import datetime
from typing import Dict, Any, List


class ExecutionModel:
    """Model for workflow execution"""
    
    def __init__(self) -> None:
        """Initialize the execution model"""
        self._running = False
        self._log_entries = []
        self._options = {
            "browser_type": "chrome",
            "headless": False,
            "timeout": 30
        }
    
    def start_execution(self, workflow: Dict[str, Any]) -> None:
        """
        Start execution of a workflow
        
        Args:
            workflow: Workflow to execute
        """
        self._running = True
        self._log_entries = []
        self.add_log_entry("info", "Execution started")
    
    def stop_execution(self) -> None:
        """Stop execution"""
        self._running = False
        self.add_log_entry("info", "Execution stopped")
    
    def add_log_entry(self, level: str, message: str) -> None:
        """
        Add a log entry
        
        Args:
            level: Log level (info, warning, error)
            message: Log message
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        self._log_entries.append(entry)
    
    def get_log_entries(self) -> List[Dict[str, Any]]:
        """
        Get all log entries
        
        Returns:
            A copy of the log entries list
        """
        return self._log_entries.copy()
    
    def is_execution_running(self) -> bool:
        """
        Check if execution is running
        
        Returns:
            True if execution is running, False otherwise
        """
        return self._running
    
    def set_option(self, key: str, value: Any) -> None:
        """
        Set an execution option
        
        Args:
            key: Option key
            value: Option value
        """
        self._options[key] = value
    
    def get_options(self) -> Dict[str, Any]:
        """
        Get all execution options
        
        Returns:
            A copy of the options dictionary
        """
        return self._options.copy()
