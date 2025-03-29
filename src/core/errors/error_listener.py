"""Error listener interface for the automation system"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List, Callable

from src.core.errors.error_types import Error


class ErrorEvent:
    """Event raised when an error occurs"""
    
    def __init__(
        self,
        error: Error,
        context: Optional[Dict[str, Any]] = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize the error event
        
        Args:
            error: The error that occurred
            context: Execution context when the error occurred
            timestamp: Time of the error (defaults to now)
        """
        self.error = error
        self.context = context or {}
        self.timestamp = timestamp or datetime.now()
        
    def __str__(self) -> str:
        """String representation of the error event"""
        return f"ErrorEvent: {self.error} at {self.timestamp}"
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the error event to a dictionary
        
        Returns:
            Dictionary representation of the error event
        """
        return {
            "error": self.error.to_dict(),
            "context": self.context,
            "timestamp": self.timestamp.isoformat()
        }


class ErrorListener(ABC):
    """Interface for error listeners"""
    
    @abstractmethod
    def on_error(self, event: ErrorEvent) -> bool:
        """
        Called when an error occurs
        
        Args:
            event: Error event containing the error and context
            
        Returns:
            True if the error was handled, False otherwise
        """
        pass


# Type for error callback functions
ErrorCallback = Callable[[ErrorEvent], bool]


class CallbackErrorListener(ErrorListener):
    """Error listener that delegates to a callback function"""
    
    def __init__(self, callback: ErrorCallback):
        """
        Initialize the callback error listener
        
        Args:
            callback: Function to call when an error occurs
        """
        self.callback = callback
        
    def on_error(self, event: ErrorEvent) -> bool:
        """
        Call the callback function when an error occurs
        
        Args:
            event: Error event containing the error and context
            
        Returns:
            Result from the callback function
        """
        return self.callback(event)


class CompositeErrorListener(ErrorListener):
    """Error listener that delegates to multiple listeners"""
    
    def __init__(self, listeners: Optional[List[ErrorListener]] = None):
        """
        Initialize the composite error listener
        
        Args:
            listeners: List of error listeners
        """
        self.listeners = listeners or []
        
    def add_listener(self, listener: ErrorListener) -> None:
        """
        Add a listener
        
        Args:
            listener: Error listener to add
        """
        if listener not in self.listeners:
            self.listeners.append(listener)
            
    def remove_listener(self, listener: ErrorListener) -> None:
        """
        Remove a listener
        
        Args:
            listener: Error listener to remove
        """
        if listener in self.listeners:
            self.listeners.remove(listener)
            
    def on_error(self, event: ErrorEvent) -> bool:
        """
        Notify all listeners of the error
        
        Args:
            event: Error event containing the error and context
            
        Returns:
            True if any listener handled the error, False otherwise
        """
        handled = False
        
        for listener in self.listeners:
            try:
                if listener.on_error(event):
                    handled = True
            except Exception:
                # Don't let exceptions in listeners propagate
                pass
                
        return handled
