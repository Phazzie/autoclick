"""
Workflow Adapter Module

This module provides adapter functions to convert between the frontend workflow format
and the backend workflow model format.
"""

from typing import Dict, List, Any, Optional
from src.models.workflow import Workflow


def frontend_to_backend_workflow(frontend_data: Dict[str, Any]) -> Workflow:
    """
    Convert a frontend workflow representation to a backend Workflow object.
    
    Args:
        frontend_data: Dictionary containing workflow data from the frontend
        
    Returns:
        Workflow: A backend Workflow object
    """
    workflow = Workflow(
        id=frontend_data.get('id', ''),
        name=frontend_data.get('name', 'New Workflow')
    )
    
    # Convert steps
    if 'steps' in frontend_data:
        workflow.steps = [frontend_to_backend_step(step) for step in frontend_data['steps']]
    
    return workflow


def frontend_to_backend_step(frontend_step: Dict[str, Any]) -> Workflow.Step:
    """
    Convert a frontend step representation to a backend Step object.
    
    Args:
        frontend_step: Dictionary containing step data from the frontend
        
    Returns:
        Workflow.Step: A backend Step object
    """
    step_type = frontend_step.get('type', 'unknown')
    
    # Map frontend step types to backend step types if needed
    step_type_mapping = {
        'navigate': 'navigate',
        'click': 'click',
        'input': 'input',
        'wait': 'wait',
        'screenshot': 'screenshot',
        'condition': 'condition',
        'loop': 'loop'
    }
    
    backend_type = step_type_mapping.get(step_type, step_type)
    
    # Create the step with basic properties
    step = Workflow.Step(
        id=frontend_step.get('id', ''),
        type=backend_type,
        name=frontend_step.get('name', ''),
        description=frontend_step.get('description', '')
    )
    
    # Add type-specific properties
    if 'target' in frontend_step:
        step.target = frontend_step['target']
    
    if 'value' in frontend_step:
        step.value = frontend_step['value']
    
    # Handle any additional properties based on step type
    if backend_type == 'condition':
        if 'condition' in frontend_step:
            step.condition = frontend_step['condition']
    
    if backend_type == 'loop':
        if 'iterations' in frontend_step:
            step.iterations = frontend_step['iterations']
    
    return step


def backend_to_frontend_workflow(workflow: Workflow) -> Dict[str, Any]:
    """
    Convert a backend Workflow object to a frontend workflow representation.
    
    Args:
        workflow: Backend Workflow object
        
    Returns:
        Dict: A dictionary representation for the frontend
    """
    result = {
        'id': workflow.id,
        'name': workflow.name,
        'steps': [backend_to_frontend_step(step) for step in workflow.steps]
    }
    
    return result


def backend_to_frontend_step(step: Workflow.Step) -> Dict[str, Any]:
    """
    Convert a backend Step object to a frontend step representation.
    
    Args:
        step: Backend Step object
        
    Returns:
        Dict: A dictionary representation for the frontend
    """
    # Create the base step dictionary
    frontend_step = {
        'id': step.id,
        'type': step.type,
        'name': step.name,
        'description': step.description
    }
    
    # Add type-specific properties
    if hasattr(step, 'target') and step.target:
        frontend_step['target'] = step.target
    
    if hasattr(step, 'value') and step.value:
        frontend_step['value'] = step.value
    
    # Handle specific step types
    if step.type == 'condition' and hasattr(step, 'condition'):
        frontend_step['condition'] = step.condition
    
    if step.type == 'loop' and hasattr(step, 'iterations'):
        frontend_step['iterations'] = step.iterations
    
    return frontend_step
