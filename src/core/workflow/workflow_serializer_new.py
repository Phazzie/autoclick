"""
Workflow serializer implementation.

This module provides an implementation of the workflow serializer,
for serializing and deserializing workflows.
"""
from typing import Dict, Any, List, Optional
import json
import uuid
import datetime

from .service_interfaces import IWorkflowSerializer
from .interfaces import IWorkflow, IWorkflowStep, IWorkflowEngine
from .service_exceptions import WorkflowSerializationError, WorkflowDeserializationError


class WorkflowSerializer(IWorkflowSerializer):
    """
    Implementation of a workflow serializer.
    
    This class provides an implementation of the IWorkflowSerializer interface,
    for serializing and deserializing workflows.
    """
    
    def __init__(self, workflow_engine: IWorkflowEngine):
        """
        Initialize a workflow serializer.
        
        Args:
            workflow_engine: Workflow engine to use for creating workflows and steps
        """
        self._workflow_engine = workflow_engine
    
    def serialize_workflow(self, workflow: IWorkflow) -> Dict[str, Any]:
        """
        Serialize a workflow to a dictionary.
        
        Args:
            workflow: Workflow to serialize
            
        Returns:
            Serialized workflow
            
        Raises:
            WorkflowSerializationError: If there is an error serializing the workflow
        """
        try:
            # Get the steps
            steps = workflow.get_steps()
            
            # Serialize the steps
            serialized_steps = [self.serialize_step(step) for step in steps]
            
            # Serialize the workflow
            return {
                "workflow_id": workflow.workflow_id,
                "name": workflow.name,
                "description": workflow.description,
                "version": workflow.version,
                "enabled": workflow.enabled,
                "steps": serialized_steps,
                "metadata": getattr(workflow, "metadata", {}),
                "created_at": getattr(workflow, "created_at", datetime.datetime.now().isoformat()),
                "updated_at": getattr(workflow, "updated_at", datetime.datetime.now().isoformat())
            }
        except Exception as e:
            raise WorkflowSerializationError(workflow.workflow_id, str(e), e)
    
    def deserialize_workflow(self, data: Dict[str, Any]) -> IWorkflow:
        """
        Deserialize a workflow from a dictionary.
        
        Args:
            data: Serialized workflow
            
        Returns:
            Deserialized workflow
            
        Raises:
            WorkflowDeserializationError: If there is an error deserializing the workflow
        """
        try:
            # Create the workflow
            workflow = self._workflow_engine.create_workflow({
                "workflow_id": data.get("workflow_id", str(uuid.uuid4())),
                "name": data.get("name", "Unnamed Workflow"),
                "description": data.get("description"),
                "version": data.get("version", "1.0.0"),
                "enabled": data.get("enabled", True),
                "metadata": data.get("metadata", {})
            })
            
            # Set the timestamps if available
            if "created_at" in data:
                setattr(workflow, "created_at", data["created_at"])
            if "updated_at" in data:
                setattr(workflow, "updated_at", data["updated_at"])
            
            # Deserialize the steps
            for step_data in data.get("steps", []):
                step = self.deserialize_step(step_data)
                workflow.add_step(step)
            
            return workflow
        except Exception as e:
            raise WorkflowDeserializationError(str(e), e)
    
    def serialize_step(self, step: IWorkflowStep) -> Dict[str, Any]:
        """
        Serialize a workflow step to a dictionary.
        
        Args:
            step: Workflow step to serialize
            
        Returns:
            Serialized workflow step
            
        Raises:
            WorkflowSerializationError: If there is an error serializing the step
        """
        try:
            return {
                "step_id": step.step_id,
                "step_type": step.step_type,
                "name": step.name,
                "description": step.description,
                "enabled": step.enabled,
                "config": getattr(step, "config", {}),
                "metadata": getattr(step, "metadata", {})
            }
        except Exception as e:
            raise WorkflowSerializationError(step.step_id, str(e), e)
    
    def deserialize_step(self, data: Dict[str, Any]) -> IWorkflowStep:
        """
        Deserialize a workflow step from a dictionary.
        
        Args:
            data: Serialized workflow step
            
        Returns:
            Deserialized workflow step
            
        Raises:
            WorkflowDeserializationError: If there is an error deserializing the step
        """
        try:
            # Create the step
            return self._workflow_engine.create_step({
                "step_id": data.get("step_id", str(uuid.uuid4())),
                "step_type": data.get("step_type", "unknown"),
                "name": data.get("name", "Unnamed Step"),
                "description": data.get("description"),
                "enabled": data.get("enabled", True),
                "config": data.get("config", {}),
                "metadata": data.get("metadata", {})
            })
        except Exception as e:
            raise WorkflowDeserializationError(str(e), e)
    
    def serialize_to_json(self, workflow: IWorkflow) -> str:
        """
        Serialize a workflow to a JSON string.
        
        Args:
            workflow: Workflow to serialize
            
        Returns:
            Serialized workflow as a JSON string
            
        Raises:
            WorkflowSerializationError: If there is an error serializing the workflow
        """
        try:
            # Serialize the workflow to a dictionary
            data = self.serialize_workflow(workflow)
            
            # Convert to JSON
            return json.dumps(data, indent=2)
        except Exception as e:
            raise WorkflowSerializationError(workflow.workflow_id, str(e), e)
    
    def deserialize_from_json(self, json_str: str) -> IWorkflow:
        """
        Deserialize a workflow from a JSON string.
        
        Args:
            json_str: Serialized workflow as a JSON string
            
        Returns:
            Deserialized workflow
            
        Raises:
            WorkflowDeserializationError: If there is an error deserializing the workflow
        """
        try:
            # Parse the JSON
            data = json.loads(json_str)
            
            # Deserialize the workflow
            return self.deserialize_workflow(data)
        except Exception as e:
            raise WorkflowDeserializationError(str(e), e)
