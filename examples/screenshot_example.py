"""Example demonstrating screenshot functionality"""
import os
import sys
import time
from typing import Dict, Any, List

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.screenshot_action import ScreenshotAction
from src.core.utils.screenshot_manager import ScreenshotManager, CaptureMode
from src.core.workflow.workflow_engine import WorkflowEngine


# Create a simple action for the example
class NavigateAction(BaseAction):
    """Action that navigates to a URL"""

    def __init__(self, description: str, url: str, action_id: str = None):
        """Initialize the navigate action"""
        super().__init__(description, action_id)
        self.url = url

    @property
    def type(self) -> str:
        """Get the action type"""
        return "navigate"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        # Get the browser driver from the context
        driver = context.get("driver")
        if not driver:
            return ActionResult.create_failure("No browser driver in context")

        try:
            # Navigate to the URL
            driver.get(self.url)
            return ActionResult.create_success(f"Navigated to {self.url}")
        except Exception as e:
            return ActionResult.create_failure(f"Failed to navigate to {self.url}: {str(e)}")


# Create a simple action for the example
class WaitAction(BaseAction):
    """Action that waits for a specified time"""

    def __init__(self, description: str, seconds: float, action_id: str = None):
        """Initialize the wait action"""
        super().__init__(description, action_id)
        self.seconds = seconds

    @property
    def type(self) -> str:
        """Get the action type"""
        return "wait"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """Execute the action"""
        try:
            # Wait for the specified time
            time.sleep(self.seconds)
            return ActionResult.create_success(f"Waited for {self.seconds} seconds")
        except Exception as e:
            return ActionResult.create_failure(f"Failed to wait: {str(e)}")


def create_example_workflow(screenshot_dir: str) -> List[BaseAction]:
    """
    Create an example workflow that demonstrates screenshot functionality
    
    Args:
        screenshot_dir: Directory to store screenshots
        
    Returns:
        List of actions in the workflow
    """
    return [
        NavigateAction(
            description="Navigate to Google",
            url="https://www.google.com"
        ),
        WaitAction(
            description="Wait for page to load",
            seconds=1.0
        ),
        ScreenshotAction(
            description="Capture full screen",
            name="google_full_screen",
            mode="full_screen",
            screenshot_dir=screenshot_dir
        ),
        ScreenshotAction(
            description="Capture search box",
            name="google_search_box",
            mode="element",
            selector="input[name='q']",
            screenshot_dir=screenshot_dir
        ),
        ScreenshotAction(
            description="Capture region",
            name="google_region",
            mode="region",
            region=(100, 100, 300, 200),
            screenshot_dir=screenshot_dir
        ),
        NavigateAction(
            description="Navigate to GitHub",
            url="https://github.com"
        ),
        WaitAction(
            description="Wait for page to load",
            seconds=1.0
        ),
        ScreenshotAction(
            description="Capture GitHub homepage",
            name="github_homepage",
            mode="full_screen",
            screenshot_dir=screenshot_dir
        )
    ]


def main() -> None:
    """Main function"""
    # Import selenium
    try:
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("Selenium is required for this example.")
        print("Please install it using: pip install selenium webdriver-manager")
        return

    # Create a screenshot directory
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    print(f"Screenshots will be saved to: {screenshot_dir}")
    
    # Create a workflow
    workflow = create_example_workflow(screenshot_dir)
    
    # Create a workflow engine
    engine = WorkflowEngine()
    
    # Create a browser driver
    print("Creating browser driver...")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    
    try:
        # Create a context with the driver
        context = {"driver": driver}
        
        # Execute the workflow
        print("Executing workflow...")
        result = engine.execute_workflow(workflow, context)
        
        # Print the result
        print(f"Workflow result: {'Success' if result['success'] else 'Failure'}")
        print(f"Message: {result['message']}")
        
        # Get the screenshot manager
        screenshot_manager = ScreenshotManager(screenshot_dir)
        
        # Print information about the screenshots
        screenshots = screenshot_manager.get_screenshots()
        print(f"\nCaptured {len(screenshots)} screenshots:")
        for screenshot in screenshots:
            print(f"  - {os.path.basename(screenshot)}")
            
            # Get metadata if available
            metadata = screenshot_manager.get_metadata(screenshot)
            if metadata:
                print(f"    Mode: {metadata.get('mode', 'unknown')}")
                print(f"    Description: {metadata.get('description', 'unknown')}")
    
    finally:
        # Close the browser
        print("\nClosing browser...")
        driver.quit()


if __name__ == "__main__":
    main()
