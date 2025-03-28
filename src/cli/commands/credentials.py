"""Credentials command handler"""
import argparse
import getpass
import logging
import os
from pathlib import Path
from typing import Dict, Any

from src.core.credentials_manager import CredentialsManager


def get_credentials_manager() -> CredentialsManager:
    """
    Get a configured credentials manager
    
    Returns:
        Configured credentials manager
    """
    # Default credentials file path
    credentials_path = Path.home() / ".autoclick" / "credentials.json"
    
    # Ensure the directory exists
    credentials_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Get the encryption key from environment or generate one
    encryption_key = os.environ.get("AUTOCLICK_ENCRYPTION_KEY", "default_key")
    
    # Create the configuration
    config = {
        "storage_path": str(credentials_path),
        "encryption_key": encryption_key,
    }
    
    # Create and return the credentials manager
    return CredentialsManager(config)


def credentials_command(args: argparse.Namespace) -> int:
    """
    Handle the credentials command
    
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
        # Get the credentials manager
        manager = get_credentials_manager()
        
        # Handle the add subcommand
        if args.subcommand == "add":
            site = args.site
            username = args.username
            password = args.password
            
            # Save the credentials
            manager.save(site, {
                "username": username,
                "password": password,
            })
            
            logger.info(f"Added credentials for {site}")
        
        # Handle the get subcommand
        elif args.subcommand == "get":
            site = args.site
            
            # Load the credentials
            credentials = manager.load(site)
            
            if credentials:
                print(f"Site: {site}")
                print(f"Username: {credentials.get('username', '')}")
                print(f"Password: {'*' * len(credentials.get('password', ''))}")
            else:
                logger.error(f"No credentials found for {site}")
                return 2
        
        # Handle the list subcommand
        elif args.subcommand == "list":
            # List all keys
            keys = manager.list_keys()
            
            if keys:
                print("Stored credentials:")
                for key in keys:
                    print(f"- {key}")
            else:
                print("No credentials found")
        
        # Handle the remove subcommand
        elif args.subcommand == "remove":
            site = args.site
            
            # Check if the site exists
            if site not in manager.list_keys():
                logger.error(f"No credentials found for {site}")
                return 2
            
            # Delete the credentials
            manager.delete(site)
            
            logger.info(f"Removed credentials for {site}")
        
        else:
            logger.error(f"Unknown subcommand: {args.subcommand}")
            return 2
        
        return 0
    
    except Exception as e:
        logger.error(f"Error in credentials command: {str(e)}")
        return 1
