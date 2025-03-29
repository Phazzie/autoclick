"""Visualization helpers for workflow state"""
import json
from typing import Dict, Any, List, Optional, Union
from datetime import datetime

from src.core.context.execution_context import ExecutionContext
from src.core.context.execution_state import ExecutionStateEnum


class StateVisualizer:
    """
    Provides visualization helpers for workflow state
    
    This class generates human-readable representations of workflow state
    for debugging, logging, and UI display.
    """
    
    @staticmethod
    def get_state_summary(context: ExecutionContext) -> Dict[str, Any]:
        """
        Get a summary of the current execution state
        
        Args:
            context: Execution context
            
        Returns:
            Dictionary with state summary information
        """
        return {
            "context_id": context.id,
            "state": context.state.current_state.name,
            "variable_count": {
                "global": len(context.variables._variables[1]),  # GLOBAL scope
                "workflow": len(context.variables._variables[2]),  # WORKFLOW scope
                "local": len(context.variables._variables[3])  # LOCAL scope
            },
            "state_history_count": len(context.state.state_history),
            "has_parent": context.parent is not None,
            "child_count": len(context._children)
        }
    
    @staticmethod
    def get_state_history(context: ExecutionContext) -> List[Dict[str, Any]]:
        """
        Get the state transition history
        
        Args:
            context: Execution context
            
        Returns:
            List of state transition events
        """
        return [
            {
                "old_state": event.old_state.name,
                "new_state": event.new_state.name,
                "timestamp": event.timestamp.isoformat()
            }
            for event in context.state.state_history
        ]
    
    @staticmethod
    def get_variable_snapshot(
        context: ExecutionContext, 
        include_global: bool = True,
        include_workflow: bool = True,
        include_local: bool = True
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get a snapshot of all variables
        
        Args:
            context: Execution context
            include_global: Whether to include global variables
            include_workflow: Whether to include workflow variables
            include_local: Whether to include local variables
            
        Returns:
            Dictionary of variables by scope
        """
        from src.core.context.variable_storage import VariableScope
        
        result = {}
        
        if include_global:
            result["global"] = {
                name: StateVisualizer._format_value(value)
                for name, value in context.variables._variables[VariableScope.GLOBAL].items()
            }
        
        if include_workflow:
            result["workflow"] = {
                name: StateVisualizer._format_value(value)
                for name, value in context.variables._variables[VariableScope.WORKFLOW].items()
            }
        
        if include_local:
            result["local"] = {
                name: StateVisualizer._format_value(value)
                for name, value in context.variables._variables[VariableScope.LOCAL].items()
            }
        
        return result
    
    @staticmethod
    def get_state_diagram(context: ExecutionContext) -> Dict[str, Any]:
        """
        Get a diagram representation of the state machine
        
        Args:
            context: Execution context
            
        Returns:
            Dictionary with state diagram information
        """
        from src.core.context.execution_state import VALID_TRANSITIONS
        
        # Get the current state
        current_state = context.state.current_state
        
        # Create nodes for all states
        nodes = []
        for state in ExecutionStateEnum:
            nodes.append({
                "id": state.name,
                "label": state.name,
                "active": state == current_state
            })
        
        # Create edges for valid transitions
        edges = []
        for from_state, to_states in VALID_TRANSITIONS.items():
            for to_state in to_states:
                edges.append({
                    "from": from_state.name,
                    "to": to_state.name,
                    "active": from_state == current_state
                })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "current_state": current_state.name
        }
    
    @staticmethod
    def get_context_hierarchy(context: ExecutionContext) -> Dict[str, Any]:
        """
        Get a hierarchical representation of the context and its children
        
        Args:
            context: Execution context
            
        Returns:
            Dictionary with context hierarchy information
        """
        result = {
            "id": context.id,
            "state": context.state.current_state.name,
            "variable_count": sum(len(vars) for vars in context.variables._variables.values()),
            "children": []
        }
        
        # Add children recursively
        for child in context._children:
            result["children"].append(StateVisualizer.get_context_hierarchy(child))
        
        return result
    
    @staticmethod
    def to_json(data: Any, indent: int = 2) -> str:
        """
        Convert data to a JSON string
        
        Args:
            data: Data to convert
            indent: Indentation level
            
        Returns:
            JSON string representation
        """
        return json.dumps(data, indent=indent)
    
    @staticmethod
    def _format_value(value: Any) -> Union[str, int, float, bool, List, Dict, None]:
        """
        Format a value for display
        
        Args:
            value: Value to format
            
        Returns:
            Formatted value
        """
        if value is None:
            return None
        elif isinstance(value, (str, int, float, bool)):
            return value
        elif isinstance(value, (list, tuple)):
            return [StateVisualizer._format_value(item) for item in value]
        elif isinstance(value, dict):
            return {
                str(k): StateVisualizer._format_value(v)
                for k, v in value.items()
            }
        elif isinstance(value, datetime):
            return value.isoformat()
        else:
            # For complex objects, just return their string representation
            return str(value)
