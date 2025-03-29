"""Interface for metric analyzers"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

from src.core.analytics.metric import Metric


class AnalyzerInterface(ABC):
    """
    Interface for metric analyzers
    
    Analyzers process metrics to extract insights and statistics.
    """
    
    @abstractmethod
    def analyze(self, metrics: List[Metric]) -> Dict[str, Any]:
        """
        Analyze metrics and return results
        
        Args:
            metrics: List of metrics to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        pass
        
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the analyzer
        
        Returns:
            Analyzer name
        """
        pass
        
    @abstractmethod
    def get_description(self) -> str:
        """
        Get a description of the analyzer
        
        Returns:
            Analyzer description
        """
        pass
