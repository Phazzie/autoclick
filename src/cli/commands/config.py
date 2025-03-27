"""Config command handler"""
import argparse
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any


# Default configuration file path
DEFAULT_CONFIG_PATH = Path.home() / ".autoclick" / "config.json"


def load_config() -> Dict[str, Any]:
    """
    Load configuration from file
    
    Returns:
        Configuration dictionary
    """
    if not DEFAULT_CONFIG_PATH.exists():
        return {}
    
    try:
        with open(DEFAULT_CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading configuration: {str(e)}")
        return {}


def save_config(config: Dict[str, Any]) -> bool:
    """
    Save configuration to file
    
    Args:
        config: Configuration dictionary
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure the directory exists
        DEFAULT_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        with open(DEFAULT_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving configuration: {str(e)}")
        return False


def config_command(args: argparse.Namespace) -> int:
    """
    Handle the config command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    
    # If no subcommand is specified, show help
    if not hasattr(args, "subcommand") or not args.subcommand:
        logger.error("No subcommand specified")
        return 2
    
    try:
        # Handle the show subcommand
        if args.subcommand == "show":
            config = load_config()
            if not config:
                print("No configuration found")
            else:
                print(json.dumps(config, indent=2))
        
        # Handle the set subcommand
        elif args.subcommand == "set":
            config = load_config()
            
            # Parse the key and value
            key = args.key
            value = args.value
            
            # Try to convert the value to the appropriate type
            try:
                # Try to convert to int
                value = int(value)
            except ValueError:
                try:
                    # Try to convert to float
                    value = float(value)
                except ValueError:
                    # Try to convert to bool
                    if value.lower() in ("true", "yes", "1"):
                        value = True
                    elif value.lower() in ("false", "no", "0"):
                        value = False
            
            # Set the value
            config[key] = value
            
            # Save the configuration
            if save_config(config):
                logger.info(f"Set {key} = {value}")
            else:
                logger.error("Failed to save configuration")
                return 3
        
        # Handle the get subcommand
        elif args.subcommand == "get":
            config = load_config()
            key = args.key
            
            if key in config:
                print(config[key])
            else:
                logger.error(f"Key not found: {key}")
                return 2
        
        # Handle the import subcommand
        elif args.subcommand == "import":
            try:
                with open(args.file, "r") as f:
                    imported_config = json.load(f)
                
                if not isinstance(imported_config, dict):
                    logger.error("Invalid configuration format")
                    return 3
                
                # Save the imported configuration
                if save_config(imported_config):
                    logger.info(f"Imported configuration from {args.file}")
                else:
                    logger.error("Failed to save configuration")
                    return 3
            except Exception as e:
                logger.error(f"Error importing configuration: {str(e)}")
                return 3
        
        # Handle the export subcommand
        elif args.subcommand == "export":
            config = load_config()
            
            try:
                with open(args.file, "w") as f:
                    json.dump(config, f, indent=2)
                logger.info(f"Exported configuration to {args.file}")
            except Exception as e:
                logger.error(f"Error exporting configuration: {str(e)}")
                return 3
        
        else:
            logger.error(f"Unknown subcommand: {args.subcommand}")
            return 2
        
        return 0
    
    except Exception as e:
        logger.error(f"Error in config command: {str(e)}")
        return 1
