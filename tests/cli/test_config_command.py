"""Tests for the config command handler"""
# pylint: disable=redefined-outer-name
import argparse
import json
import os
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from src.cli.commands.config import config_command, load_config, save_config


@pytest.fixture
def mock_config_file(tmp_path):
    """Create a mock config file"""
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps({"browser": "chrome", "headless": True}))
    return config_file


@pytest.fixture
def mock_args():
    """Return mock command-line arguments"""
    return argparse.Namespace()


@patch("src.cli.commands.config.DEFAULT_CONFIG_PATH")
def test_load_config(mock_config_path, mock_config_file):
    """Test loading configuration from file"""
    # Set the mock config path
    mock_config_path.exists.return_value = True
    mock_config_path.__str__.return_value = str(mock_config_file)
    
    # Load the config
    config = load_config()
    
    # Verify the config was loaded correctly
    assert config == {"browser": "chrome", "headless": True}


@patch("src.cli.commands.config.DEFAULT_CONFIG_PATH")
def test_save_config(mock_config_path, tmp_path):
    """Test saving configuration to file"""
    # Create a temporary file for the config
    config_file = tmp_path / "config.json"
    
    # Set the mock config path
    mock_config_path.__str__.return_value = str(config_file)
    mock_config_path.parent = tmp_path
    
    # Save a config
    config = {"browser": "firefox", "headless": False}
    result = save_config(config)
    
    # Verify the result
    assert result is True
    
    # Verify the config was saved correctly
    saved_config = json.loads(config_file.read_text())
    assert saved_config == config


@patch("src.cli.commands.config.load_config")
def test_config_show_command(mock_load_config, mock_args, capsys):
    """Test the config show command"""
    # Set up the mock
    mock_load_config.return_value = {"browser": "chrome", "headless": True}
    
    # Set up the args
    mock_args.subcommand = "show"
    
    # Call the command handler
    result = config_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify the output
    captured = capsys.readouterr()
    assert "browser" in captured.out
    assert "chrome" in captured.out
    assert "headless" in captured.out
    assert "true" in captured.out.lower()


@patch("src.cli.commands.config.load_config")
@patch("src.cli.commands.config.save_config")
def test_config_set_command(mock_save_config, mock_load_config, mock_args):
    """Test the config set command"""
    # Set up the mocks
    mock_load_config.return_value = {"browser": "chrome"}
    mock_save_config.return_value = True
    
    # Set up the args
    mock_args.subcommand = "set"
    mock_args.key = "headless"
    mock_args.value = "true"
    
    # Call the command handler
    result = config_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify save_config was called with the updated config
    mock_save_config.assert_called_once()
    saved_config = mock_save_config.call_args[0][0]
    assert saved_config["browser"] == "chrome"
    assert saved_config["headless"] is True


@patch("src.cli.commands.config.load_config")
def test_config_get_command(mock_load_config, mock_args, capsys):
    """Test the config get command"""
    # Set up the mock
    mock_load_config.return_value = {"browser": "chrome", "headless": True}
    
    # Set up the args
    mock_args.subcommand = "get"
    mock_args.key = "browser"
    
    # Call the command handler
    result = config_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify the output
    captured = capsys.readouterr()
    assert "chrome" in captured.out


@patch("src.cli.commands.config.save_config")
def test_config_import_command(mock_save_config, mock_args, mock_config_file):
    """Test the config import command"""
    # Set up the mock
    mock_save_config.return_value = True
    
    # Set up the args
    mock_args.subcommand = "import"
    mock_args.file = str(mock_config_file)
    
    # Call the command handler
    result = config_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify save_config was called with the imported config
    mock_save_config.assert_called_once()
    saved_config = mock_save_config.call_args[0][0]
    assert saved_config["browser"] == "chrome"
    assert saved_config["headless"] is True


@patch("src.cli.commands.config.load_config")
def test_config_export_command(mock_load_config, mock_args, tmp_path):
    """Test the config export command"""
    # Set up the mock
    mock_load_config.return_value = {"browser": "chrome", "headless": True}
    
    # Create a temporary file for the export
    export_file = tmp_path / "export.json"
    
    # Set up the args
    mock_args.subcommand = "export"
    mock_args.file = str(export_file)
    
    # Call the command handler
    result = config_command(mock_args)
    
    # Verify the result
    assert result == 0
    
    # Verify the config was exported correctly
    exported_config = json.loads(export_file.read_text())
    assert exported_config["browser"] == "chrome"
    assert exported_config["headless"] is True
