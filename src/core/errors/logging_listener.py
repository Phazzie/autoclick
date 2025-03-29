"""Error logging listener for the automation system"""
import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional, TextIO

from src.core.errors.error_listener import ErrorListener, ErrorEvent


class LoggingErrorListener(ErrorListener):
    """Error listener that logs errors to a logger"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        """
        Initialize the logging error listener
        
        Args:
            logger: Logger to use (creates a new one if None)
        """
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        
    def on_error(self, event: ErrorEvent) -> bool:
        """
        Log the error event
        
        Args:
            event: Error event containing the error and context
            
        Returns:
            False (error not handled, just logged)
        """
        error = event.error
        
        # Log the error with appropriate severity
        if error.severity.name == "FATAL":
            self.logger.critical(f"FATAL ERROR: {error}", exc_info=error.exception)
        elif error.severity.name == "CRITICAL":
            self.logger.critical(f"CRITICAL ERROR: {error}", exc_info=error.exception)
        elif error.severity.name == "ERROR":
            self.logger.error(f"ERROR: {error}", exc_info=error.exception)
        elif error.severity.name == "WARNING":
            self.logger.warning(f"WARNING: {error}")
        else:
            self.logger.info(f"INFO: {error}")
            
        # Return False to indicate the error was not handled
        return False


class FileErrorListener(ErrorListener):
    """Error listener that logs errors to a file"""
    
    def __init__(self, file_path: str, append: bool = True):
        """
        Initialize the file error listener
        
        Args:
            file_path: Path to the log file
            append: Whether to append to the file (True) or overwrite it (False)
        """
        self.file_path = file_path
        self.append = append
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Create or truncate the file
        mode = "a" if append else "w"
        try:
            with open(file_path, mode) as f:
                if not append:
                    f.write("# Error Log\n")
                    f.write(f"# Created: {datetime.now().isoformat()}\n\n")
        except Exception as e:
            self.logger.error(f"Failed to initialize error log file: {str(e)}")
        
    def on_error(self, event: ErrorEvent) -> bool:
        """
        Log the error event to the file
        
        Args:
            event: Error event containing the error and context
            
        Returns:
            False (error not handled, just logged)
        """
        try:
            # Convert the event to a dictionary
            event_dict = event.to_dict()
            
            # Add a timestamp for this log entry
            event_dict["log_timestamp"] = datetime.now().isoformat()
            
            # Write the event to the file
            with open(self.file_path, "a") as f:
                f.write(json.dumps(event_dict) + "\n")
                
            return False
        except Exception as e:
            self.logger.error(f"Failed to log error to file: {str(e)}")
            return False
