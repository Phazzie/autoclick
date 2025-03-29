"""Performance analyzer for metrics"""
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from src.core.analytics.metric import Metric, MetricType
from src.core.analytics.analyzers.analyzer_interface import AnalyzerInterface


class PerformanceAnalyzer(AnalyzerInterface):
    """
    Analyzer for performance metrics
    
    This analyzer focuses on performance-related metrics like
    duration, latency, and resource usage.
    """
    
    def get_name(self) -> str:
        """
        Get the name of the analyzer
        
        Returns:
            Analyzer name
        """
        return "Performance Analyzer"
        
    def get_description(self) -> str:
        """
        Get a description of the analyzer
        
        Returns:
            Analyzer description
        """
        return "Analyzes performance metrics to identify bottlenecks and optimization opportunities"
        
    def analyze(self, metrics: List[Metric]) -> Dict[str, Any]:
        """
        Analyze metrics and return results
        
        Args:
            metrics: List of metrics to analyze
            
        Returns:
            Dictionary containing analysis results
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
        
        # Group by operation/component
        grouped_by_operation = self._group_by_operation(performance_metrics)
        
        # Analyze each operation
        results = {
            "operations": {},
            "summary": {},
            "bottlenecks": [],
            "recommendations": []
        }
        
        # Process each operation
        for operation, op_metrics in grouped_by_operation.items():
            op_results = self._analyze_operation(operation, op_metrics)
            results["operations"][operation] = op_results
            
            # Check if this is a bottleneck
            if op_results.get("is_bottleneck", False):
                results["bottlenecks"].append({
                    "operation": operation,
                    "metrics": op_results,
                    "impact": op_results.get("bottleneck_impact", "medium")
                })
                
                # Add recommendation
                results["recommendations"].append({
                    "operation": operation,
                    "recommendation": op_results.get("recommendation", "Investigate performance issues"),
                    "priority": op_results.get("priority", "medium")
                })
                
        # Create summary
        results["summary"] = self._create_summary(results["operations"])
        
        return results
        
    def _group_by_operation(self, metrics: List[Metric]) -> Dict[str, List[Metric]]:
        """
        Group metrics by operation or component
        
        Args:
            metrics: List of metrics to group
            
        Returns:
            Dictionary mapping operation names to lists of metrics
        """
        grouped = defaultdict(list)
        
        for metric in metrics:
            # Try to get operation from tags or context
            operation = None
            
            # Check tags
            if "operation" in metric.tags:
                operation = metric.tags["operation"]
            elif "component" in metric.tags:
                operation = metric.tags["component"]
            elif "action" in metric.tags:
                operation = metric.tags["action"]
                
            # Check context
            if operation is None and "operation" in metric.context:
                operation = metric.context["operation"]
            elif operation is None and "component" in metric.context:
                operation = metric.context["component"]
            elif operation is None and "action" in metric.context:
                operation = metric.context["action"]
                
            # Fall back to metric name
            if operation is None:
                operation = metric.name
                
            grouped[operation].append(metric)
            
        return grouped
        
    def _analyze_operation(self, operation: str, metrics: List[Metric]) -> Dict[str, Any]:
        """
        Analyze metrics for a specific operation
        
        Args:
            operation: Name of the operation
            metrics: List of metrics for the operation
            
        Returns:
            Dictionary containing analysis results
        """
        # Group by metric type
        metrics_by_type = defaultdict(list)
        for metric in metrics:
            metrics_by_type[metric.metric_type].append(metric)
            
        results = {
            "operation": operation,
            "count": len(metrics),
            "metric_types": [t.name for t in metrics_by_type.keys()]
        }
        
        # Analyze duration metrics
        if MetricType.DURATION in metrics_by_type:
            duration_values = [m.value for m in metrics_by_type[MetricType.DURATION]]
            results["duration"] = self._analyze_duration(duration_values)
            
            # Check if this is a bottleneck based on duration
            if results["duration"]["avg"] > 1000:  # More than 1 second
                results["is_bottleneck"] = True
                results["bottleneck_impact"] = "high"
                results["recommendation"] = f"Optimize the '{operation}' operation to reduce execution time"
                results["priority"] = "high"
            elif results["duration"]["avg"] > 500:  # More than 500ms
                results["is_bottleneck"] = True
                results["bottleneck_impact"] = "medium"
                results["recommendation"] = f"Consider optimizing the '{operation}' operation"
                results["priority"] = "medium"
            elif results["duration"]["max"] > 2000:  # Max over 2 seconds
                results["is_bottleneck"] = True
                results["bottleneck_impact"] = "medium"
                results["recommendation"] = f"Investigate occasional slow execution in '{operation}'"
                results["priority"] = "medium"
                
        # Analyze resource usage metrics
        for resource_type in (MetricType.CPU_USAGE, MetricType.MEMORY_USAGE, MetricType.DISK_USAGE):
            if resource_type in metrics_by_type:
                resource_values = [m.value for m in metrics_by_type[resource_type]]
                resource_name = resource_type.name.lower()
                results[resource_name] = self._analyze_resource_usage(resource_values)
                
                # Check if this is a bottleneck based on resource usage
                if results[resource_name]["avg"] > 80:  # More than 80%
                    results["is_bottleneck"] = True
                    results["bottleneck_impact"] = "high"
                    results["recommendation"] = f"Reduce {resource_name} in '{operation}'"
                    results["priority"] = "high"
                elif results[resource_name]["avg"] > 60:  # More than 60%
                    results["is_bottleneck"] = True
                    results["bottleneck_impact"] = "medium"
                    results["recommendation"] = f"Monitor {resource_name} in '{operation}'"
                    results["priority"] = "medium"
                    
        return results
        
    def _analyze_duration(self, duration_values: List[float]) -> Dict[str, Any]:
        """
        Analyze duration values
        
        Args:
            duration_values: List of duration values in milliseconds
            
        Returns:
            Dictionary containing duration analysis
        """
        if not duration_values:
            return {"count": 0}
            
        sorted_values = sorted(duration_values)
        
        return {
            "count": len(duration_values),
            "min": min(duration_values),
            "max": max(duration_values),
            "avg": sum(duration_values) / len(duration_values),
            "median": sorted_values[len(sorted_values) // 2],
            "p95": sorted_values[int(len(sorted_values) * 0.95)] if len(sorted_values) >= 20 else max(duration_values),
            "p99": sorted_values[int(len(sorted_values) * 0.99)] if len(sorted_values) >= 100 else max(duration_values)
        }
        
    def _analyze_resource_usage(self, usage_values: List[float]) -> Dict[str, Any]:
        """
        Analyze resource usage values
        
        Args:
            usage_values: List of resource usage values (percentage)
            
        Returns:
            Dictionary containing resource usage analysis
        """
        if not usage_values:
            return {"count": 0}
            
        sorted_values = sorted(usage_values)
        
        return {
            "count": len(usage_values),
            "min": min(usage_values),
            "max": max(usage_values),
            "avg": sum(usage_values) / len(usage_values),
            "median": sorted_values[len(sorted_values) // 2],
            "p95": sorted_values[int(len(sorted_values) * 0.95)] if len(sorted_values) >= 20 else max(usage_values)
        }
        
    def _create_summary(self, operations: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a summary of all operations
        
        Args:
            operations: Dictionary mapping operation names to analysis results
            
        Returns:
            Dictionary containing summary information
        """
        if not operations:
            return {"operation_count": 0}
            
        # Count bottlenecks
        bottleneck_count = sum(1 for op in operations.values() if op.get("is_bottleneck", False))
        
        # Find slowest and fastest operations
        duration_ops = [(op_name, op_data) for op_name, op_data in operations.items() if "duration" in op_data]
        
        slowest_op = None
        fastest_op = None
        
        if duration_ops:
            slowest_op = max(duration_ops, key=lambda x: x[1]["duration"]["avg"])
            fastest_op = min(duration_ops, key=lambda x: x[1]["duration"]["avg"])
            
        # Calculate total and average duration
        total_duration = 0
        duration_count = 0
        
        for op_data in operations.values():
            if "duration" in op_data:
                total_duration += op_data["duration"]["avg"] * op_data["count"]
                duration_count += op_data["count"]
                
        avg_duration = total_duration / duration_count if duration_count > 0 else 0
        
        return {
            "operation_count": len(operations),
            "bottleneck_count": bottleneck_count,
            "total_duration": total_duration,
            "avg_duration": avg_duration,
            "slowest_operation": slowest_op[0] if slowest_op else None,
            "fastest_operation": fastest_op[0] if fastest_op else None
        }
