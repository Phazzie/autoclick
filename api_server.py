from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).parent))

# Import required modules from your existing application
from src.models.workflow import Workflow
from src.models.workflow_adapter import frontend_to_backend_workflow, backend_to_frontend_workflow
from src.services.workflow_service import WorkflowService
from src.execution.execution_engine import ExecutionEngine

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize services
workflow_service = WorkflowService()
execution_engine = ExecutionEngine()

@app.route('/api/workflows', methods=['GET'])
def get_workflows():
    """Get all workflows"""
    try:
        workflows = workflow_service.get_all_workflows()
        return jsonify([backend_to_frontend_workflow(w) for w in workflows])
    except Exception as e:
        print(f"Error getting workflows: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    """Get a specific workflow by ID"""
    try:
        workflow = workflow_service.get_workflow_by_id(workflow_id)
        if workflow:
            return jsonify(backend_to_frontend_workflow(workflow))
        return jsonify({"error": "Workflow not found"}), 404
    except Exception as e:
        print(f"Error getting workflow {workflow_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows', methods=['POST'])
def create_workflow():
    """Create a new workflow"""
    try:
        data = request.json
        workflow = frontend_to_backend_workflow(data)
        created_workflow = workflow_service.create_workflow(workflow)
        return jsonify(backend_to_frontend_workflow(created_workflow)), 201
    except Exception as e:
        print(f"Error creating workflow: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    """Update an existing workflow"""
    try:
        data = request.json
        workflow = workflow_service.get_workflow_by_id(workflow_id)
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404

        # Update workflow properties
        if 'name' in data:
            workflow.name = data['name']
        if 'steps' in data:
            # Convert the steps from the frontend format to your backend format
            temp_workflow = frontend_to_backend_workflow(data)
            workflow.steps = temp_workflow.steps

        updated_workflow = workflow_service.update_workflow(workflow)
        return jsonify(backend_to_frontend_workflow(updated_workflow))
    except Exception as e:
        print(f"Error updating workflow {workflow_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    """Delete a workflow"""
    try:
        success = workflow_service.delete_workflow(workflow_id)
        if success:
            return jsonify({"status": "success"})
        return jsonify({"error": "Workflow not found"}), 404
    except Exception as e:
        print(f"Error deleting workflow {workflow_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/workflows/<workflow_id>/execute', methods=['POST'])
def execute_workflow(workflow_id):
    """Execute a workflow"""
    try:
        workflow = workflow_service.get_workflow_by_id(workflow_id)
        if not workflow:
            return jsonify({"error": "Workflow not found"}), 404

        # Execute the workflow
        result = execution_engine.execute_workflow(workflow)
        return jsonify({
            "status": "success",
            "message": f"Workflow executed successfully",
            "result": result
        })
    except Exception as e:
        print(f"Error executing workflow {workflow_id}: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Error executing workflow: {str(e)}"
        }), 500

@app.route('/api/workflow-types', methods=['GET'])
def get_workflow_step_types():
    """Get available workflow step types"""
    try:
        # This should return the available step types from your application
        # Replace with actual step types from your application
        step_types = [
            {"id": "navigate", "name": "Navigate to URL", "description": "Navigate to a specific URL"},
            {"id": "click", "name": "Click Element", "description": "Click on an element on the page"},
            {"id": "input", "name": "Enter Text", "description": "Enter text into an input field"},
            {"id": "wait", "name": "Wait", "description": "Wait for a specified amount of time"},
            {"id": "screenshot", "name": "Take Screenshot", "description": "Capture a screenshot of the page"},
            {"id": "condition", "name": "Condition", "description": "Conditional logic based on element state"},
            {"id": "loop", "name": "Loop", "description": "Repeat actions multiple times"}
        ]
        return jsonify(step_types)
    except Exception as e:
        print(f"Error getting workflow step types: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting API server on http://localhost:5000")
    app.run(debug=True, port=5000)
