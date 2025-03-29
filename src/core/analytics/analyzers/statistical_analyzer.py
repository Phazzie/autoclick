"""Statistical analyzer for metrics"""
import statistics
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

from src.core.analytics.metric import Metric, MetricType
from src.core.analytics.analyzers.analyzer_interface import AnalyzerInterface


class StatisticalAnalyzer(AnalyzerInterface):
    """
    Analyzer for statistical analysis of metrics
    
    This analyzer calculates statistical measures like mean, median,
    standard deviation, and percentiles.
    """
    
    def get_name(self) -> str:
        """
        Get the name of the analyzer
        
        Returns:
            Analyzer name
        """
        return "Statistical Analyzer"
        
    def get_description(self) -> str:
        """
        Get a description of the analyzer
        
        Returns:
            Analyzer description
        """
        return "Calculates statistical measures for metrics"
        
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
                
            # Extract values
            values = [m.value for m in group_metrics]
            
            # Calculate statistics
            stats = self._calculate_statistics(values)
            
            # Store results
            results[f"{name} ({metric_type.name})"] = stats
            
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
        
    def _calculate_statistics(self, values: List[float]) -> Dict[str, Any]:
        """
        Calculate statistics for a list of values
        
        Args:
            values: List of numeric values
            
        Returns:
            Dictionary containing statistical measures
        """
        if not values:
            return {"count": 0}
            
        result = {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "range": max(values) - min(values),
            "sum": sum(values),
            "mean": statistics.mean(values)
        }
        
        # Add median if we have enough values
        if len(values) >= 1:
            result["median"] = statistics.median(values)
            
        # Add standard deviation and variance if we have enough values
        if len(values) >= 2:
            result["variance"] = statistics.variance(values)
            result["std_dev"] = statistics.stdev(values)
            
        # Add percentiles
        sorted_values = sorted(values)
        result["percentiles"] = {
            "25": self._percentile(sorted_values, 25),
            "50": self._percentile(sorted_values, 50),
            "75": self._percentile(sorted_values, 75),
            "90": self._percentile(sorted_values, 90),
            "95": self._percentile(sorted_values, 95),
            "99": self._percentile(sorted_values, 99)
        }
        
        # Add distribution information
        result["distribution"] = self._calculate_distribution(values)
        
        return result
        
    def _percentile(self, sorted_values: List[float], percentile: int) -> float:
        """
        Calculate a percentile from sorted values
        
        Args:
            sorted_values: List of values sorted in ascending order
            percentile: Percentile to calculate (0-100)
            
        Returns:
            Percentile value
        """
        if not sorted_values:
            return 0
            
        k = (len(sorted_values) - 1) * (percentile / 100)
        f = int(k)
        c = int(k) + 1 if k < len(sorted_values) - 1 else int(k)
        
        if f == c:
            return sorted_values[f]
        return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)
        
    def _calculate_distribution(self, values: List[float]) -> Dict[str, Any]:
        """
        Calculate distribution information for values
        
        Args:
            values: List of numeric values
            
        Returns:
            Dictionary containing distribution information
        """
        if not values:
            return {"bins": []}
            
        # Determine bin count (square root of count, capped)
        bin_count = min(10, max(5, int(len(values) ** 0.5)))
        
        # Create bins
        min_val = min(values)
        max_val = max(values)
        
        # Handle case where all values are the same
        if min_val == max_val:
            return {
                "bins": [{
                    "min": min_val,
                    "max": max_val,
                    "count": len(values),
                    "percentage": 100.0
                }]
            }
            
        bin_width = (max_val - min_val) / bin_count
        bins = []
        
        for i in range(bin_count):
            bin_min = min_val + i * bin_width
            bin_max = min_val + (i + 1) * bin_width
            
            # Adjust the last bin to include the max value
            if i == bin_count - 1:
                bin_max = max_val
                
            # Count values in this bin
            bin_count = sum(1 for v in values if bin_min <= v <= bin_max)
            
            bins.append({
                "min": bin_min,
                "max": bin_max,
                "count": bin_count,
                "percentage": (bin_count / len(values)) * 100
            })
            
        return {"bins": bins}
