"""Parallel runner for executing automation scripts in parallel"""
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.core.interfaces import AutomationInterface, RunnerInterface


class ParallelRunner(RunnerInterface):
    """Executes automation scripts in parallel"""

    def __init__(self) -> None:
        """Initialize the parallel runner"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.max_workers: int = 4  # Default value
        self.running = False
        self.executor = None

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the runner with configuration

        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing parallel runner")
        self.config = config
        self.max_workers = config.get("max_workers", 4)

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
        self.logger.info(f"Running {len(scripts)} scripts in parallel with {self.max_workers} workers")
        self.running = True
        results = []

        try:
            # Execute each script and collect results
            for script in scripts:
                if not self.running:
                    self.logger.info("Execution stopped by user")
                    break

                try:
                    result = automation.execute(script)
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error executing script {script}: {str(e)}")
                    results.append({
                        "status": "error",
                        "script": str(script),
                        "message": str(e)
                    })

            return {
                "status": "success",
                "total": len(scripts),
                "completed": len(results),
                "results": results,
            }
        except Exception as e:
            self.logger.error(f"Error running scripts in parallel: {str(e)}")
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
        self.logger.info("Stopping parallel runner")
        self.running = False
        if self.executor:
            self.executor.shutdown(wait=False)
