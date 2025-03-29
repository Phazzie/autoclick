"""
Performance report for analyzing system performance.
"""
from typing import Any, Dict, List, Optional
from datetime import datetime

from src.core.reporting.base_report import BaseReport
from src.core.analytics.metric import Metric, MetricType
from src.core.analytics.analyzers.performance_analyzer import PerformanceAnalyzer


class PerformanceReport(BaseReport):
    """
    Report for system performance analysis.
    
    This report provides detailed information about system performance,
    including execution times, resource usage, and bottleneck identification.
    """
    
    def __init__(
        self,
        title: str = "Performance Analysis Report",
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize the performance report.
        
        Args:
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
        """
        super().__init__(
            report_type="performance",
            title=title,
            description=description,
            tags=tags
        )
        self.data = {
            "metrics": [],
            "analysis": {},
            "bottlenecks": [],
            "recommendations": [],
            "summary": {
                "total_operations": 0,
                "total_duration_ms": 0,
                "average_duration_ms": 0,
                "slowest_operation": None,
                "fastest_operation": None
            }
        }
        self.analyzer = PerformanceAnalyzer()
        
    def collect_data(self, metrics: List[Metric]) -> None:
        """
        Collect performance data from metrics.
        
        Args:
            metrics: List of metrics to analyze
        """
        self.source = metrics
        self.data["collection_time"] = datetime.now().isoformat()
        
        # Store metrics
        self.data["metrics"] = [metric.to_dict() for metric in metrics]
        
        # Analyze metrics
        self._analyze_metrics(metrics)
        
    def _analyze_metrics(self, metrics: List[Metric]) -> None:
        """
        Analyze metrics using the performance analyzer.
        
        Args:
            metrics: List of metrics to analyze
        """
        # Filter performance-related metrics
        performance_metrics = [
            m for m in metrics if m.metric_type in (
                MetricType.DURATION,
                MetricType.LATENCY,
                MetricType.RESPONSE_TIME,
                MetricType.CPU_USAGE,
                MetricType.MEMORY_USAGE,
                MetricType.DISK_USAGE
            )
        ]
        
        # Skip analysis if no performance metrics
        if not performance_metrics:
            self.logger.warning("No performance metrics found for analysis")
            return
            
        # Analyze metrics
        analysis_results = self.analyzer.analyze(performance_metrics)
        
        # Store analysis results
        self.data["analysis"] = analysis_results
        
        # Extract bottlenecks and recommendations
        self.data["bottlenecks"] = analysis_results.get("bottlenecks", [])
        self.data["recommendations"] = analysis_results.get("recommendations", [])
        
        # Update summary
        summary = analysis_results.get("summary", {})
        self.data["summary"] = {
            "total_operations": summary.get("operation_count", 0),
            "total_duration_ms": summary.get("total_duration", 0),
            "average_duration_ms": summary.get("avg_duration", 0),
            "slowest_operation": summary.get("slowest_operation", None),
            "fastest_operation": summary.get("fastest_operation", None),
            "bottleneck_count": summary.get("bottleneck_count", 0)
        }
        
    def get_bottlenecks(self) -> List[Dict[str, Any]]:
        """
        Get identified bottlenecks.
        
        Returns:
            List of bottlenecks with their details
        """
        return self.data["bottlenecks"]
        
    def get_recommendations(self) -> List[Dict[str, Any]]:
        """
        Get performance improvement recommendations.
        
        Returns:
            List of recommendations
        """
        return self.data["recommendations"]
        
    def get_operation_details(self, operation_name: str) -> Optional[Dict[str, Any]]:
        """
        Get details for a specific operation.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            Operation details or None if not found
        """
        operations = self.data["analysis"].get("operations", {})
        return operations.get(operation_name)
        
    def get_slowest_operations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Get the slowest operations.
        
        Args:
            limit: Maximum number of operations to return
            
        Returns:
            List of slowest operations with their details
        """
        operations = self.data["analysis"].get("operations", {})
        
        # Filter operations with duration data
        duration_ops = [(name, data) for name, data in operations.items() if "duration" in data]
        
        # Sort by average duration (descending)
        sorted_ops = sorted(duration_ops, key=lambda x: x[1]["duration"]["avg"], reverse=True)
        
        # Return top N operations
        result = []
        for name, data in sorted_ops[:limit]:
            result.append({
                "operation": name,
                "average_duration_ms": data["duration"]["avg"],
                "max_duration_ms": data["duration"]["max"],
                "call_count": data["count"]
            })
            
        return result
