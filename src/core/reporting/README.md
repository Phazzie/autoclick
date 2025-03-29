# Reporting System

This module provides a comprehensive reporting system for the AUTOCLICK automation tool. The system follows SOLID principles, with a strong emphasis on the Single Responsibility Principle (SRP).

## Components

### 1. Report Interface (`report_interface.py`)

Defines the contract that all report implementations must follow. Contains:
- `ReportInterface`: Abstract base class for all reports
- `ReportMetadata`: Class for storing report metadata

### 2. Base Report (`base_report.py`)

Provides common functionality for all report types:
- Basic data collection
- Report generation with metadata
- Export to various formats (JSON, CSV, HTML, TXT)

### 3. Specific Report Types

- `ExecutionReport`: Detailed information about workflow execution
- `TestCaseReport`: Results of data-driven test execution
- `SummaryReport`: High-level overview of multiple workflow executions

### 4. Report Factory (`report_factory.py`)

Factory for creating different types of reports:
- Creates reports based on type
- Manages report type registration
- Provides access to available report types

### 5. Report Manager (`report_manager.py`)

Manages report instances:
- Creates reports using the factory
- Tracks created reports
- Provides filtering and retrieval of reports

### 6. Report Storage (`report_storage.py`)

Handles report persistence:
- Saves reports to disk in various formats
- Lists available report files
- Manages report file deletion

### 7. Report Formatter (`report_formatter.py`)

Formats report data for display:
- Creates summaries of reports
- Formats data as tables
- Extracts key metrics from reports

### 8. Report Service (`report_service.py`)

Coordinates the reporting process:
- Delegates to specialized components
- Provides a simplified interface for report generation
- Manages the full reporting lifecycle

## Usage Example

```python
from src.core.reporting.report_service import ReportService

# Create report service
report_service = ReportService(report_dir="reports")

# Generate an execution report
report_data = report_service.generate_report(
    report_type="execution",
    source=workflow,
    title="Workflow Execution Report",
    description="Detailed execution report",
    tags=["workflow", "execution"],
    save=True
)

# Get a report summary
report = report_service.report_manager.get_reports(report_type="execution")[0]
summary = report_service.get_report_summary(report)
print(summary)

# Extract key metrics
metrics = report_service.get_report_metrics(report)
print(metrics)
```

## Design Principles

This reporting system strictly follows these principles:

### Single Responsibility Principle (SRP)
Each class has exactly one responsibility:
- `ReportInterface`: Define the contract
- `BaseReport`: Provide common functionality
- `ExecutionReport`: Report on workflow execution
- `ReportFactory`: Create reports
- `ReportManager`: Manage report instances
- `ReportStorage`: Handle report persistence
- `ReportFormatter`: Format report data
- `ReportService`: Coordinate the reporting process

### Open/Closed Principle (OCP)
The system is open for extension but closed for modification:
- New report types can be added without changing existing code
- New export formats can be added by extending the base report

### Liskov Substitution Principle (LSP)
All report implementations can be used interchangeably:
- All reports implement the same interface
- The report manager works with any report type

### Interface Segregation Principle (ISP)
Interfaces are focused and minimal:
- `ReportInterface` defines only essential methods
- Specialized functionality is added in implementations

### Dependency Inversion Principle (DIP)
High-level components depend on abstractions:
- `ReportManager` depends on `ReportInterface`, not concrete implementations
- `ReportService` coordinates components through their interfaces
