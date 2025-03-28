"""Core interfaces for the automation system"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


class AutomationInterface(ABC):
    """Base interface for automation implementations"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the automation with configuration"""
        pass

    @abstractmethod
    def execute(self, script_path: Union[str, Path]) -> Dict[str, Any]:
        """Execute an automation script and return results"""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up resources"""
        pass


class StorageInterface(ABC):
    """Interface for storage implementations"""

    @abstractmethod
    def save(self, key: str, data: Any) -> None:
        """Save data with the given key"""
        pass

    @abstractmethod
    def load(self, key: str) -> Any:
        """Load data for the given key"""
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete data for the given key"""
        pass

    @abstractmethod
    def list_keys(self) -> List[str]:
        """List all available keys"""
        pass


class ReporterInterface(ABC):
    """Interface for result reporting implementations"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the reporter with configuration"""
        pass

    @abstractmethod
    def report(self, results: Dict[str, Any]) -> None:
        """Generate a report from results"""
        pass

    @abstractmethod
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all reports"""
        pass


class RunnerInterface(ABC):
    """Interface for execution runners"""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the runner with configuration"""
        pass

    @abstractmethod
    def run(
        self, automation: AutomationInterface, scripts: List[Union[str, Path]]
    ) -> Dict[str, Any]:
        """Run multiple scripts using the provided automation"""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stop all running executions"""
        pass


class ElementInterface(ABC):
    """Interface for web element interactions"""

    @abstractmethod
    def find(self, selector: str) -> Any:
        """Find an element using the selector"""
        pass

    @abstractmethod
    def click(self) -> None:
        """Click on the element"""
        pass

    @abstractmethod
    def type(self, text: str) -> None:
        """Type text into the element"""
        pass

    @abstractmethod
    def get_text(self) -> str:
        """Get the text content of the element"""
        pass

    @abstractmethod
    def is_visible(self) -> bool:
        """Check if the element is visible"""
        pass
