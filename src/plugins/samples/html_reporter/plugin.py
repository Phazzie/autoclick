"""HTML reporter plugin implementation"""
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from src.plugins.interfaces import ReporterPluginInterface


class HTMLReporterPlugin(ReporterPluginInterface):
    """Generates HTML reports from automation results"""
    
    def __init__(self) -> None:
        """Initialize the HTML reporter plugin"""
        self.logger = logging.getLogger(__name__)
        self.config: Dict[str, Any] = {}
        self.template_path: Optional[str] = None
    
    def initialize(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin with configuration
        
        Args:
            config: Configuration dictionary
        """
        self.logger.info("Initializing HTML reporter plugin")
        self.config = config
        self.template_path = config.get("template_path")
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about the plugin
        
        Returns:
            Dictionary containing plugin information
        """
        return {
            "name": "html_reporter",
            "version": "1.0.0",
            "description": "Generates HTML reports from automation results",
            "author": "AUTOCLICK Team",
            "supported_formats": self.get_supported_formats(),
        }
    
    def cleanup(self) -> None:
        """Clean up resources"""
        self.logger.info("Cleaning up HTML reporter plugin")
    
    def generate_report(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Generate an HTML report from data
        
        Args:
            data: Data to include in the report
            output_path: Path to save the report
            
        Returns:
            Path to the generated report
        """
        self.logger.info(f"Generating HTML report at {output_path}")
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate HTML content
        html_content = self._generate_html_content(data)
        
        # Write the HTML file
        with open(output_path, "w") as f:
            f.write(html_content)
        
        return output_path
    
    def get_supported_formats(self) -> List[str]:
        """
        Get the supported report formats
        
        Returns:
            List of format strings
        """
        return ["html"]
    
    def _generate_html_content(self, data: Dict[str, Any]) -> str:
        """
        Generate HTML content from data
        
        Args:
            data: Data to include in the report
            
        Returns:
            HTML content
        """
        # Get the results from the data
        results = data.get("results", [])
        
        # Count results by status
        status_counts = {}
        for result in results:
            status = result.get("status", "unknown")
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Calculate success rate
        total = len(results)
        success = status_counts.get("success", 0)
        success_rate = (success / total) * 100 if total > 0 else 0
        
        # Generate HTML
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Automation Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            color: #333;
        }}
        h1, h2 {{
            color: #2c3e50;
        }}
        .summary {{
            background-color: #f8f9fa;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 20px;
        }}
        .success {{
            color: #28a745;
        }}
        .error {{
            color: #dc3545;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>
    <h1>Automation Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Scripts: {total}</p>
        <p>Success: <span class="success">{success}</span></p>
        <p>Success Rate: <span class="{
            'success' if success_rate >= 80 else 'error'
        }">{success_rate:.2f}%</span></p>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>
    
    <h2>Results</h2>
    <table>
        <tr>
            <th>Script</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Message</th>
        </tr>
"""
        
        # Add rows for each result
        for result in results:
            script = result.get("script", "Unknown")
            status = result.get("status", "unknown")
            duration = result.get("duration", 0)
            message = result.get("message", "")
            
            html += f"""
        <tr>
            <td>{script}</td>
            <td class="{'success' if status == 'success' else 'error'}">{status}</td>
            <td>{duration:.2f}s</td>
            <td>{message}</td>
        </tr>"""
        
        # Close the HTML
        html += """
    </table>
</body>
</html>
"""
        
        return html
