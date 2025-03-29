"""Time series analyzer for metrics"""
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import statistics
from collections import defaultdict

from src.core.analytics.metric import Metric, MetricType
from src.core.analytics.analyzers.analyzer_interface import AnalyzerInterface


class TimeSeriesAnalyzer(AnalyzerInterface):
    """
    Analyzer for time series metrics
    
    This analyzer processes metrics over time to identify trends,
    patterns, and anomalies.
    """
    
    def __init__(
        self,
        interval_minutes: int = 5,
        min_points_for_trend: int = 3
    ):
        """
        Initialize the time series analyzer
        
        Args:
            interval_minutes: Size of time intervals in minutes
            min_points_for_trend: Minimum number of points needed to calculate a trend
        """
        self.interval_minutes = interval_minutes
        self.min_points_for_trend = min_points_for_trend
        
    def get_name(self) -> str:
        """
        Get the name of the analyzer
        
        Returns:
            Analyzer name
        """
        return "Time Series Analyzer"
        
    def get_description(self) -> str:
        """
        Get a description of the analyzer
        
        Returns:
            Analyzer description
        """
        return "Analyzes metrics over time to identify trends and patterns"
        
    def analyze(self, metrics: List[Metric]) -> Dict[str, Any]:
        """
        Analyze metrics and return results
        
        Args:
            metrics: List of metrics to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        # Group metrics by name and type
        grouped_metrics = self._group_metrics(metrics)
        
        # Analyze each group
        results = {}
        for (name, metric_type), group_metrics in grouped_metrics.items():
            # Skip groups with non-numeric values
            if not all(isinstance(m.value, (int, float)) for m in group_metrics):
                continue
                
            # Sort by timestamp
            sorted_metrics = sorted(group_metrics, key=lambda m: m.timestamp)
            
            # Skip groups with too few points
            if len(sorted_metrics) < self.min_points_for_trend:
                continue
                
            # Calculate time series statistics
            time_series_data = self._calculate_time_series(sorted_metrics)
            
            # Calculate trends
            trends = self._calculate_trends(time_series_data)
            
            # Store results
            results[f"{name} ({metric_type.name})"] = {
                "time_series": time_series_data,
                "trends": trends,
                "summary": self._summarize_time_series(time_series_data)
            }
            
        return results
        
    def _group_metrics(self, metrics: List[Metric]) -> Dict[Tuple[str, MetricType], List[Metric]]:
        """
        Group metrics by name and type
        
        Args:
            metrics: List of metrics to group
            
        Returns:
            Dictionary mapping (name, type) to list of metrics
        """
        grouped = defaultdict(list)
        for metric in metrics:
            key = (metric.name, metric.metric_type)
            grouped[key].append(metric)
        return grouped
        
    def _calculate_time_series(self, metrics: List[Metric]) -> List[Dict[str, Any]]:
        """
        Calculate time series data points
        
        Args:
            metrics: List of metrics sorted by timestamp
            
        Returns:
            List of time series data points
        """
        # Group by time interval
        interval = timedelta(minutes=self.interval_minutes)
        intervals = defaultdict(list)
        
        for metric in metrics:
            # Round timestamp to interval
            rounded_time = metric.timestamp.replace(
                second=0,
                microsecond=0,
                minute=(metric.timestamp.minute // self.interval_minutes) * self.interval_minutes
            )
            intervals[rounded_time].append(metric.value)
            
        # Calculate statistics for each interval
        time_series = []
        for timestamp, values in sorted(intervals.items()):
            time_series.append({
                "timestamp": timestamp.isoformat(),
                "count": len(values),
                "min": min(values),
                "max": max(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "values": values
            })
            
        return time_series
        
    def _calculate_trends(self, time_series: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate trends from time series data
        
        Args:
            time_series: List of time series data points
            
        Returns:
            Dictionary containing trend analysis
        """
        if not time_series or len(time_series) < self.min_points_for_trend:
            return {"trend": "insufficient_data"}
            
        # Extract mean values
        means = [point["mean"] for point in time_series]
        
        # Calculate simple linear trend
        n = len(means)
        if n < 2:
            return {"trend": "insufficient_data"}
            
        # Calculate slope using simple linear regression
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(means) / n
        
        numerator = sum((x[i] - x_mean) * (means[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator
            
        # Determine trend direction
        if abs(slope) < 0.001:
            trend = "stable"
        elif slope > 0:
            trend = "increasing"
        else:
            trend = "decreasing"
            
        # Calculate percent change
        first_value = means[0]
        last_value = means[-1]
        
        if first_value == 0:
            percent_change = float('inf') if last_value > 0 else 0
        else:
            percent_change = ((last_value - first_value) / first_value) * 100
            
        return {
            "trend": trend,
            "slope": slope,
            "percent_change": percent_change,
            "first_value": first_value,
            "last_value": last_value
        }
        
    def _summarize_time_series(self, time_series: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create a summary of time series data
        
        Args:
            time_series: List of time series data points
            
        Returns:
            Dictionary containing summary statistics
        """
        if not time_series:
            return {"status": "no_data"}
            
        # Extract statistics
        all_values = []
        for point in time_series:
            all_values.extend(point["values"])
            
        if not all_values:
            return {"status": "no_data"}
            
        # Calculate overall statistics
        return {
            "count": len(all_values),
            "min": min(all_values),
            "max": max(all_values),
            "mean": statistics.mean(all_values),
            "median": statistics.median(all_values),
            "intervals": len(time_series),
            "start_time": time_series[0]["timestamp"],
            "end_time": time_series[-1]["timestamp"]
        }
