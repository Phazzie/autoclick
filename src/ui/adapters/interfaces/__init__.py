"""
UI adapter interfaces.

This module exports interfaces for UI adapters.
"""
from .iworkflow_adapter import IWorkflowAdapter
from .ivariable_adapter import IVariableAdapter
from .icondition_adapter import IConditionAdapter
from .idata_source_adapter import IDataSourceAdapter
from .ierror_adapter import IErrorAdapter
from .iloop_adapter import ILoopAdapter
from .ireporting_adapter import IReportingAdapter
from .icredential_adapter import ICredentialAdapter

__all__ = [
    'IWorkflowAdapter',
    'IVariableAdapter',
    'IConditionAdapter',
    'IDataSourceAdapter',
    'IErrorAdapter',
    'ILoopAdapter',
    'IReportingAdapter',
    'ICredentialAdapter'
]
