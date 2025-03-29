"""Interface for report visualizers"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from src.core.reporting.report_interface import ReportInterface


class VisualizerInterface(ABC):
    """
    Interface for report visualizers
    
    Visualizers convert report data into visual representations
    like HTML, charts, or other formats.
    """
    
    @abstractmethod
    def visualize(self, report: ReportInterface) -> str:
        """
        Visualize a report
        
        Args:
            report: Report to visualize
            
        Returns:
            Visualization content as a string
        """
        pass
        
    @abstractmethod
    def save(self, report: ReportInterface, destination: str) -> str:
        """
        Visualize a report and save it to a file
        
        Args:
            report: Report to visualize
            destination: File path to save the visualization
            
        Returns:
            Path to the saved file
        """
        pass
        
    @abstractmethod
    def get_format(self) -> str:
        """
        Get the format of the visualization
        
        Returns:
            Format name (e.g., 'html', 'svg', 'png')
        """
        pass
