"""Action for capturing screenshots"""
from typing import Dict, Any, Optional, Tuple

from src.core.actions.base_action import BaseAction
from src.core.actions.action_interface import ActionResult
from src.core.actions.action_factory import ActionFactory
from src.core.utils.screenshot_manager import ScreenshotManager
from src.core.utils.screenshot_capture import CaptureMode


@ActionFactory.register("screenshot")
class ScreenshotAction(BaseAction):
    """Action that captures a screenshot"""

    def __init__(
        self,
        description: str,
        name: str,
        mode: str = "full_screen",
        selector: Optional[str] = None,
        region: Optional[Tuple[int, int, int, int]] = None,
        screenshot_dir: Optional[str] = None,
        action_id: Optional[str] = None
    ):
        """
        Initialize the screenshot action

        Args:
            description: Human-readable description of the action
            name: Base name for the screenshot
            mode: Capture mode ("full_screen", "element", or "region")
            selector: CSS selector for the element to capture (required for "element" mode)
            region: Region to capture as (x, y, width, height) (required for "region" mode)
            screenshot_dir: Directory to store screenshots (uses default if not provided)
            action_id: Optional unique identifier (generated if not provided)

        Raises:
            ValueError: If required parameters are missing for the selected mode
        """
        super().__init__(description, action_id)
        self.name = name
        self.mode_str = mode.lower()
        self.selector = selector
        self.region = region
        self.screenshot_dir = screenshot_dir

        # Validate parameters based on mode
        self._validate_parameters()

    def _validate_parameters(self) -> None:
        """Validate the action parameters"""
        if self.mode_str == "element" and not self.selector:
            raise ValueError("Selector is required for 'element' capture mode")

        if self.mode_str == "region" and not self.region:
            raise ValueError("Region is required for 'region' capture mode")

    @property
    def type(self) -> str:
        """Get the action type"""
        return "screenshot"

    def _execute(self, context: Dict[str, Any]) -> ActionResult:
        """
        Execute the screenshot action

        Args:
            context: Execution context containing browser, etc.

        Returns:
            Result of the action execution
        """
        # Get the browser driver from the context
        driver = context.get("driver")
        if not driver:
            return ActionResult.create_failure("No browser driver in context")

        try:
            # Create the screenshot manager
            manager = ScreenshotManager(self.screenshot_dir)

            # Find the element if in element mode
            element = self._find_element(driver) if self.mode_str == "element" else None

            # Capture the screenshot
            screenshot_path = manager.capture_and_save(
                driver=driver,
                name=self.name,
                mode=self._get_capture_mode(),
                element=element,
                region=self.region,
                metadata=self._create_metadata()
            )

            return ActionResult.create_success(
                f"Screenshot captured: {screenshot_path}",
                {"screenshot_path": screenshot_path}
            )

        except Exception as e:
            return ActionResult.create_failure(f"Failed to capture screenshot: {str(e)}")

    def _find_element(self, driver: Any) -> Any:
        """Find an element using the selector"""
        element = driver.find_element_by_css_selector(self.selector)
        if not element:
            raise ValueError(f"Element not found: {self.selector}")
        return element

    def _get_capture_mode(self) -> CaptureMode:
        """Get the capture mode enum value"""
        if self.mode_str == "element":
            return CaptureMode.ELEMENT
        elif self.mode_str == "region":
            return CaptureMode.REGION
        else:
            return CaptureMode.FULL_SCREEN

    def _create_metadata(self) -> Dict[str, Any]:
        """Create metadata for the screenshot"""
        return {
            "action_id": self.id,
            "description": self.description,
            "mode": self.mode_str,
            "selector": self.selector,
            "region": self.region
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert the action to a dictionary"""
        data = super().to_dict()
        data.update({
            "name": self.name,
            "mode": self.mode_str,
            "selector": self.selector,
            "region": self.region,
            "screenshot_dir": self.screenshot_dir
        })
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScreenshotAction':
        """
        Create an action from a dictionary

        Args:
            data: Dictionary representation of the action

        Returns:
            Instantiated action
        """
        return cls(
            description=data.get("description", ""),
            name=data.get("name", "screenshot"),
            mode=data.get("mode", "full_screen"),
            selector=data.get("selector"),
            region=data.get("region"),
            screenshot_dir=data.get("screenshot_dir"),
            action_id=data.get("id")
        )
