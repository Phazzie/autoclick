"""Automation engine for web automation"""
import importlib.util
import logging
import sys
from pathlib import Path
from typing import Any, Dict, Optional, Union

from src.core.interfaces import AutomationInterface
from src.core.webdriver_manager import WebDriverManager


class AutomationEngine(AutomationInterface):
    """Core automation engine for executing web automation scripts"""

    def __init__(self) -> None:
        """Initialize the automation engine"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.driver = None
        self.driver_manager: Optional[WebDriverManager] = None

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the automation engine with configuration

        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing automation engine")
        self.config = config
        self.driver_manager = WebDriverManager(config)

    def execute(self, script_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Execute an automation script and return results

        Args:
            script_path: Path to the script to execute

        Returns:
            Dictionary containing the results of the script execution

        Raises:
            FileNotFoundError: If the script file does not exist
            ImportError: If the script cannot be imported
            RuntimeError: If the script execution fails
        """
        self.logger.info(f"Executing script: {script_path}")
        script_path = Path(script_path)

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        try:
            # Initialize the WebDriver
            if self.driver_manager:
                self.driver = self.driver_manager.initialize_driver()
            else:
                raise RuntimeError("Driver manager not initialized")

            # Load the script module
            module_name = script_path.stem
            spec = importlib.util.spec_from_file_location(module_name, script_path)
            if spec is None or spec.loader is None:
                raise ImportError(f"Could not load script: {script_path}")

            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            # Execute the script
            if not hasattr(module, "run"):
                raise AttributeError(f"Script {script_path} does not have a run function")

            result = module.run(self.driver)
            return result if isinstance(result, dict) else {"result": result}

        except Exception as e:
            self.logger.error(f"Error executing script: {str(e)}")
            return {"status": "error", "message": str(e)}
        finally:
            # Clean up resources
            self.cleanup()

    def cleanup(self) -> None:
        """Clean up resources"""
        self.logger.info("Cleaning up resources")
        if self.driver_manager:
            self.driver_manager.close()
            self.driver = None
