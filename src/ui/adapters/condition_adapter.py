"""
Adapter for condition operations to provide the interface expected by the UI.
SOLID: Single responsibility - adapting condition operations.
KISS: Simple delegation to ConditionFactory.
"""
from typing import Dict, List, Any, Optional

from src.core.conditions.condition_factory import ConditionFactory
from src.core.conditions.condition_interface import ConditionInterface, ConditionResult


class ConditionAdapter:
    """Adapter for condition operations to provide the interface expected by the UI."""
    
    def __init__(self, condition_factory: ConditionFactory):
        """
        Initialize the adapter with a ConditionFactory instance.
        
        Args:
            condition_factory: Factory for creating and managing conditions
        """
        self.condition_factory = condition_factory
    
    def get_condition_types(self) -> List[Dict[str, Any]]:
        """
        Get all registered condition types.
        
        Returns:
            List of condition types with metadata
        """
        condition_types = self.condition_factory.get_registered_condition_types()
        
        # Create metadata for each condition type
        result = []
        for condition_type in condition_types:
            # Add metadata based on condition type
            if condition_type == "comparison":
                result.append({
                    "type": condition_type,
                    "name": "Comparison",
                    "description": "Compare two values",
                    "category": "Basic",
                    "parameters": [
                        {"name": "left_value", "type": "string", "description": "Left value or variable name"},
                        {"name": "operator", "type": "enum", "description": "Comparison operator", 
                         "options": ["EQUAL", "NOT_EQUAL", "GREATER_THAN", "GREATER_THAN_OR_EQUAL", 
                                    "LESS_THAN", "LESS_THAN_OR_EQUAL", "CONTAINS", "NOT_CONTAINS", 
                                    "STARTS_WITH", "ENDS_WITH", "MATCHES_REGEX"]},
                        {"name": "right_value", "type": "string", "description": "Right value or variable name"}
                    ]
                })
            elif condition_type == "element_exists":
                result.append({
                    "type": condition_type,
                    "name": "Element Exists",
                    "description": "Check if an element exists in the DOM",
                    "category": "Web",
                    "parameters": [
                        {"name": "selector", "type": "string", "description": "CSS selector for the element"}
                    ]
                })
            elif condition_type == "text_contains":
                result.append({
                    "type": condition_type,
                    "name": "Text Contains",
                    "description": "Check if an element's text contains a specific string",
                    "category": "Web",
                    "parameters": [
                        {"name": "selector", "type": "string", "description": "CSS selector for the element"},
                        {"name": "text", "type": "string", "description": "Text to check for"},
                        {"name": "case_sensitive", "type": "boolean", "description": "Whether the comparison should be case-sensitive"}
                    ]
                })
            elif condition_type == "and":
                result.append({
                    "type": condition_type,
                    "name": "AND",
                    "description": "Combine multiple conditions with AND logic",
                    "category": "Composite",
                    "parameters": [
                        {"name": "conditions", "type": "array", "description": "List of conditions to combine"}
                    ]
                })
            elif condition_type == "or":
                result.append({
                    "type": condition_type,
                    "name": "OR",
                    "description": "Combine multiple conditions with OR logic",
                    "category": "Composite",
                    "parameters": [
                        {"name": "conditions", "type": "array", "description": "List of conditions to combine"}
                    ]
                })
            elif condition_type == "not":
                result.append({
                    "type": condition_type,
                    "name": "NOT",
                    "description": "Negate a condition",
                    "category": "Composite",
                    "parameters": [
                        {"name": "condition", "type": "object", "description": "Condition to negate"}
                    ]
                })
            else:
                # Generic metadata for unknown condition types
                result.append({
                    "type": condition_type,
                    "name": condition_type.replace("_", " ").title(),
                    "description": f"{condition_type} condition",
                    "category": "Other",
                    "parameters": []
                })
        
        return result
    
    def create_condition(self, condition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a condition from the given data.
        
        Args:
            condition_data: Dictionary containing condition configuration
            
        Returns:
            Dictionary containing the created condition data
        """
        # Create the condition using the factory
        condition = self.condition_factory.create_condition(condition_data)
        
        # Convert the condition to a dictionary
        result = {
            "id": condition.id,
            "description": condition.description,
            "type": condition.type
        }
        
        # Add condition-specific data
        if hasattr(condition, "to_dict"):
            result.update(condition.to_dict())
        
        return result
    
    def get_condition_by_id(self, condition_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a condition by ID.
        
        Args:
            condition_id: ID of the condition to get
            
        Returns:
            Dictionary containing the condition data, or None if not found
        """
        # Get the condition from the factory
        condition = self.condition_factory.get_condition_by_id(condition_id)
        
        if not condition:
            return None
        
        # Convert the condition to a dictionary
        if hasattr(condition, "to_dict"):
            return condition.to_dict()
        
        # Fallback for conditions without to_dict method
        return {
            "id": condition.id,
            "description": condition.description,
            "type": condition.type
        }
    
    def update_condition(self, condition_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a condition.
        
        Args:
            condition_data: Dictionary containing updated condition configuration
            
        Returns:
            Dictionary containing the updated condition data
        """
        # Update the condition using the factory
        condition = self.condition_factory.update_condition(condition_data)
        
        # Convert the condition to a dictionary
        if hasattr(condition, "to_dict"):
            return condition.to_dict()
        
        # Fallback for conditions without to_dict method
        return {
            "id": condition.id,
            "description": condition.description,
            "type": condition.type
        }
    
    def delete_condition(self, condition_id: str) -> bool:
        """
        Delete a condition.
        
        Args:
            condition_id: ID of the condition to delete
            
        Returns:
            True if the condition was deleted, False otherwise
        """
        return self.condition_factory.delete_condition(condition_id)
    
    def evaluate_condition(self, condition_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a condition with the given context.
        
        Args:
            condition_id: ID of the condition to evaluate
            context: Execution context containing variables, browser, etc.
            
        Returns:
            Dictionary containing the evaluation result
        """
        # Get the condition from the factory
        condition = self.condition_factory.get_condition_by_id(condition_id)
        
        if not condition:
            return {
                "success": False,
                "value": False,
                "message": f"Condition not found: {condition_id}"
            }
        
        # Evaluate the condition
        result = condition.evaluate(context)
        
        # Convert the result to a dictionary
        return {
            "success": result.success,
            "value": result.value,
            "message": result.message
        }
