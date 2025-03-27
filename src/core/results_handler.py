"""Results handler for processing and reporting automation results"""
import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from src.core.interfaces import ReporterInterface


class ResultsHandler(ReporterInterface):
    """Handles processing and reporting of automation results"""

    def __init__(self) -> None:
        """Initialize the results handler"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.results_dir: Optional[Path] = None
        self.screenshots_dir: Optional[Path] = None
        self.report_format: str = "json"
        self.results: List[Dict[str, Any]] = []

    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the reporter with configuration

        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing results handler")
        self.config = config
        self.results_dir = Path(config.get("results_dir", "results"))
        self.report_format = config.get("report_format", "json")

        # Set up screenshots directory
        screenshots_dir = config.get("screenshots_dir")
        if screenshots_dir:
            self.screenshots_dir = Path(screenshots_dir)
        else:
            self.screenshots_dir = self.results_dir / "screenshots"

        self._ensure_dirs_exist()

    def _ensure_dirs_exist(self) -> None:
        """Ensure the required directories exist"""
        if self.results_dir:
            self.results_dir.mkdir(parents=True, exist_ok=True)

        if self.screenshots_dir:
            self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    def report(self, results: Dict[str, Any]) -> None:
        """
        Generate a report from results

        Args:
            results: Dictionary containing the results to report
        """
        self.logger.info("Generating report")

        # Store the results
        self.results = results.get("results", [])

        # Generate a report file
        if self.report_format == "json":
            self._generate_json_report(results)
        else:
            self.logger.warning(f"Unsupported report format: {self.report_format}")

    def add_screenshot(self, screenshot_path: Union[str, Path], result_index: Optional[int] = None) -> bool:
        """
        Add a screenshot to a result

        Args:
            screenshot_path: Path to the screenshot file
            result_index: Index of the result to add the screenshot to (None for the latest)

        Returns:
            True if successful, False otherwise
        """
        if not self.results:
            self.logger.error("No results to add screenshot to")
            return False

        if not self.screenshots_dir:
            self.logger.error("Screenshots directory not set")
            return False

        # Convert to Path object
        screenshot_path = Path(screenshot_path)

        if not screenshot_path.exists():
            self.logger.error(f"Screenshot file not found: {screenshot_path}")
            return False

        try:
            # Determine the result to add the screenshot to
            if result_index is None:
                result_index = len(self.results) - 1

            if result_index < 0 or result_index >= len(self.results):
                self.logger.error(f"Invalid result index: {result_index}")
                return False

            result = self.results[result_index]

            # Generate a unique filename for the screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            script_name = Path(result.get("script", "unknown")).stem
            screenshot_filename = f"{script_name}_{timestamp}.png"

            # Copy the screenshot to the screenshots directory
            target_path = self.screenshots_dir / screenshot_filename
            shutil.copy2(screenshot_path, target_path)

            # Add the screenshot to the result
            if "screenshots" not in result:
                result["screenshots"] = []

            result["screenshots"].append({
                "path": str(target_path),
                "timestamp": datetime.now().isoformat(),
                "filename": screenshot_filename,
            })

            self.logger.info(f"Added screenshot to result {result_index}: {target_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding screenshot: {str(e)}")
            return False

    def _generate_json_report(self, results: Dict[str, Any]) -> None:
        """
        Generate a JSON report

        Args:
            results: Dictionary containing the results to report
        """
        if not self.results_dir:
            self.logger.error("Results directory not set")
            return

        # Add timestamp to the results
        report_data = results.copy()
        report_data["timestamp"] = datetime.now().isoformat()
        report_data["summary"] = self.get_summary()

        # Add screenshots directory to the report
        if self.screenshots_dir:
            report_data["screenshots_dir"] = str(self.screenshots_dir)

        # Write the report to a file
        report_file = self.results_dir / "report.json"
        with open(report_file, "w") as f:
            json.dump(report_data, f, indent=2)

        self.logger.info(f"Report generated: {report_file}")

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all reports

        Returns:
            Dictionary containing the summary
        """
        self.logger.info("Generating summary")

        # Count results by status
        status_counts: Dict[str, int] = {}
        for result in self.results:
            status = result.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1

        # Calculate success rate
        total = len(self.results)
        success = status_counts.get("success", 0)
        success_rate = (success / total) * 100 if total > 0 else 0

        return {
            "total": total,
            "success": success,
            "success_rate": success_rate,
            **status_counts,
        }
