"""Tests for the automation engine"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
from typing import Dict, Any
from unittest.mock import MagicMock, patch

import pytest

from src.core.interfaces import AutomationInterface


@pytest.fixture
def mock_config() -> Dict[str, Any]:
    """Return a mock configuration for testing"""
    return {
        "browser": "chrome",
        "headless": True,
        "timeout": 5,
        "scripts_dir": "scripts",
    }


@pytest.fixture
def mock_script_path(tmp_path: Path) -> Path:
    """Create a mock script file for testing"""
    script_dir = tmp_path / "scripts"
    script_dir.mkdir(exist_ok=True)
    
    script_path = script_dir / "test_script.py"
    script_path.write_text(
        """
        def run(driver):
            driver.get("https://example.com")
            return {"status": "success"}
        """
    )
    return script_path


def test_automation_engine_implements_interface():
    """Test that AutomationEngine implements the AutomationInterface"""
    # This will fail until we implement the AutomationEngine class
    from src.core.automation_engine import AutomationEngine
    
    # Check that AutomationEngine is a subclass of AutomationInterface
    assert issubclass(AutomationEngine, AutomationInterface)


def test_automation_engine_initialization(mock_config):
    """Test that AutomationEngine initializes correctly"""
    # This will fail until we implement the AutomationEngine class
    from src.core.automation_engine import AutomationEngine
    
    # Create an instance of AutomationEngine
    engine = AutomationEngine()
    
    # Initialize with config
    engine.initialize(mock_config)
    
    # Check that the config was stored
    assert engine.config == mock_config
    
    # Check that the driver is None initially
    assert engine.driver is None


@patch("src.core.webdriver_manager.WebDriverManager")
def test_automation_engine_execute(mock_webdriver_manager, mock_config, mock_script_path):
    """Test that AutomationEngine can execute a script"""
    # This will fail until we implement the AutomationEngine class
    from src.core.automation_engine import AutomationEngine
    
    # Create a mock driver
    mock_driver = MagicMock()
    
    # Configure the mock WebDriverManager
    mock_webdriver_manager_instance = mock_webdriver_manager.return_value
    mock_webdriver_manager_instance.initialize_driver.return_value = mock_driver
    
    # Create an instance of AutomationEngine
    engine = AutomationEngine()
    
    # Initialize with config
    engine.initialize(mock_config)
    
    # Execute the script
    result = engine.execute(mock_script_path)
    
    # Check that the driver was initialized
    mock_webdriver_manager_instance.initialize_driver.assert_called_once()
    
    # Check that the result is a dictionary
    assert isinstance(result, dict)
    
    # Check that the driver was closed
    mock_webdriver_manager_instance.close.assert_called_once()


def test_automation_engine_cleanup():
    """Test that AutomationEngine cleans up resources"""
    # This will fail until we implement the AutomationEngine class
    from src.core.automation_engine import AutomationEngine
    
    # Create an instance of AutomationEngine
    engine = AutomationEngine()
    
    # Create a mock driver manager
    engine.driver_manager = MagicMock()
    
    # Call cleanup
    engine.cleanup()
    
    # Check that the driver was closed
    engine.driver_manager.close.assert_called_once()
