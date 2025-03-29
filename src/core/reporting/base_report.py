"""
Base report implementation with common functionality for all report types.
"""
import json
import csv
import os
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging

from src.core.reporting.report_interface import ReportInterface, ReportMetadata


class BaseReport(ReportInterface):
    """
    Base implementation of the report interface with common functionality.
    
    This class provides common methods and properties for all report types,
    including metadata management, basic data collection, and export functionality.
    """
    
    def __init__(
        self,
        report_type: str,
        title: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize the base report.
        
        Args:
            report_type: Type of the report
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
        """
        self.metadata = ReportMetadata(
            report_type=report_type,
            title=title,
            description=description,
            tags=tags
        )
        self.data: Dict[str, Any] = {}
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def collect_data(self, source: Any) -> None:
        """
        Collect data from the specified source for the report.
        
        This base implementation stores the source for subclasses to process.
        Subclasses should override this method to extract specific data.
        
        Args:
            source: The data source to collect from
        """
        self.source = source
        self.data["collection_time"] = datetime.now().isoformat()
    
    def generate(self) -> Dict[str, Any]:
        """
        Generate the report based on collected data.
        
        This base implementation returns the collected data with metadata.
        Subclasses should override this method to generate specific report content.
        
        Returns:
            A dictionary containing the report data
        """
        result = {
            "metadata": self.metadata.to_dict(),
            "data": self.data
        }
        return result
    
    def export(self, format_type: str, destination: Optional[str] = None) -> Union[str, bytes]:
        """
        Export the report in the specified format.
        
        Args:
            format_type: The format to export (e.g., 'html', 'pdf', 'json', 'csv')
            destination: Optional file path to save the report
            
        Returns:
            The report content as string or bytes depending on the format
        """
        report_data = self.generate()
        
        if format_type.lower() == 'json':
            content = json.dumps(report_data, indent=2)
            if destination:
                with open(destination, 'w', encoding='utf-8') as f:
                    f.write(content)
            return content
            
        elif format_type.lower() == 'csv':
            # Flatten the data structure for CSV
            flattened_data = self._flatten_dict(report_data)
            
            if destination:
                with open(destination, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(flattened_data.keys())
                    writer.writerow(flattened_data.values())
                
            # Return CSV as string
            output = []
            writer = csv.writer(output)
            writer.writerow(flattened_data.keys())
            writer.writerow(flattened_data.values())
            return '\n'.join(output)
            
        elif format_type.lower() == 'html':
            # Simple HTML template
            html_content = self._generate_html(report_data)
            
            if destination:
                with open(destination, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            return html_content
            
        elif format_type.lower() == 'txt':
            # Simple text format
            content = self._generate_text(report_data)
            
            if destination:
                with open(destination, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return content
            
        else:
            raise ValueError(f"Unsupported export format: {format_type}")
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get metadata about the report.
        
        Returns:
            A dictionary containing report metadata
        """
        return self.metadata.to_dict()
    
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
        """
        Flatten a nested dictionary for CSV export.
        
        Args:
            d: The dictionary to flatten
            parent_key: The parent key for nested dictionaries
            sep: Separator for nested keys
            
        Returns:
            A flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                # Convert lists to string representation
                items.append((new_key, str(v)))
            else:
                items.append((new_key, v))
                
        return dict(items)
    
    def _generate_html(self, data: Dict[str, Any]) -> str:
        """
        Generate HTML representation of the report.
        
        Args:
            data: Report data
            
        Returns:
            HTML string
        """
        metadata = data.get('metadata', {})
        report_data = data.get('data', {})
        
        html = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            f'<title>{metadata.get("title", "Report")}</title>',
            '<style>',
            'body { font-family: Arial, sans-serif; margin: 20px; }',
            'h1 { color: #4a6da7; }',
            'h2 { color: #5e81ac; }',
            'table { border-collapse: collapse; width: 100%; }',
            'th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }',
            'th { background-color: #f2f2f2; }',
            'tr:nth-child(even) { background-color: #f9f9f9; }',
            '.metadata { background-color: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 20px; }',
            '</style>',
            '</head>',
            '<body>',
            f'<h1>{metadata.get("title", "Report")}</h1>',
            '<div class="metadata">',
            '<h2>Metadata</h2>',
            '<table>',
            '<tr><th>Property</th><th>Value</th></tr>'
        ]
        
        # Add metadata
        for key, value in metadata.items():
            html.append(f'<tr><td>{key}</td><td>{value}</td></tr>')
        
        html.append('</table>')
        html.append('</div>')
        
        # Add report data
        html.append('<h2>Report Data</h2>')
        html.append('<table>')
        html.append('<tr><th>Property</th><th>Value</th></tr>')
        
        # Flatten data for display
        flat_data = self._flatten_dict(report_data)
        for key, value in flat_data.items():
            html.append(f'<tr><td>{key}</td><td>{value}</td></tr>')
        
        html.append('</table>')
        html.append('</body>')
        html.append('</html>')
        
        return '\n'.join(html)
    
    def _generate_text(self, data: Dict[str, Any]) -> str:
        """
        Generate text representation of the report.
        
        Args:
            data: Report data
            
        Returns:
            Text string
        """
        metadata = data.get('metadata', {})
        report_data = data.get('data', {})
        
        lines = [
            f"=== {metadata.get('title', 'Report')} ===",
            "",
            "--- Metadata ---"
        ]
        
        # Add metadata
        for key, value in metadata.items():
            lines.append(f"{key}: {value}")
        
        lines.append("")
        lines.append("--- Report Data ---")
        
        # Flatten data for display
        flat_data = self._flatten_dict(report_data)
        for key, value in flat_data.items():
            lines.append(f"{key}: {value}")
        
        return '\n'.join(lines)
