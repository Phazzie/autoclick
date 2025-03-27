"""Results handler for processing and reporting automation results"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.core.interfaces import ReporterInterface


class ResultsHandler(ReporterInterface):
    """Handles processing and reporting of automation results"""

    def __init__(self) -> None:
        """Initialize the results handler"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.results_dir: Optional[Path] = None
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
        self._ensure_results_dir_exists()

    def _ensure_results_dir_exists(self) -> None:
        """Ensure the results directory exists"""
        if self.results_dir:
            self.results_dir.mkdir(parents=True, exist_ok=True)

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
