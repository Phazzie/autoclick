"""Tests for the sequence runner"""
# pylint: disable=redefined-outer-name
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import MagicMock

import pytest

from src.core.interfaces import RunnerInterface, AutomationInterface


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
def mock_scripts(tmp_path: Path) -> List[Path]:
    """Create mock script files for testing"""
    script_dir = tmp_path / "scripts"
    script_dir.mkdir(exist_ok=True)
    
    scripts = []
    for i in range(3):
        script_path = script_dir / f"test_script_{i}.py"
        script_path.write_text(
            f"""
            def run(driver):
                driver.get("https://example.com/{i}")
                return {{"status": "success", "script": {i}}}
            """
        )
        scripts.append(script_path)
    
    return scripts


@pytest.fixture
def mock_automation() -> AutomationInterface:
    """Return a mock automation interface for testing"""
    mock = MagicMock(spec=AutomationInterface)
    mock.execute.side_effect = lambda script: {"status": "success", "script": str(script)}
    return mock


def test_sequence_runner_implements_interface():
    """Test that SequenceRunner implements the RunnerInterface"""
    # This will fail until we implement the SequenceRunner class
    from src.core.sequence_runner import SequenceRunner
    
    # Check that SequenceRunner is a subclass of RunnerInterface
    assert issubclass(SequenceRunner, RunnerInterface)


def test_sequence_runner_initialization(mock_config):
    """Test that SequenceRunner initializes correctly"""
    # This will fail until we implement the SequenceRunner class
    from src.core.sequence_runner import SequenceRunner
    
    # Create an instance of SequenceRunner
    runner = SequenceRunner()
    
    # Initialize with config
    runner.initialize(mock_config)
    
    # Check that the config was stored
    assert runner.config == mock_config


def test_sequence_runner_run(mock_automation, mock_scripts, mock_config):
    """Test that SequenceRunner can run scripts in sequence"""
    # This will fail until we implement the SequenceRunner class
    from src.core.sequence_runner import SequenceRunner
    
    # Create an instance of SequenceRunner
    runner = SequenceRunner()
    
    # Initialize with config
    runner.initialize(mock_config)
    
    # Run the scripts
    results = runner.run(mock_automation, mock_scripts)
    
    # Check that the automation was called for each script
    assert mock_automation.execute.call_count == len(mock_scripts)
    
    # Check that the results contain an entry for each script
    assert len(results["results"]) == len(mock_scripts)
    
    # Check that all scripts were successful
    for result in results["results"]:
        assert result["status"] == "success"


def test_sequence_runner_stop():
    """Test that SequenceRunner can stop execution"""
    # This will fail until we implement the SequenceRunner class
    from src.core.sequence_runner import SequenceRunner
    
    # Create an instance of SequenceRunner
    runner = SequenceRunner()
    
    # Set a flag to indicate that execution is in progress
    runner.running = True
    
    # Stop the execution
    runner.stop()
    
    # Check that the flag was reset
    assert not runner.running
