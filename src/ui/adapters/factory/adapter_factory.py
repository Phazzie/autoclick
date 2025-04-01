"""
Adapter factory implementation.

This module provides a factory for creating adapter instances.
"""
from typing import Optional

from src.core.workflow.workflow_service_new import WorkflowService
from src.core.variables.variable_storage import VariableStorage
from src.core.conditions.condition_factory_new import ConditionFactory
from src.core.data.data_source_manager import DataSourceManager
from src.core.errors.error_manager import ErrorManager
from src.core.loops.loop_factory import LoopFactory
from src.core.reporting.reporting_service import ReportingService
from src.core.credentials.credential_manager import CredentialManager

from src.ui.adapters.interfaces.iworkflow_adapter import IWorkflowAdapter
from src.ui.adapters.interfaces.ivariable_adapter import IVariableAdapter
from src.ui.adapters.interfaces.icondition_adapter import IConditionAdapter
from src.ui.adapters.interfaces.idata_source_adapter import IDataSourceAdapter
from src.ui.adapters.interfaces.ierror_adapter import IErrorAdapter
from src.ui.adapters.interfaces.iloop_adapter import ILoopAdapter
from src.ui.adapters.interfaces.ireporting_adapter import IReportingAdapter
from src.ui.adapters.interfaces.icredential_adapter import ICredentialAdapter

from src.ui.adapters.impl.workflow_adapter import WorkflowAdapter
from src.ui.adapters.impl.variable_adapter import VariableAdapter
from src.ui.adapters.impl.condition_adapter import ConditionAdapter
from src.ui.adapters.impl.data_source_adapter import DataSourceAdapter
from src.ui.adapters.impl.error_adapter import ErrorAdapter
from src.ui.adapters.impl.loop_adapter import LoopAdapter
from src.ui.adapters.impl.reporting_adapter import ReportingAdapter
from src.ui.adapters.impl.credential_adapter import CredentialAdapter


class AdapterFactory:
    """Factory for creating adapter instances."""
    
    _instance: Optional['AdapterFactory'] = None
    
    def __new__(cls) -> 'AdapterFactory':
        """Create a new instance or return the existing one (singleton pattern)."""
        if cls._instance is None:
            cls._instance = super(AdapterFactory, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize the factory."""
        # Initialize cached adapters
        self._workflow_adapter: Optional[IWorkflowAdapter] = None
        self._variable_adapter: Optional[IVariableAdapter] = None
        self._condition_adapter: Optional[IConditionAdapter] = None
        self._data_source_adapter: Optional[IDataSourceAdapter] = None
        self._error_adapter: Optional[IErrorAdapter] = None
        self._loop_adapter: Optional[ILoopAdapter] = None
        self._reporting_adapter: Optional[IReportingAdapter] = None
        self._credential_adapter: Optional[ICredentialAdapter] = None
    
    @classmethod
    def get_instance(cls) -> 'AdapterFactory':
        """Get the singleton instance of the factory."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get_workflow_adapter(self, workflow_service: Optional[WorkflowService] = None) -> IWorkflowAdapter:
        """
        Get a workflow adapter.
        
        Args:
            workflow_service: Optional workflow service to use
            
        Returns:
            Workflow adapter instance
        """
        if self._workflow_adapter is None or workflow_service is not None:
            self._workflow_adapter = WorkflowAdapter(workflow_service)
        return self._workflow_adapter
    
    def get_variable_adapter(self, variable_storage: Optional[VariableStorage] = None) -> IVariableAdapter:
        """
        Get a variable adapter.
        
        Args:
            variable_storage: Optional variable storage to use
            
        Returns:
            Variable adapter instance
        """
        if self._variable_adapter is None or variable_storage is not None:
            self._variable_adapter = VariableAdapter(variable_storage)
        return self._variable_adapter
    
    def get_condition_adapter(self, condition_factory: Optional[ConditionFactory] = None) -> IConditionAdapter:
        """
        Get a condition adapter.
        
        Args:
            condition_factory: Optional condition factory to use
            
        Returns:
            Condition adapter instance
        """
        if self._condition_adapter is None or condition_factory is not None:
            self._condition_adapter = ConditionAdapter(condition_factory)
        return self._condition_adapter
    
    def get_data_source_adapter(self, data_source_manager: Optional[DataSourceManager] = None) -> IDataSourceAdapter:
        """
        Get a data source adapter.
        
        Args:
            data_source_manager: Optional data source manager to use
            
        Returns:
            Data source adapter instance
        """
        if self._data_source_adapter is None or data_source_manager is not None:
            self._data_source_adapter = DataSourceAdapter(data_source_manager)
        return self._data_source_adapter
    
    def get_error_adapter(self, error_manager: Optional[ErrorManager] = None) -> IErrorAdapter:
        """
        Get an error adapter.
        
        Args:
            error_manager: Optional error manager to use
            
        Returns:
            Error adapter instance
        """
        if self._error_adapter is None or error_manager is not None:
            self._error_adapter = ErrorAdapter(error_manager)
        return self._error_adapter
    
    def get_loop_adapter(self, loop_factory: Optional[LoopFactory] = None) -> ILoopAdapter:
        """
        Get a loop adapter.
        
        Args:
            loop_factory: Optional loop factory to use
            
        Returns:
            Loop adapter instance
        """
        if self._loop_adapter is None or loop_factory is not None:
            self._loop_adapter = LoopAdapter(loop_factory)
        return self._loop_adapter
    
    def get_reporting_adapter(self, reporting_service: Optional[ReportingService] = None) -> IReportingAdapter:
        """
        Get a reporting adapter.
        
        Args:
            reporting_service: Optional reporting service to use
            
        Returns:
            Reporting adapter instance
        """
        if self._reporting_adapter is None or reporting_service is not None:
            self._reporting_adapter = ReportingAdapter(reporting_service)
        return self._reporting_adapter
    
    def get_credential_adapter(self, credential_manager: Optional[CredentialManager] = None) -> ICredentialAdapter:
        """
        Get a credential adapter.
        
        Args:
            credential_manager: Optional credential manager to use
            
        Returns:
            Credential adapter instance
        """
        if self._credential_adapter is None or credential_manager is not None:
            self._credential_adapter = CredentialAdapter(credential_manager)
        return self._credential_adapter
