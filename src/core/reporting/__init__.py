"""
Reporting system for AUTOCLICK.

This module provides a comprehensive reporting system with strict adherence to
Single Responsibility Principle (SRP) and other SOLID principles.
"""

from src.core.reporting.report_interface import ReportInterface, ReportMetadata
from src.core.reporting.base_report import BaseReport
from src.core.reporting.execution_report import ExecutionReport
from src.core.reporting.test_case_report import TestCaseReport
from src.core.reporting.summary_report import SummaryReport
from src.core.reporting.report_factory import ReportFactory
from src.core.reporting.report_manager import ReportManager
from src.core.reporting.report_storage import ReportStorage
from src.core.reporting.report_formatter import ReportFormatter
from src.core.reporting.report_service import ReportService

__all__ = [
    'ReportInterface',
    'ReportMetadata',
    'BaseReport',
    'ExecutionReport',
    'TestCaseReport',
    'SummaryReport',
    'ReportFactory',
    'ReportManager',
    'ReportStorage',
    'ReportFormatter',
    'ReportService'
]
