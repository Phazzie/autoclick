"""Integration tests for automation engine with runners"""
# pylint: disable=redefined-outer-name
import os
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import MagicMock, patch
import pytest

from src.core.automation_engine import AutomationEngine
from src.core.sequence_runner import SequenceRunner
from src.core.parallel_runner import ParallelRunner


@pytest.fixture
def test_scripts_dir(tmp_path) -> Path:
    """Create test scripts for testing"""
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()

    # Create a simple script that returns success
    success_script = scripts_dir / "success_script.py"
    success_script.write_text("""
def run(driver):
    # This is a mock script that always succeeds
    return {
        "status": "success",
        "message": "Success script executed"
    }
""")

    # Create a script that returns an error
    error_script = scripts_dir / "error_script.py"
    error_script.write_text("""
def run(driver):
    # This is a mock script that always fails
    raise ValueError("Simulated error")
""")

    # Create a script that takes some time
    slow_script = scripts_dir / "slow_script.py"
    slow_script.write_text("""
import time

def run(driver):
    # This is a mock script that takes some time
    time.sleep(0.5)
    return {
        "status": "success",
        "message": "Slow script executed"
    }
""")

    return scripts_dir


@pytest.fixture
def config() -> Dict[str, Any]:
    """Return a configuration for testing"""
    return {
        "browser": "chrome",
        "headless": True,
        "timeout": 5,
        "scripts_dir": "scripts",
        "max_workers": 3,
    }


@patch("src.core.webdriver_manager.WebDriverManager.initialize_driver")
def test_sequence_runner_with_automation_engine(mock_initialize_driver, test_scripts_dir, config):
    """Test that SequenceRunner works with AutomationEngine"""
    # Mock the WebDriver
    mock_driver = MagicMock()
    mock_initialize_driver.return_value = mock_driver

    # Create an instance of AutomationEngine
    engine = AutomationEngine()
    engine.initialize(config)

    # Create an instance of SequenceRunner
    runner = SequenceRunner()
    runner.initialize(config)

    # Get the script paths
    scripts = list(test_scripts_dir.glob("*.py"))

    # Run the scripts
    results = runner.run(engine, scripts)

    # Check that the results contain an entry for each script
    assert len(results["results"]) == len(scripts)

    # Check that the total count is correct
    assert results["total"] == len(scripts)

    # Check that the completed count is correct
    assert results["completed"] == len(scripts)

    # Check that at least one script succeeded
    success_count = sum(1 for result in results["results"] if result.get("status") == "success")
    assert success_count > 0

    # Check that at least one script failed
    error_count = sum(1 for result in results["results"] if result.get("status") == "error")
    assert error_count > 0


@patch("src.core.webdriver_manager.WebDriverManager.initialize_driver")
def test_parallel_runner_with_automation_engine(mock_initialize_driver, test_scripts_dir, config):
    """Test that ParallelRunner works with AutomationEngine"""
    # Mock the WebDriver
    mock_driver = MagicMock()
    mock_initialize_driver.return_value = mock_driver

    # Create an instance of AutomationEngine
    engine = AutomationEngine()
    engine.initialize(config)

    # Create an instance of ParallelRunner
    runner = ParallelRunner()
    runner.initialize(config)

    # Get the script paths
    scripts = list(test_scripts_dir.glob("*.py"))

    # Run the scripts
    results = runner.run(engine, scripts)

    # Check that the results contain an entry for each script
    assert len(results["results"]) == len(scripts)

    # Check that the total count is correct
    assert results["total"] == len(scripts)

    # Check that the completed count is correct
    assert results["completed"] == len(scripts)

    # Check that at least one script succeeded
    success_count = sum(1 for result in results["results"] if result.get("status") == "success")
    assert success_count > 0

    # Check that at least one script failed
    error_count = sum(1 for result in results["results"] if result.get("status") == "error")
    assert error_count > 0


def test_runner_stop_method():
    """Test that runners have a stop method that sets running to False"""
    # Test SequenceRunner
    sequence_runner = SequenceRunner()
    sequence_runner.running = True
    sequence_runner.stop()
    assert not sequence_runner.running

    # Test ParallelRunner
    parallel_runner = ParallelRunner()
    parallel_runner.running = True
    parallel_runner.stop()
    assert not parallel_runner.running
