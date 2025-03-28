"""Tests for plugin interfaces"""
# pylint: disable=redefined-outer-name
from typing import Dict, Any
import pytest

from src.plugins.interfaces import (
    PluginInterface,
    AutomationPluginInterface,
    ReporterPluginInterface,
    StoragePluginInterface
)


def test_plugin_interface_methods():
    """Test that PluginInterface has the required methods"""
    # Check that the interface has the required methods
    assert hasattr(PluginInterface, "initialize")
    assert hasattr(PluginInterface, "get_info")
    assert hasattr(PluginInterface, "cleanup")


def test_automation_plugin_interface_methods():
    """Test that AutomationPluginInterface has the required methods"""
    # Check that the interface inherits from PluginInterface
    assert issubclass(AutomationPluginInterface, PluginInterface)
    
    # Check that the interface has the required methods
    assert hasattr(AutomationPluginInterface, "execute")
    assert hasattr(AutomationPluginInterface, "get_capabilities")


def test_reporter_plugin_interface_methods():
    """Test that ReporterPluginInterface has the required methods"""
    # Check that the interface inherits from PluginInterface
    assert issubclass(ReporterPluginInterface, PluginInterface)
    
    # Check that the interface has the required methods
    assert hasattr(ReporterPluginInterface, "generate_report")
    assert hasattr(ReporterPluginInterface, "get_supported_formats")


def test_storage_plugin_interface_methods():
    """Test that StoragePluginInterface has the required methods"""
    # Check that the interface inherits from PluginInterface
    assert issubclass(StoragePluginInterface, PluginInterface)
    
    # Check that the interface has the required methods
    assert hasattr(StoragePluginInterface, "save")
    assert hasattr(StoragePluginInterface, "load")
    assert hasattr(StoragePluginInterface, "delete")
    assert hasattr(StoragePluginInterface, "list")
