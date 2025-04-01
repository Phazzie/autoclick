"""Tests for the AdapterFactory class."""
import unittest
from unittest.mock import MagicMock, patch

from src.core.workflow.workflow_service_new import WorkflowService
from src.core.variables.variable_storage import VariableStorage
from src.core.conditions.condition_factory_new import ConditionFactory
from src.core.data.data_source_manager import DataSourceManager
from src.core.errors.error_manager import ErrorManager
from src.core.loops.loop_factory import LoopFactory
from src.core.reporting.reporting_service import ReportingService
from src.core.credentials.credential_manager import CredentialManager

from src.ui.adapters.factory.adapter_factory import AdapterFactory
from src.ui.adapters.impl.workflow_adapter import WorkflowAdapter
from src.ui.adapters.impl.variable_adapter import VariableAdapter
from src.ui.adapters.impl.condition_adapter import ConditionAdapter
from src.ui.adapters.impl.data_source_adapter import DataSourceAdapter
from src.ui.adapters.impl.error_adapter import ErrorAdapter
from src.ui.adapters.impl.loop_adapter import LoopAdapter
from src.ui.adapters.impl.reporting_adapter import ReportingAdapter
from src.ui.adapters.impl.credential_adapter import CredentialAdapter


class TestAdapterFactory(unittest.TestCase):
    """Test cases for the AdapterFactory class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Reset the singleton instance
        AdapterFactory._instance = None
        
        # Create a new factory
        self.factory = AdapterFactory()
    
    def test_singleton_pattern(self):
        """Test that the factory follows the singleton pattern."""
        # Create another factory
        factory2 = AdapterFactory()
        
        # Check that they are the same instance
        self.assertIs(self.factory, factory2)
        
        # Check that get_instance returns the same instance
        factory3 = AdapterFactory.get_instance()
        self.assertIs(self.factory, factory3)
    
    def test_get_workflow_adapter(self):
        """Test getting a workflow adapter."""
        # Act
        adapter = self.factory.get_workflow_adapter()
        
        # Assert
        self.assertIsInstance(adapter, WorkflowAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_workflow_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_workflow_adapter_with_service(self):
        """Test getting a workflow adapter with a custom service."""
        # Arrange
        mock_service = MagicMock(spec=WorkflowService)
        
        # Act
        adapter = self.factory.get_workflow_adapter(mock_service)
        
        # Assert
        self.assertIsInstance(adapter, WorkflowAdapter)
        
        # Check that a new instance is returned when a service is provided
        adapter2 = self.factory.get_workflow_adapter()
        self.assertIs(adapter, adapter2)
        
        # Check that a new instance is returned when a different service is provided
        mock_service2 = MagicMock(spec=WorkflowService)
        adapter3 = self.factory.get_workflow_adapter(mock_service2)
        self.assertIsNot(adapter, adapter3)
    
    def test_get_variable_adapter(self):
        """Test getting a variable adapter."""
        # Act
        adapter = self.factory.get_variable_adapter()
        
        # Assert
        self.assertIsInstance(adapter, VariableAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_variable_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_condition_adapter(self):
        """Test getting a condition adapter."""
        # Act
        adapter = self.factory.get_condition_adapter()
        
        # Assert
        self.assertIsInstance(adapter, ConditionAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_condition_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_data_source_adapter(self):
        """Test getting a data source adapter."""
        # Act
        adapter = self.factory.get_data_source_adapter()
        
        # Assert
        self.assertIsInstance(adapter, DataSourceAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_data_source_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_error_adapter(self):
        """Test getting an error adapter."""
        # Act
        adapter = self.factory.get_error_adapter()
        
        # Assert
        self.assertIsInstance(adapter, ErrorAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_error_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_loop_adapter(self):
        """Test getting a loop adapter."""
        # Act
        adapter = self.factory.get_loop_adapter()
        
        # Assert
        self.assertIsInstance(adapter, LoopAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_loop_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_reporting_adapter(self):
        """Test getting a reporting adapter."""
        # Act
        adapter = self.factory.get_reporting_adapter()
        
        # Assert
        self.assertIsInstance(adapter, ReportingAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_reporting_adapter()
        self.assertIs(adapter, adapter2)
    
    def test_get_credential_adapter(self):
        """Test getting a credential adapter."""
        # Act
        adapter = self.factory.get_credential_adapter()
        
        # Assert
        self.assertIsInstance(adapter, CredentialAdapter)
        
        # Check that the same instance is returned
        adapter2 = self.factory.get_credential_adapter()
        self.assertIs(adapter, adapter2)


if __name__ == "__main__":
    unittest.main()
