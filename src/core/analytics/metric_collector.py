"""Metric collector for gathering analytics data"""
import time
import logging
from typing import Dict, List, Any, Optional, Callable, TypeVar, Generic, Union
from datetime import datetime
from contextlib import contextmanager

from src.core.analytics.metric import Metric, MetricType, MetricValue


T = TypeVar('T')


class MetricCollector:
    """
    Collects metrics for analytics
    
    This class provides methods for collecting various types of metrics,
    including timing, counting, and custom metrics.
    """
    
    def __init__(self, prefix: str = ""):
        """
        Initialize the metric collector
        
        Args:
            prefix: Optional prefix for metric names
        """
        self.metrics: List[Metric] = []
        self.prefix = prefix
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def _get_name(self, name: str) -> str:
        """
        Get the full metric name with prefix
        
        Args:
            name: Base metric name
            
        Returns:
            Full metric name with prefix
        """
        if not self.prefix:
            return name
        return f"{self.prefix}.{name}"
        
    def collect(
        self,
        name: str,
        value: MetricValue,
        metric_type: MetricType,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Collect a metric
        
        Args:
            name: Metric name
            value: Metric value
            metric_type: Type of metric
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        metric = Metric(
            name=self._get_name(name),
            value=value,
            metric_type=metric_type,
            context=context,
            tags=tags
        )
        
        self.metrics.append(metric)
        self.logger.debug(f"Collected metric: {metric}")
        
        return metric
        
    def count(
        self,
        name: str,
        value: int = 1,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Collect a count metric
        
        Args:
            name: Metric name
            value: Count value (default: 1)
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        return self.collect(
            name=name,
            value=value,
            metric_type=MetricType.COUNT,
            context=context,
            tags=tags
        )
        
    def timing(
        self,
        name: str,
        duration_ms: float,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Collect a timing metric
        
        Args:
            name: Metric name
            duration_ms: Duration in milliseconds
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        return self.collect(
            name=name,
            value=duration_ms,
            metric_type=MetricType.DURATION,
            context=context,
            tags=tags
        )
        
    @contextmanager
    def measure_time(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ):
        """
        Context manager for measuring execution time
        
        Args:
            name: Metric name
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Yields:
            None
        """
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            duration_ms = (end_time - start_time) * 1000
            self.timing(name, duration_ms, context, tags)
            
    def gauge(
        self,
        name: str,
        value: float,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Collect a gauge metric (point-in-time value)
        
        Args:
            name: Metric name
            value: Gauge value
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        return self.collect(
            name=name,
            value=value,
            metric_type=MetricType.CUSTOM,
            context=context,
            tags=tags
        )
        
    def success(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Record a success
        
        Args:
            name: Metric name
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        return self.collect(
            name=name,
            value=1,
            metric_type=MetricType.SUCCESS_COUNT,
            context=context,
            tags=tags
        )
        
    def error(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Record an error
        
        Args:
            name: Metric name
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        return self.collect(
            name=name,
            value=1,
            metric_type=MetricType.ERROR_COUNT,
            context=context,
            tags=tags
        )
        
    def rate(
        self,
        name: str,
        success_count: int,
        total_count: int,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ) -> Metric:
        """
        Calculate and collect a rate metric
        
        Args:
            name: Metric name
            success_count: Number of successes
            total_count: Total number of attempts
            context: Additional contextual information
            tags: Tags for categorizing the metric
            
        Returns:
            The collected metric
        """
        if total_count == 0:
            rate = 0.0
        else:
            rate = success_count / total_count
            
        return self.collect(
            name=name,
            value=rate,
            metric_type=MetricType.RATE,
            context=context,
            tags=tags
        )
        
    def get_metrics(self) -> List[Metric]:
        """
        Get all collected metrics
        
        Returns:
            List of collected metrics
        """
        return self.metrics
        
    def clear(self) -> None:
        """Clear all collected metrics"""
        self.metrics = []
        
    def get_metrics_by_type(self, metric_type: MetricType) -> List[Metric]:
        """
        Get metrics of a specific type
        
        Args:
            metric_type: Type of metrics to retrieve
            
        Returns:
            List of metrics of the specified type
        """
        return [m for m in self.metrics if m.metric_type == metric_type]
        
    def get_metrics_by_name(self, name: str) -> List[Metric]:
        """
        Get metrics with a specific name
        
        Args:
            name: Name of metrics to retrieve
            
        Returns:
            List of metrics with the specified name
        """
        full_name = self._get_name(name)
        return [m for m in self.metrics if m.name == full_name]
        
    def get_metrics_by_tag(self, tag_key: str, tag_value: Optional[str] = None) -> List[Metric]:
        """
        Get metrics with a specific tag
        
        Args:
            tag_key: Tag key to match
            tag_value: Optional tag value to match
            
        Returns:
            List of metrics with the specified tag
        """
        if tag_value is None:
            return [m for m in self.metrics if tag_key in m.tags]
        return [m for m in self.metrics if m.tags.get(tag_key) == tag_value]
