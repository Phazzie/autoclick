"""
Report storage with strict adherence to Single Responsibility Principle.
"""
import os
import logging
from typing import Optional
from datetime import datetime

from src.core.reporting.report_interface import ReportInterface


class ReportStorage:
    """
    Storage for report files.
    
    This class has the single responsibility of storing reports to disk.
    It does not handle report creation or management.
    """
    
    def __init__(self, report_dir: str = "reports"):
        """
        Initialize the report storage.
        
        Args:
            report_dir: Directory for storing reports
        """
        self.report_dir = report_dir
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create report directory if it doesn't exist
        os.makedirs(report_dir, exist_ok=True)
    
    def save_report(
        self,
        report: ReportInterface,
        format_type: str = "json",
        filename: Optional[str] = None
    ) -> str:
        """
        Save a report to disk.
        
        Args:
            report: The report to save
            format_type: Format to save as (e.g., 'json', 'html', 'csv', 'txt')
            filename: Optional filename (generated if not provided)
            
        Returns:
            Path to the saved report file
        """
        # Generate filename if not provided
        if filename is None:
            metadata = report.get_metadata()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_type = metadata.get("report_type", "report")
            filename = f"{report_type}_{timestamp}.{format_type}"
        
        # Ensure correct extension
        if not filename.endswith(f".{format_type}"):
            filename = f"{filename}.{format_type}"
        
        # Create full path
        file_path = os.path.join(self.report_dir, filename)
        
        # Export report to file
        report.export(format_type=format_type, destination=file_path)
        
        self.logger.info(f"Report saved to {file_path}")
        
        return file_path
    
    def list_reports(self, format_type: Optional[str] = None) -> list[str]:
        """
        List report files in the storage directory.
        
        Args:
            format_type: Optional format type to filter by (e.g., 'json', 'html')
            
        Returns:
            List of report file paths
        """
        if not os.path.exists(self.report_dir):
            return []
        
        files = os.listdir(self.report_dir)
        
        if format_type:
            files = [f for f in files if f.endswith(f".{format_type}")]
        
        return [os.path.join(self.report_dir, f) for f in files]
    
    def delete_report(self, file_path: str) -> bool:
        """
        Delete a report file.
        
        Args:
            file_path: Path to the report file
            
        Returns:
            True if the file was deleted, False otherwise
        """
        if not os.path.exists(file_path):
            self.logger.warning(f"Report file not found: {file_path}")
            return False
        
        try:
            os.remove(file_path)
            self.logger.info(f"Deleted report file: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to delete report file: {file_path} - {str(e)}")
            return False
    
    def clear_storage(self) -> int:
        """
        Delete all report files in the storage directory.
        
        Returns:
            Number of files deleted
        """
        if not os.path.exists(self.report_dir):
            return 0
        
        files = os.listdir(self.report_dir)
        deleted_count = 0
        
        for file in files:
            file_path = os.path.join(self.report_dir, file)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    deleted_count += 1
                except Exception as e:
                    self.logger.error(f"Failed to delete file: {file_path} - {str(e)}")
        
        self.logger.info(f"Cleared {deleted_count} report files from storage")
        return deleted_count
