"""Metric definitions for analytics"""
from enum import Enum, auto
from typing import Dict, Any, Union, Optional
from datetime import datetime


class MetricType(Enum):
    """Types of metrics that can be collected"""
    
    # Timing metrics
    DURATION = auto()
    LATENCY = auto()
    RESPONSE_TIME = auto()
    
    # Count metrics
    COUNT = auto()
    ERROR_COUNT = auto()
    SUCCESS_COUNT = auto()
    
    # Rate metrics
    RATE = auto()
    ERROR_RATE = auto()
    SUCCESS_RATE = auto()
    
    # Resource metrics
    MEMORY_USAGE = auto()
    CPU_USAGE = auto()
    DISK_USAGE = auto()
    
    # Custom metrics
    CUSTOM = auto()


# Type for metric values - can be numeric or boolean
MetricValue = Union[int, float, bool]


class Metric:
    """
    Represents a single metric measurement
    
    This class encapsulates a metric with its type, value, timestamp,
    and associated metadata.
    """
    
    def __init__(
        self,
        name: str,
        value: MetricValue,
        metric_type: MetricType,
        timestamp: Optional[datetime] = None,
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[Dict[str, str]] = None
    ):
        """
        Initialize a metric
        
        Args:
            name: Name of the metric
            value: Value of the metric
            metric_type: Type of the metric
            timestamp: Time when the metric was collected (defaults to now)
            context: Additional contextual information
            tags: Tags for categorizing the metric
        """
        self.name = name
        self.value = value
        self.metric_type = metric_type
        self.timestamp = timestamp or datetime.now()
        self.context = context or {}
        self.tags = tags or {}
        
    def __str__(self) -> str:
        """String representation of the metric"""
        return f"{self.name} ({self.metric_type.name}): {self.value} at {self.timestamp}"
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the metric to a dictionary
        
        Returns:
            Dictionary representation of the metric
        """
        return {
            "name": self.name,
            "value": self.value,
            "type": self.metric_type.name,
            "timestamp": self.timestamp.isoformat(),
            "context": self.context,
            "tags": self.tags
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Metric':
        """
        Create a metric from a dictionary
        
        Args:
            data: Dictionary containing metric data
            
        Returns:
            Metric instance
        """
        return cls(
            name=data["name"],
            value=data["value"],
            metric_type=MetricType[data["type"]],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            context=data.get("context", {}),
            tags=data.get("tags", {})
        )
        
    def with_tag(self, key: str, value: str) -> 'Metric':
        """
        Add a tag to the metric
        
        Args:
            key: Tag key
            value: Tag value
            
        Returns:
            Self for method chaining
        """
        self.tags[key] = value
        return self
        
    def with_context(self, key: str, value: Any) -> 'Metric':
        """
        Add context information to the metric
        
        Args:
            key: Context key
            value: Context value
            
        Returns:
            Self for method chaining
        """
        self.context[key] = value
        return self
