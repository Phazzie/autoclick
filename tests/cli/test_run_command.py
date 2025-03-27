"""Tests for the run command handler"""
# pylint: disable=redefined-outer-name
import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from src.cli.commands.run import run_command


@pytest.fixture
def mock_args():
    """Return mock command-line arguments"""
    args = argparse.Namespace()
    args.script_path = "test_script.py"
    args.browser = "chrome"
    args.headless = True
    args.timeout = 30
    args.config = None
    args.parallel = False
    args.max_workers = 4
    args.quiet = False
    args.verbose = False
    return args


@pytest.fixture
def mock_script_path(tmp_path):
    """Create a mock script file"""
    script_path = tmp_path / "test_script.py"
    script_path.write_text("def run(driver):\n    return {'status': 'success'}")
    return script_path


@patch("src.cli.commands.run.AutomationEngine")
@patch("src.cli.commands.run.SequenceRunner")
def test_run_command_with_single_script(mock_sequence_runner, mock_automation_engine, mock_args, mock_script_path):
    """Test running a single script"""
    # Update args to use the mock script path
    mock_args.script_path = str(mock_script_path)
    
    # Configure mocks
    mock_engine_instance = MagicMock()
    mock_automation_engine.return_value = mock_engine_instance
    
    mock_runner_instance = MagicMock()
    mock_sequence_runner.return_value = mock_runner_instance
    mock_runner_instance.run.return_value = {
        "results": [{"status": "success", "script": str(mock_script_path)}]
    }
    
    # Call the command handler
    result = run_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify the engine was initialized with the correct config
    mock_engine_instance.initialize.assert_called_once()
    config = mock_engine_instance.initialize.call_args[0][0]
    assert config["browser"] == "chrome"
    assert config["headless"] is True
    assert config["timeout"] == 30
    
    # Verify the runner was initialized and run
    mock_runner_instance.initialize.assert_called_once()
    mock_runner_instance.run.assert_called_once()


@patch("src.cli.commands.run.AutomationEngine")
@patch("src.cli.commands.run.ParallelRunner")
def test_run_command_with_parallel(mock_parallel_runner, mock_automation_engine, mock_args, mock_script_path):
    """Test running scripts in parallel"""
    # Update args to use the mock script path and enable parallel execution
    mock_args.script_path = str(mock_script_path)
    mock_args.parallel = True
    
    # Configure mocks
    mock_engine_instance = MagicMock()
    mock_automation_engine.return_value = mock_engine_instance
    
    mock_runner_instance = MagicMock()
    mock_parallel_runner.return_value = mock_runner_instance
    mock_runner_instance.run.return_value = {
        "results": [{"status": "success", "script": str(mock_script_path)}]
    }
    
    # Call the command handler
    result = run_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify the parallel runner was used
    mock_parallel_runner.assert_called_once()
    mock_runner_instance.initialize.assert_called_once()
    mock_runner_instance.run.assert_called_once()


@patch("src.cli.commands.run.AutomationEngine")
@patch("src.cli.commands.run.SequenceRunner")
def test_run_command_with_directory(mock_sequence_runner, mock_automation_engine, mock_args, tmp_path):
    """Test running scripts from a directory"""
    # Create multiple scripts in a directory
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    
    script1 = scripts_dir / "script1.py"
    script1.write_text("def run(driver):\n    return {'status': 'success'}")
    
    script2 = scripts_dir / "script2.py"
    script2.write_text("def run(driver):\n    return {'status': 'success'}")
    
    # Update args to use the scripts directory
    mock_args.script_path = str(scripts_dir)
    
    # Configure mocks
    mock_engine_instance = MagicMock()
    mock_automation_engine.return_value = mock_engine_instance
    
    mock_runner_instance = MagicMock()
    mock_sequence_runner.return_value = mock_runner_instance
    mock_runner_instance.run.return_value = {
        "results": [
            {"status": "success", "script": str(script1)},
            {"status": "success", "script": str(script2)}
        ]
    }
    
    # Call the command handler
    result = run_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify the runner was called with both scripts
    mock_runner_instance.run.assert_called_once()
    # The second argument to run should be a list of scripts
    scripts_arg = mock_runner_instance.run.call_args[0][1]
    assert len(scripts_arg) == 2
    assert all(isinstance(script, Path) for script in scripts_arg)


@patch("src.cli.commands.run.AutomationEngine")
@patch("src.cli.commands.run.SequenceRunner")
def test_run_command_with_errors(mock_sequence_runner, mock_automation_engine, mock_args, mock_script_path):
    """Test running a script that returns an error"""
    # Update args to use the mock script path
    mock_args.script_path = str(mock_script_path)
    
    # Configure mocks
    mock_engine_instance = MagicMock()
    mock_automation_engine.return_value = mock_engine_instance
    
    mock_runner_instance = MagicMock()
    mock_sequence_runner.return_value = mock_runner_instance
    mock_runner_instance.run.return_value = {
        "results": [{"status": "error", "script": str(mock_script_path), "message": "Test error"}]
    }
    
    # Call the command handler
    result = run_command(mock_args)
    
    # Verify the result indicates an error
    assert result == 4
