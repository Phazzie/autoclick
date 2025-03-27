"""Main entry point for the AUTOCLICK CLI"""
import argparse
import logging
import sys
from typing import List, Optional

from src.version import __version__
from src.cli.commands import (
    run_command,
    config_command,
    credentials_command,
    plugins_command,
    report_command,
    interactive_command,
)


def setup_logging(verbose: bool = False, quiet: bool = False) -> None:
    """
    Set up logging configuration
    
    Args:
        verbose: Enable verbose output
        quiet: Suppress all output except errors
    """
    log_level = logging.INFO
    if verbose:
        log_level = logging.DEBUG
    elif quiet:
        log_level = logging.ERROR
    
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_parser() -> argparse.ArgumentParser:
    """
    Create the command-line argument parser
    
    Returns:
        Configured argument parser
    """
    # Create the main parser
    parser = argparse.ArgumentParser(
        prog="autoclick",
        description="AUTOCLICK - A streamlined, maintainable, and easily extensible web automation application",
        epilog="For more information, visit https://github.com/Phazzie/autoclick",
    )
    
    # Add global options
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true", help="Suppress all output except errors"
    )
    parser.add_argument(
        "--version", action="version", version=f"AUTOCLICK v{__version__}"
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Execute automation scripts")
    run_parser.add_argument("script_path", help="Path to the script or directory of scripts")
    run_parser.add_argument(
        "--browser", choices=["chrome", "firefox", "edge"], 
        default="chrome", help="Browser to use"
    )
    run_parser.add_argument(
        "--headless", action="store_true", help="Run in headless mode"
    )
    run_parser.add_argument(
        "--timeout", type=int, default=30, help="Set timeout in seconds"
    )
    run_parser.add_argument(
        "--config", help="Path to a configuration file"
    )
    run_parser.add_argument(
        "--parallel", action="store_true", help="Run scripts in parallel"
    )
    run_parser.add_argument(
        "--max-workers", type=int, default=4, help="Maximum number of parallel workers"
    )
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Manage configuration settings")
    config_subparsers = config_parser.add_subparsers(dest="subcommand", help="Config subcommand")
    
    # Config show
    config_show_parser = config_subparsers.add_parser("show", help="Show current configuration")
    
    # Config set
    config_set_parser = config_subparsers.add_parser("set", help="Set a configuration value")
    config_set_parser.add_argument("key", help="Configuration key")
    config_set_parser.add_argument("value", help="Configuration value")
    
    # Config get
    config_get_parser = config_subparsers.add_parser("get", help="Get a configuration value")
    config_get_parser.add_argument("key", help="Configuration key")
    
    # Config import
    config_import_parser = config_subparsers.add_parser("import", help="Import configuration from a file")
    config_import_parser.add_argument("file", help="Path to the configuration file")
    
    # Config export
    config_export_parser = config_subparsers.add_parser("export", help="Export configuration to a file")
    config_export_parser.add_argument("file", help="Path to the output file")
    
    # Credentials command
    credentials_parser = subparsers.add_parser("credentials", help="Manage stored credentials")
    credentials_subparsers = credentials_parser.add_subparsers(dest="subcommand", help="Credentials subcommand")
    
    # Credentials add
    credentials_add_parser = credentials_subparsers.add_parser("add", help="Add credentials")
    credentials_add_parser.add_argument("site", help="Site name")
    credentials_add_parser.add_argument("--username", required=True, help="Username")
    credentials_add_parser.add_argument("--password", required=True, help="Password")
    
    # Credentials get
    credentials_get_parser = credentials_subparsers.add_parser("get", help="Get credentials for a site")
    credentials_get_parser.add_argument("site", help="Site name")
    
    # Credentials list
    credentials_list_parser = credentials_subparsers.add_parser("list", help="List all stored credentials")
    
    # Credentials remove
    credentials_remove_parser = credentials_subparsers.add_parser("remove", help="Remove credentials for a site")
    credentials_remove_parser.add_argument("site", help="Site name")
    
    # Plugins command
    plugins_parser = subparsers.add_parser("plugins", help="Manage plugins")
    plugins_subparsers = plugins_parser.add_subparsers(dest="subcommand", help="Plugins subcommand")
    
    # Plugins list
    plugins_list_parser = plugins_subparsers.add_parser("list", help="List all installed plugins")
    
    # Plugins info
    plugins_info_parser = plugins_subparsers.add_parser("info", help="Show information about a plugin")
    plugins_info_parser.add_argument("plugin", help="Plugin name")
    
    # Plugins install
    plugins_install_parser = plugins_subparsers.add_parser("install", help="Install a plugin")
    plugins_install_parser.add_argument("plugin_path", help="Path to the plugin")
    
    # Plugins uninstall
    plugins_uninstall_parser = plugins_subparsers.add_parser("uninstall", help="Uninstall a plugin")
    plugins_uninstall_parser.add_argument("plugin", help="Plugin name")
    
    # Plugins enable
    plugins_enable_parser = plugins_subparsers.add_parser("enable", help="Enable a plugin")
    plugins_enable_parser.add_argument("plugin", help="Plugin name")
    
    # Plugins disable
    plugins_disable_parser = plugins_subparsers.add_parser("disable", help="Disable a plugin")
    plugins_disable_parser.add_argument("plugin", help="Plugin name")
    
    # Report command
    report_parser = subparsers.add_parser("report", help="Generate and manage reports")
    report_subparsers = report_parser.add_subparsers(dest="subcommand", help="Report subcommand")
    
    # Report generate
    report_generate_parser = report_subparsers.add_parser("generate", help="Generate a report")
    report_generate_parser.add_argument(
        "--format", choices=["html", "json", "csv"], default="html", help="Report format"
    )
    
    # Report show
    report_show_parser = report_subparsers.add_parser("show", help="Show a specific report")
    report_show_parser.add_argument("report_id", help="Report ID or 'latest'")
    
    # Report list
    report_list_parser = report_subparsers.add_parser("list", help="List all reports")
    
    # Report export
    report_export_parser = report_subparsers.add_parser("export", help="Export a report to a file")
    report_export_parser.add_argument("report_id", help="Report ID or 'latest'")
    report_export_parser.add_argument("file", help="Path to the output file")
    
    # Interactive command
    interactive_parser = subparsers.add_parser("interactive", help="Start interactive shell")
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the CLI
    
    Args:
        args: Command-line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    # Set up logging
    setup_logging(verbose=parsed_args.verbose, quiet=parsed_args.quiet)
    
    # If no command is specified, show help
    if not parsed_args.command:
        parser.print_help()
        return 0
    
    try:
        # Dispatch to the appropriate command handler
        if parsed_args.command == "run":
            return run_command(parsed_args)
        elif parsed_args.command == "config":
            return config_command(parsed_args)
        elif parsed_args.command == "credentials":
            return credentials_command(parsed_args)
        elif parsed_args.command == "plugins":
            return plugins_command(parsed_args)
        elif parsed_args.command == "report":
            return report_command(parsed_args)
        elif parsed_args.command == "interactive":
            return interactive_command(parsed_args)
        else:
            parser.print_help()
            return 0
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        if parsed_args.verbose:
            logging.exception("Detailed error information:")
        return 1


if __name__ == "__main__":
    sys.exit(main())
