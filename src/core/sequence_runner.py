"""Sequence runner for executing automation scripts in sequence"""
import logging
from pathlib import Path
from typing import Any, Dict, List, Union

from src.core.interfaces import AutomationInterface, RunnerInterface


class SequenceRunner(RunnerInterface):
    """Executes automation scripts in sequence"""

    def __init__(self) -> None:
        """Initialize the sequence runner"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.running = False

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the runner with configuration

        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing sequence runner")
        self.config = config

    def run(
        self, automation: AutomationInterface, scripts: List[Union[str, Path]]
    ) -> Dict[str, Any]:
        """
        Run multiple scripts using the provided automation

        Args:
            automation: Automation interface to use for execution
            scripts: List of script paths to execute

        Returns:
            Dictionary containing the results of all script executions
        """
        self.logger.info(f"Running {len(scripts)} scripts in sequence")
        self.running = True
        results = []

        try:
            for i, script_path in enumerate(scripts):
                if not self.running:
                    self.logger.info("Execution stopped by user")
                    break

                self.logger.info(f"Executing script {i+1}/{len(scripts)}: {script_path}")
                result = automation.execute(script_path)
                results.append(result)

            return {
                "status": "success",
                "total": len(scripts),
                "completed": len(results),
                "results": results,
            }
        except Exception as e:
            self.logger.error(f"Error running scripts: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "total": len(scripts),
                "completed": len(results),
                "results": results,
            }
        finally:
            self.running = False

    def stop(self) -> None:
        """Stop all running executions"""
        self.logger.info("Stopping sequence runner")
        self.running = False
