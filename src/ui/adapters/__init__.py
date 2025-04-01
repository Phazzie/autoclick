"""
UI adapters module.

This module provides adapters for UI components to interact with the core application.
SOLID: Each adapter follows the Interface Segregation Principle.
KISS: Simple delegation to backend components.
DRY: Avoids duplicating backend logic in UI.
"""
# Interfaces
from .interfaces.iworkflow_adapter import IWorkflowAdapter
from .interfaces.ivariable_adapter import IVariableAdapter
from .interfaces.icondition_adapter import IConditionAdapter
from .interfaces.idata_source_adapter import IDataSourceAdapter
from .interfaces.ierror_adapter import IErrorAdapter
from .interfaces.iloop_adapter import ILoopAdapter
from .interfaces.ireporting_adapter import IReportingAdapter
from .interfaces.icredential_adapter import ICredentialAdapter

# Implementations
from .impl.workflow_adapter import WorkflowAdapter
from .impl.variable_adapter import VariableAdapter
from .impl.condition_adapter import ConditionAdapter
from .impl.data_source_adapter import DataSourceAdapter
from .impl.error_adapter import ErrorAdapter
from .impl.loop_adapter import LoopAdapter
from .impl.reporting_adapter import ReportingAdapter
from .impl.credential_adapter import CredentialAdapter

# Factory
from .factory.adapter_factory import AdapterFactory

__all__ = [
    # Interfaces
    'IWorkflowAdapter',
    'IVariableAdapter',
    'IConditionAdapter',
    'IDataSourceAdapter',
    'IErrorAdapter',
    'ILoopAdapter',
    'IReportingAdapter',
    'ICredentialAdapter',

    # Implementations
    'WorkflowAdapter',
    'VariableAdapter',
    'ConditionAdapter',
    'DataSourceAdapter',
    'ErrorAdapter',
    'LoopAdapter',
    'ReportingAdapter',
    'CredentialAdapter',

    # Factory
    'AdapterFactory'
]
