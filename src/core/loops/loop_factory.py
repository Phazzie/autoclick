"""
Loop factory.

This module provides a factory for creating loop instances.
"""
from typing import Dict, Any, List, Optional
import uuid


class Loop:
    """
    Base class for loops.
    
    This class provides a base implementation for loops.
    """
    
    def __init__(self, loop_type: str, loop_id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a loop.
        
        Args:
            loop_type: Type of loop
            loop_id: Optional ID for the loop
            name: Optional name for the loop
            description: Optional description for the loop
            config: Optional configuration for the loop
        """
        self.loop_type = loop_type
        self.loop_id = loop_id or str(uuid.uuid4())
        self.name = name or f"{loop_type.capitalize()} Loop"
        self.description = description or ""
        self.config = config or {}
    
    def validate(self) -> List[str]:
        """
        Validate the loop configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate basic properties
        if not self.loop_id:
            errors.append("Loop ID is required")
        
        if not self.name:
            errors.append("Loop name is required")
        
        return errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the loop to a dictionary.
        
        Returns:
            Dictionary representation of the loop
        """
        return {
            "loop_id": self.loop_id,
            "loop_type": self.loop_type,
            "name": self.name,
            "description": self.description,
            "config": self.config
        }


class CountLoop(Loop):
    """
    Loop that iterates a fixed number of times.
    
    This class provides a loop that iterates a fixed number of times.
    """
    
    def __init__(self, loop_id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a count loop.
        
        Args:
            loop_id: Optional ID for the loop
            name: Optional name for the loop
            description: Optional description for the loop
            config: Optional configuration for the loop
        """
        super().__init__("count", loop_id, name, description, config)
    
    def validate(self) -> List[str]:
        """
        Validate the loop configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = super().validate()
        
        # Validate count
        if "count" not in self.config:
            errors.append("Count is required")
        elif not isinstance(self.config["count"], int):
            errors.append("Count must be an integer")
        elif self.config["count"] < 0:
            errors.append("Count must be non-negative")
        
        return errors


class WhileLoop(Loop):
    """
    Loop that iterates while a condition is true.
    
    This class provides a loop that iterates while a condition is true.
    """
    
    def __init__(self, loop_id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a while loop.
        
        Args:
            loop_id: Optional ID for the loop
            name: Optional name for the loop
            description: Optional description for the loop
            config: Optional configuration for the loop
        """
        super().__init__("while", loop_id, name, description, config)
    
    def validate(self) -> List[str]:
        """
        Validate the loop configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = super().validate()
        
        # Validate condition
        if "condition" not in self.config:
            errors.append("Condition is required")
        
        return errors


class ForEachLoop(Loop):
    """
    Loop that iterates over items in a collection.
    
    This class provides a loop that iterates over items in a collection.
    """
    
    def __init__(self, loop_id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize a for-each loop.
        
        Args:
            loop_id: Optional ID for the loop
            name: Optional name for the loop
            description: Optional description for the loop
            config: Optional configuration for the loop
        """
        super().__init__("for_each", loop_id, name, description, config)
    
    def validate(self) -> List[str]:
        """
        Validate the loop configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = super().validate()
        
        # Validate collection
        if "collection" not in self.config:
            errors.append("Collection is required")
        
        # Validate item variable
        if "item_variable" not in self.config:
            errors.append("Item variable is required")
        elif not isinstance(self.config["item_variable"], str):
            errors.append("Item variable must be a string")
        
        return errors


class UntilLoop(Loop):
    """
    Loop that iterates until a condition is true.
    
    This class provides a loop that iterates until a condition is true.
    """
    
    def __init__(self, loop_id: Optional[str] = None, name: Optional[str] = None,
                 description: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        """
        Initialize an until loop.
        
        Args:
            loop_id: Optional ID for the loop
            name: Optional name for the loop
            description: Optional description for the loop
            config: Optional configuration for the loop
        """
        super().__init__("until", loop_id, name, description, config)
    
    def validate(self) -> List[str]:
        """
        Validate the loop configuration.
        
        Returns:
            List of validation errors, empty if valid
        """
        errors = super().validate()
        
        # Validate condition
        if "condition" not in self.config:
            errors.append("Condition is required")
        
        return errors


class LoopFactory:
    """
    Factory for creating loop instances.
    
    This class provides methods for creating and managing loops.
    """
    
    def __init__(self):
        """Initialize the loop factory."""
        self._loop_types = {
            "count": CountLoop,
            "while": WhileLoop,
            "for_each": ForEachLoop,
            "until": UntilLoop
        }
        self._loop_schemas = {
            "count": {
                "type": "object",
                "properties": {
                    "count": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Number of iterations"
                    },
                    "index_variable": {
                        "type": "string",
                        "description": "Variable to store the current index"
                    }
                },
                "required": ["count"]
            },
            "while": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "object",
                        "description": "Condition to evaluate"
                    },
                    "max_iterations": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Maximum number of iterations"
                    }
                },
                "required": ["condition"]
            },
            "for_each": {
                "type": "object",
                "properties": {
                    "collection": {
                        "type": "string",
                        "description": "Collection to iterate over"
                    },
                    "item_variable": {
                        "type": "string",
                        "description": "Variable to store the current item"
                    },
                    "index_variable": {
                        "type": "string",
                        "description": "Variable to store the current index"
                    }
                },
                "required": ["collection", "item_variable"]
            },
            "until": {
                "type": "object",
                "properties": {
                    "condition": {
                        "type": "object",
                        "description": "Condition to evaluate"
                    },
                    "max_iterations": {
                        "type": "integer",
                        "minimum": 0,
                        "description": "Maximum number of iterations"
                    }
                },
                "required": ["condition"]
            }
        }
    
    def get_loop_types(self) -> List[str]:
        """
        Get all available loop types.
        
        Returns:
            List of loop types
        """
        return list(self._loop_types.keys())
    
    def get_loop_schema(self, loop_type: str) -> Dict[str, Any]:
        """
        Get the schema for a loop type.
        
        Args:
            loop_type: Loop type
            
        Returns:
            Schema for the loop type
            
        Raises:
            ValueError: If the loop type is not supported
        """
        if loop_type not in self._loop_schemas:
            raise ValueError(f"Unsupported loop type: {loop_type}")
        
        return self._loop_schemas[loop_type]
    
    def create_loop(self, loop_type: str, loop_data: Dict[str, Any]) -> Loop:
        """
        Create a loop.
        
        Args:
            loop_type: Loop type
            loop_data: Loop data
            
        Returns:
            Created loop
            
        Raises:
            ValueError: If the loop type is not supported
        """
        if loop_type not in self._loop_types:
            raise ValueError(f"Unsupported loop type: {loop_type}")
        
        # Create the loop
        loop_class = self._loop_types[loop_type]
        loop = loop_class(
            loop_id=loop_data.get("loop_id"),
            name=loop_data.get("name"),
            description=loop_data.get("description"),
            config=loop_data.get("config", {})
        )
        
        return loop
