"""Analytics manager for coordinating metric collection and analysis"""
import json
import os
import logging
from typing import Dict, List, Any, Optional, Type, Set, Union
from datetime import datetime

from src.core.analytics.metric import Metric, MetricType
from src.core.analytics.metric_collector import MetricCollector


class AnalyticsManager:
    """
    Manages analytics data collection and analysis
    
    This class coordinates metric collectors and analyzers to provide
    a unified interface for analytics.
    """
    
    def __init__(self, storage_dir: str = "analytics"):
        """
        Initialize the analytics manager
        
        Args:
            storage_dir: Directory for storing analytics data
        """
        self.storage_dir = storage_dir
        self.collectors: Dict[str, MetricCollector] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create storage directory if it doesn't exist
        os.makedirs(storage_dir, exist_ok=True)
        
    def get_collector(self, name: str, create_if_missing: bool = True) -> Optional[MetricCollector]:
        """
        Get a metric collector by name
        
        Args:
            name: Name of the collector
            create_if_missing: Whether to create the collector if it doesn't exist
            
        Returns:
            The metric collector, or None if not found and not created
        """
        if name in self.collectors:
            return self.collectors[name]
            
        if create_if_missing:
            collector = MetricCollector(prefix=name)
            self.collectors[name] = collector
            return collector
            
        return None
        
    def register_collector(self, name: str, collector: MetricCollector) -> None:
        """
        Register a metric collector
        
        Args:
            name: Name for the collector
            collector: Metric collector to register
        """
        self.collectors[name] = collector
        
    def remove_collector(self, name: str) -> None:
        """
        Remove a metric collector
        
        Args:
            name: Name of the collector to remove
        """
        if name in self.collectors:
            del self.collectors[name]
            
    def get_all_metrics(self) -> List[Metric]:
        """
        Get all metrics from all collectors
        
        Returns:
            List of all collected metrics
        """
        all_metrics = []
        for collector in self.collectors.values():
            all_metrics.extend(collector.get_metrics())
        return all_metrics
        
    def get_metrics_by_type(self, metric_type: MetricType) -> List[Metric]:
        """
        Get metrics of a specific type from all collectors
        
        Args:
            metric_type: Type of metrics to retrieve
            
        Returns:
            List of metrics of the specified type
        """
        all_metrics = []
        for collector in self.collectors.values():
            all_metrics.extend(collector.get_metrics_by_type(metric_type))
        return all_metrics
        
    def get_metrics_by_tag(self, tag_key: str, tag_value: Optional[str] = None) -> List[Metric]:
        """
        Get metrics with a specific tag from all collectors
        
        Args:
            tag_key: Tag key to match
            tag_value: Optional tag value to match
            
        Returns:
            List of metrics with the specified tag
        """
        all_metrics = []
        for collector in self.collectors.values():
            all_metrics.extend(collector.get_metrics_by_tag(tag_key, tag_value))
        return all_metrics
        
    def clear_all_metrics(self) -> None:
        """Clear all metrics from all collectors"""
        for collector in self.collectors.values():
            collector.clear()
            
    def save_metrics(self, filename: str) -> str:
        """
        Save all metrics to a file
        
        Args:
            filename: Name of the file to save to
            
        Returns:
            Full path to the saved file
        """
        # Get all metrics
        all_metrics = self.get_all_metrics()
        
        # Convert to dictionaries
        metric_dicts = [metric.to_dict() for metric in all_metrics]
        
        # Create full path
        if not filename.endswith(".json"):
            filename += ".json"
        full_path = os.path.join(self.storage_dir, filename)
        
        # Save to file
        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(metric_dicts, f, indent=2)
            
        self.logger.info(f"Saved {len(all_metrics)} metrics to {full_path}")
        return full_path
        
    def load_metrics(self, filename: str) -> List[Metric]:
        """
        Load metrics from a file
        
        Args:
            filename: Name of the file to load from
            
        Returns:
            List of loaded metrics
            
        Raises:
            FileNotFoundError: If the file doesn't exist
        """
        # Create full path
        if not filename.endswith(".json"):
            filename += ".json"
        full_path = os.path.join(self.storage_dir, filename)
        
        # Load from file
        with open(full_path, "r", encoding="utf-8") as f:
            metric_dicts = json.load(f)
            
        # Convert to metrics
        metrics = [Metric.from_dict(d) for d in metric_dicts]
        
        self.logger.info(f"Loaded {len(metrics)} metrics from {full_path}")
        return metrics
        
    def get_metric_names(self) -> Set[str]:
        """
        Get all unique metric names
        
        Returns:
            Set of unique metric names
        """
        names = set()
        for metric in self.get_all_metrics():
            names.add(metric.name)
        return names
        
    def get_metric_types(self) -> Set[MetricType]:
        """
        Get all unique metric types
        
        Returns:
            Set of unique metric types
        """
        types = set()
        for metric in self.get_all_metrics():
            types.add(metric.metric_type)
        return types
        
    def get_tag_keys(self) -> Set[str]:
        """
        Get all unique tag keys
        
        Returns:
            Set of unique tag keys
        """
        keys = set()
        for metric in self.get_all_metrics():
            keys.update(metric.tags.keys())
        return keys
        
    def get_tag_values(self, tag_key: str) -> Set[str]:
        """
        Get all unique values for a tag key
        
        Args:
            tag_key: Tag key to get values for
            
        Returns:
            Set of unique tag values
        """
        values = set()
        for metric in self.get_all_metrics():
            if tag_key in metric.tags:
                values.add(metric.tags[tag_key])
        return values
