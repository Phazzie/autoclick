"""Debugging utilities for development and troubleshooting"""
import logging
import sys
import traceback
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Dict, Optional


class DebugLogger:
    """Enhanced logging for debugging purposes"""

    def __init__(self, log_file: str = "debug.log"):
        self.logger = logging.getLogger("debug")
        self.logger.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)


def debug_trace(func):
    """Decorator for function call tracing"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("debug")
        try:
            logger.debug(f"Entering {func.__name__}")
            logger.debug(f"Args: {args}")
            logger.debug(f"Kwargs: {kwargs}")

            start_time = datetime.now()
            result = func(*args, **kwargs)
            execution_time = datetime.now() - start_time

            logger.debug(f"Exiting {func.__name__}")
            logger.debug(f"Execution time: {execution_time}")
            logger.debug(f"Result: {result}")
            return result

        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            raise

    return wrapper


class PerformanceProfiler:
    """Simple performance profiling utility"""

    def __init__(self):
        self.start_times: Dict[str, datetime] = {}
        self.measurements: Dict[str, float] = {}

    def start(self, name: str) -> None:
        """Start timing a section"""
        self.start_times[name] = datetime.now()

    def stop(self, name: str) -> float:
        """Stop timing a section and return duration"""
        if name not in self.start_times:
            raise ValueError(f"No start time found for {name}")

        duration = (datetime.now() - self.start_times[name]).total_seconds()
        self.measurements[name] = duration
        return duration

    def get_report(self) -> Dict[str, float]:
        """Get all measurements"""
        return self.measurements


def exception_handler(func):
    """Decorator for standardized exception handling"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger = logging.getLogger("debug")
            logger.error(f"Exception in {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())

            # Save detailed debug info
            debug_info = {
                "function": func.__name__,
                "args": args,
                "kwargs": kwargs,
                "exception": str(e),
                "traceback": traceback.format_exc(),
                "timestamp": datetime.now().isoformat(),
            }

            # Save to debug file
            debug_file = (
                Path("debug") / f"error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            )
            debug_file.parent.mkdir(exist_ok=True)
            debug_file.write_text(str(debug_info))

            raise

    return wrapper
