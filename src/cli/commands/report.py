"""Report command handler"""
import argparse
import json
import logging
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.results_handler import ResultsHandler


def get_reports_dir() -> Path:
    """
    Get the reports directory
    
    Returns:
        Path to the reports directory
    """
    # Default reports directory
    reports_dir = Path.home() / ".autoclick" / "reports"
    
    # Ensure the directory exists
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    return reports_dir


def get_results_handler() -> ResultsHandler:
    """
    Get a configured results handler
    
    Returns:
        Configured results handler
    """
    # Get the reports directory
    reports_dir = get_reports_dir()
    
    # Create the configuration
    config = {
        "results_dir": str(reports_dir),
        "report_format": "json",
    }
    
    # Create and initialize the results handler
    handler = ResultsHandler()
    handler.initialize(config)
    
    return handler


def get_report_path(report_id: str) -> Optional[Path]:
    """
    Get the path to a report file
    
    Args:
        report_id: Report ID or 'latest'
        
    Returns:
        Path to the report file, or None if not found
    """
    reports_dir = get_reports_dir()
    
    if report_id == "latest":
        # Find the most recent report
        reports = list(reports_dir.glob("report_*.json"))
        if not reports:
            return None
        
        # Sort by modification time (newest first)
        reports.sort(key=lambda p: p.stat().st_mtime, reverse=True)
        return reports[0]
    else:
        # Check if the report exists
        report_path = reports_dir / f"report_{report_id}.json"
        if report_path.exists():
            return report_path
        
        # Try with .json extension if not provided
        if not report_id.endswith(".json"):
            report_path = reports_dir / f"report_{report_id}.json"
            if report_path.exists():
                return report_path
        
        return None


def report_command(args: argparse.Namespace) -> int:
    """
    Handle the report command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    
    # If no subcommand is specified, show help
    if not hasattr(args, "subcommand") or not args.subcommand:
        logger.error("No subcommand specified")
        return 2
    
    try:
        # Get the results handler
        handler = get_results_handler()
        
        # Handle the generate subcommand
        if args.subcommand == "generate":
            # Create a sample report (in a real scenario, this would use actual results)
            sample_data = {
                "results": [
                    {
                        "script": "sample_script.py",
                        "status": "success",
                        "duration": 1.5,
                        "timestamp": datetime.now().isoformat(),
                    }
                ]
            }
            
            # Generate the report
            handler.report(sample_data)
            
            logger.info("Generated report")
        
        # Handle the show subcommand
        elif args.subcommand == "show":
            report_path = get_report_path(args.report_id)
            
            if not report_path:
                logger.error(f"Report not found: {args.report_id}")
                return 2
            
            try:
                # Load and display the report
                with open(report_path, "r") as f:
                    report_data = json.load(f)
                
                print(f"Report: {report_path.name}")
                print(f"Timestamp: {report_data.get('timestamp', 'unknown')}")
                
                # Display summary
                summary = report_data.get("summary", {})
                if summary:
                    print("\nSummary:")
                    for key, value in summary.items():
                        print(f"  {key}: {value}")
                
                # Display results
                results = report_data.get("results", [])
                if results:
                    print("\nResults:")
                    for i, result in enumerate(results):
                        status = result.get("status", "unknown")
                        script = result.get("script", f"Script {i+1}")
                        duration = result.get("duration", 0)
                        message = result.get("message", "")
                        
                        print(f"  {script}: {status} ({duration:.2f}s)")
                        if message:
                            print(f"    Message: {message}")
            except Exception as e:
                logger.error(f"Error reading report: {str(e)}")
                return 3
        
        # Handle the list subcommand
        elif args.subcommand == "list":
            reports_dir = get_reports_dir()
            reports = list(reports_dir.glob("report_*.json"))
            
            if reports:
                print("Available reports:")
                # Sort by modification time (newest first)
                reports.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                
                for report in reports:
                    # Get the report ID from the filename
                    report_id = report.stem.replace("report_", "")
                    
                    # Get the modification time
                    mod_time = datetime.fromtimestamp(report.stat().st_mtime)
                    
                    print(f"- {report_id} ({mod_time.strftime('%Y-%m-%d %H:%M:%S')})")
            else:
                print("No reports found")
        
        # Handle the export subcommand
        elif args.subcommand == "export":
            report_path = get_report_path(args.report_id)
            
            if not report_path:
                logger.error(f"Report not found: {args.report_id}")
                return 2
            
            try:
                # Copy the report to the specified file
                shutil.copy(report_path, args.file)
                logger.info(f"Exported report to {args.file}")
            except Exception as e:
                logger.error(f"Error exporting report: {str(e)}")
                return 3
        
        else:
            logger.error(f"Unknown subcommand: {args.subcommand}")
            return 2
        
        return 0
    
    except Exception as e:
        logger.error(f"Error in report command: {str(e)}")
        return 1
