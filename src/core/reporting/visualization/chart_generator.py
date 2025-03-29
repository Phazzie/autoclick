"""Chart generator for creating data visualizations"""
from typing import Any, Dict, List, Optional, Tuple
import json


class ChartGenerator:
    """
    Generates chart definitions for data visualization
    
    This class creates chart definitions that can be rendered
    by JavaScript libraries like Chart.js.
    """
    
    @staticmethod
    def create_bar_chart(
        labels: List[str],
        data: List[float],
        title: str,
        x_label: str = "",
        y_label: str = "",
        colors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a bar chart definition
        
        Args:
            labels: Labels for the x-axis
            data: Data values for the bars
            title: Chart title
            x_label: Label for the x-axis
            y_label: Label for the y-axis
            colors: Optional list of colors for the bars
            
        Returns:
            Chart definition as a dictionary
        """
        if colors is None:
            colors = ["#4e73df"]
            
        # Ensure colors list is long enough
        while len(colors) < len(data):
            colors.extend(colors)
        colors = colors[:len(data)]
        
        return {
            "type": "bar",
            "data": {
                "labels": labels,
                "datasets": [{
                    "label": title,
                    "data": data,
                    "backgroundColor": colors
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "title": {
                    "display": True,
                    "text": title
                },
                "scales": {
                    "xAxes": [{
                        "scaleLabel": {
                            "display": bool(x_label),
                            "labelString": x_label
                        }
                    }],
                    "yAxes": [{
                        "scaleLabel": {
                            "display": bool(y_label),
                            "labelString": y_label
                        },
                        "ticks": {
                            "beginAtZero": True
                        }
                    }]
                }
            }
        }
        
    @staticmethod
    def create_pie_chart(
        labels: List[str],
        data: List[float],
        title: str,
        colors: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a pie chart definition
        
        Args:
            labels: Labels for the segments
            data: Data values for the segments
            title: Chart title
            colors: Optional list of colors for the segments
            
        Returns:
            Chart definition as a dictionary
        """
        if colors is None:
            colors = [
                "#4e73df", "#1cc88a", "#36b9cc", "#f6c23e", "#e74a3b",
                "#5a5c69", "#858796", "#6610f2", "#6f42c1", "#e83e8c"
            ]
            
        # Ensure colors list is long enough
        while len(colors) < len(data):
            colors.extend(colors)
        colors = colors[:len(data)]
        
        return {
            "type": "pie",
            "data": {
                "labels": labels,
                "datasets": [{
                    "data": data,
                    "backgroundColor": colors
                }]
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "title": {
                    "display": True,
                    "text": title
                },
                "legend": {
                    "position": "right"
                }
            }
        }
        
    @staticmethod
    def create_line_chart(
        labels: List[str],
        datasets: List[Dict[str, Any]],
        title: str,
        x_label: str = "",
        y_label: str = ""
    ) -> Dict[str, Any]:
        """
        Create a line chart definition
        
        Args:
            labels: Labels for the x-axis
            datasets: List of dataset definitions
            title: Chart title
            x_label: Label for the x-axis
            y_label: Label for the y-axis
            
        Returns:
            Chart definition as a dictionary
        """
        return {
            "type": "line",
            "data": {
                "labels": labels,
                "datasets": datasets
            },
            "options": {
                "responsive": True,
                "maintainAspectRatio": False,
                "title": {
                    "display": True,
                    "text": title
                },
                "scales": {
                    "xAxes": [{
                        "scaleLabel": {
                            "display": bool(x_label),
                            "labelString": x_label
                        }
                    }],
                    "yAxes": [{
                        "scaleLabel": {
                            "display": bool(y_label),
                            "labelString": y_label
                        },
                        "ticks": {
                            "beginAtZero": True
                        }
                    }]
                }
            }
        }
        
    @staticmethod
    def create_dataset(
        label: str,
        data: List[float],
        color: str = "#4e73df",
        fill: bool = False
    ) -> Dict[str, Any]:
        """
        Create a dataset definition for a line chart
        
        Args:
            label: Dataset label
            data: Data values
            color: Line color
            fill: Whether to fill the area under the line
            
        Returns:
            Dataset definition as a dictionary
        """
        return {
            "label": label,
            "data": data,
            "borderColor": color,
            "backgroundColor": color if fill else "transparent",
            "fill": fill,
            "lineTension": 0.3,
            "pointRadius": 3,
            "pointBackgroundColor": color,
            "pointBorderColor": color,
            "pointHoverRadius": 5,
            "pointHoverBackgroundColor": color,
            "pointHoverBorderColor": color
        }
        
    @staticmethod
    def to_json(chart_def: Dict[str, Any]) -> str:
        """
        Convert a chart definition to JSON
        
        Args:
            chart_def: Chart definition
            
        Returns:
            JSON string
        """
        return json.dumps(chart_def)
        
    @staticmethod
    def create_chart_html(chart_def: Dict[str, Any], canvas_id: str, width: int = 400, height: int = 300) -> str:
        """
        Create HTML for a chart
        
        Args:
            chart_def: Chart definition
            canvas_id: ID for the canvas element
            width: Canvas width
            height: Canvas height
            
        Returns:
            HTML string
        """
        chart_json = json.dumps(chart_def)
        
        return f"""
        <div style="width: {width}px; height: {height}px; margin: 20px auto;">
            <canvas id="{canvas_id}"></canvas>
        </div>
        <script>
            (function() {{
                var ctx = document.getElementById('{canvas_id}').getContext('2d');
                var chart = new Chart(ctx, {chart_json});
            }})();
        </script>
        """
