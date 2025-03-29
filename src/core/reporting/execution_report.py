"""
Execution report for workflow execution details.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.core.reporting.base_report import BaseReport


class ExecutionReport(BaseReport):
    """
    Report for workflow execution details.
    
    This report provides detailed information about a workflow execution,
    including action execution times, success/failure status, and performance metrics.
    """
    
    def __init__(
        self,
        title: str = "Workflow Execution Report",
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize the execution report.
        
        Args:
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
        """
        super().__init__(
            report_type="execution",
            title=title,
            description=description,
            tags=tags
        )
        self.data = {
            "workflow": {},
            "actions": [],
            "performance": {
                "total_duration_ms": 0,
                "average_action_duration_ms": 0,
                "slowest_action": None,
                "fastest_action": None
            },
            "summary": {
                "total_actions": 0,
                "successful_actions": 0,
                "failed_actions": 0,
                "success_rate": 0
            },
            "errors": []
        }
    
    def collect_data(self, source: Any) -> None:
        """
        Collect data from workflow execution.
        
        Args:
            source: The workflow execution data source
        """
        super().collect_data(source)
        
        # Extract workflow information
        if hasattr(source, "id"):
            self.data["workflow"]["id"] = source.id
        
        if hasattr(source, "status"):
            self.data["workflow"]["status"] = str(source.status)
        
        # Extract action results
        if hasattr(source, "results"):
            self._process_action_results(source.results)
        
        # Extract statistics if available
        if hasattr(source, "statistics"):
            self._process_statistics(source.statistics)
    
    def _process_action_results(self, results: List[Dict[str, Any]]) -> None:
        """
        Process action results from workflow execution.
        
        Args:
            results: List of action execution results
        """
        self.data["actions"] = []
        successful_actions = 0
        failed_actions = 0
        
        for result in results:
            action_data = {
                "id": result.get("action_id", "unknown"),
                "type": result.get("action_type", "unknown"),
                "description": result.get("description", ""),
                "success": result.get("success", False),
                "message": result.get("message", ""),
                "execution_time_ms": result.get("execution_time_ms", 0),
                "timestamp": result.get("timestamp", datetime.now().isoformat())
            }
            
            self.data["actions"].append(action_data)
            
            if action_data["success"]:
                successful_actions += 1
            else:
                failed_actions += 1
                # Add to errors list if failed
                self.data["errors"].append({
                    "action_id": action_data["id"],
                    "action_type": action_data["type"],
                    "message": action_data["message"],
                    "timestamp": action_data["timestamp"]
                })
        
        # Update summary
        total_actions = len(results)
        self.data["summary"]["total_actions"] = total_actions
        self.data["summary"]["successful_actions"] = successful_actions
        self.data["summary"]["failed_actions"] = failed_actions
        
        if total_actions > 0:
            self.data["summary"]["success_rate"] = (successful_actions / total_actions) * 100
    
    def _process_statistics(self, statistics: Any) -> None:
        """
        Process performance statistics from workflow execution.
        
        Args:
            statistics: Workflow statistics object
        """
        # Extract total duration
        if hasattr(statistics, "total_duration_ms"):
            self.data["performance"]["total_duration_ms"] = statistics.total_duration_ms
        
        # Extract action durations
        if hasattr(statistics, "action_durations") and statistics.action_durations:
            durations = statistics.action_durations
            
            # Calculate average duration
            if durations:
                avg_duration = sum(durations.values()) / len(durations)
                self.data["performance"]["average_action_duration_ms"] = avg_duration
            
            # Find slowest and fastest actions
            if durations:
                slowest_action_id = max(durations, key=durations.get)
                fastest_action_id = min(durations, key=durations.get)
                
                self.data["performance"]["slowest_action"] = {
                    "action_id": slowest_action_id,
                    "duration_ms": durations[slowest_action_id]
                }
                
                self.data["performance"]["fastest_action"] = {
                    "action_id": fastest_action_id,
                    "duration_ms": durations[fastest_action_id]
                }
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate the execution report.
        
        Returns:
            A dictionary containing the execution report data
        """
        # Update metadata before generating
        self.metadata.update()
        
        # Generate base report
        report = super().generate()
        
        # Add execution-specific sections
        if self.data["errors"]:
            report["has_errors"] = True
            report["error_count"] = len(self.data["errors"])
        else:
            report["has_errors"] = False
            report["error_count"] = 0
        
        return report
