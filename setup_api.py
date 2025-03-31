"""
Setup API Server

This script installs the required dependencies for the API server.
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install the required dependencies for the API server."""
    print("Installing required dependencies...")
    
    # List of required packages
    packages = [
        "flask",
        "flask-cors"
    ]
    
    # Install each package
    for package in packages:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
    print("All dependencies installed successfully!")

def create_default_workflow():
    """Create a default workflow if none exists."""
    from src.models.workflow import Workflow
    from src.services.workflow_service import WorkflowService
    
    workflow_service = WorkflowService()
    
    # Check if default workflow exists
    default_workflow = workflow_service.get_workflow_by_id("default")
    if default_workflow:
        print("Default workflow already exists.")
        return
    
    # Create default workflow
    print("Creating default workflow...")
    workflow = Workflow(id="default", name="Default Workflow")
    
    # Add some steps
    workflow.steps = [
        Workflow.Step(
            id="step1",
            type="navigate",
            name="Navigate to URL",
            target="https://example.com",
            description="Open the website homepage"
        ),
        Workflow.Step(
            id="step2",
            type="click",
            name="Click Login Button",
            target="button.login",
            description="Click on the login button"
        ),
        Workflow.Step(
            id="step3",
            type="input",
            name="Enter Username",
            target="input#username",
            value="user@example.com",
            description="Enter the username in the input field"
        )
    ]
    
    # Save the workflow
    workflow_service.create_workflow(workflow)
    print("Default workflow created successfully!")

if __name__ == "__main__":
    install_dependencies()
    
    # Add the current directory to the Python path
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        create_default_workflow()
    except Exception as e:
        print(f"Error creating default workflow: {str(e)}")
        print("This is expected if the workflow model or service is not yet implemented.")
        print("You can run this script again after implementing those components.")
    
    print("\nSetup complete! You can now run the API server with:")
    print("python api_server.py")
