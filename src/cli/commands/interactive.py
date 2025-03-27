"""Interactive command handler"""
import argparse
import cmd
import logging
import shlex
import sys
from typing import List, Optional

from src.cli.main import create_parser, main


class AutoClickShell(cmd.Cmd):
    """Interactive shell for AUTOCLICK"""
    
    intro = "Welcome to the AUTOCLICK interactive shell. Type help or ? to list commands."
    prompt = "autoclick> "
    
    def __init__(self, verbose: bool = False, quiet: bool = False):
        """
        Initialize the shell
        
        Args:
            verbose: Enable verbose output
            quiet: Suppress all output except errors
        """
        super().__init__()
        self.verbose = verbose
        self.quiet = quiet
        self.parser = create_parser()
    
    def default(self, line: str) -> bool:
        """
        Handle unknown commands
        
        Args:
            line: Command line
            
        Returns:
            True to continue, False to exit
        """
        print(f"Unknown command: {line}")
        return True
    
    def emptyline(self) -> bool:
        """
        Handle empty lines
        
        Returns:
            True to continue
        """
        return True
    
    def do_exit(self, arg: str) -> bool:
        """
        Exit the shell
        
        Args:
            arg: Command arguments
            
        Returns:
            False to exit
        """
        print("Exiting AUTOCLICK shell")
        return False
    
    def do_quit(self, arg: str) -> bool:
        """
        Quit the shell
        
        Args:
            arg: Command arguments
            
        Returns:
            False to exit
        """
        return self.do_exit(arg)
    
    def do_EOF(self, arg: str) -> bool:
        """
        Handle EOF (Ctrl+D)
        
        Args:
            arg: Command arguments
            
        Returns:
            False to exit
        """
        print()  # Print a newline
        return self.do_exit(arg)
    
    def do_run(self, arg: str) -> bool:
        """
        Run a script
        
        Args:
            arg: Command arguments
            
        Returns:
            True to continue
        """
        args = ["run"] + shlex.split(arg)
        if self.verbose:
            args.append("--verbose")
        if self.quiet:
            args.append("--quiet")
        
        try:
            main(args)
        except SystemExit:
            pass  # Ignore SystemExit from argparse
        
        return True
    
    def do_config(self, arg: str) -> bool:
        """
        Manage configuration
        
        Args:
            arg: Command arguments
            
        Returns:
            True to continue
        """
        args = ["config"] + shlex.split(arg)
        if self.verbose:
            args.append("--verbose")
        if self.quiet:
            args.append("--quiet")
        
        try:
            main(args)
        except SystemExit:
            pass  # Ignore SystemExit from argparse
        
        return True
    
    def do_credentials(self, arg: str) -> bool:
        """
        Manage credentials
        
        Args:
            arg: Command arguments
            
        Returns:
            True to continue
        """
        args = ["credentials"] + shlex.split(arg)
        if self.verbose:
            args.append("--verbose")
        if self.quiet:
            args.append("--quiet")
        
        try:
            main(args)
        except SystemExit:
            pass  # Ignore SystemExit from argparse
        
        return True
    
    def do_plugins(self, arg: str) -> bool:
        """
        Manage plugins
        
        Args:
            arg: Command arguments
            
        Returns:
            True to continue
        """
        args = ["plugins"] + shlex.split(arg)
        if self.verbose:
            args.append("--verbose")
        if self.quiet:
            args.append("--quiet")
        
        try:
            main(args)
        except SystemExit:
            pass  # Ignore SystemExit from argparse
        
        return True
    
    def do_report(self, arg: str) -> bool:
        """
        Manage reports
        
        Args:
            arg: Command arguments
            
        Returns:
            True to continue
        """
        args = ["report"] + shlex.split(arg)
        if self.verbose:
            args.append("--verbose")
        if self.quiet:
            args.append("--quiet")
        
        try:
            main(args)
        except SystemExit:
            pass  # Ignore SystemExit from argparse
        
        return True
    
    def do_help(self, arg: str) -> bool:
        """
        Show help
        
        Args:
            arg: Command arguments
            
        Returns:
            True to continue
        """
        if not arg:
            print("Available commands:")
            print("  run         - Execute automation scripts")
            print("  config      - Manage configuration settings")
            print("  credentials - Manage stored credentials")
            print("  plugins     - Manage plugins")
            print("  report      - Generate and manage reports")
            print("  exit/quit   - Exit the shell")
            print("  help        - Show this help message")
            print("\nUse 'help <command>' for more information on a specific command.")
        elif arg == "run":
            print("Usage: run <script_path> [options]")
            print("\nOptions:")
            print("  --browser <browser>  - Browser to use (chrome, firefox, edge)")
            print("  --headless           - Run in headless mode")
            print("  --timeout <seconds>  - Set timeout in seconds")
            print("  --config <file>      - Use a specific configuration file")
            print("  --parallel           - Run scripts in parallel")
            print("  --max-workers <num>  - Maximum number of parallel workers")
        elif arg == "config":
            print("Usage: config <subcommand> [options]")
            print("\nSubcommands:")
            print("  show                 - Show current configuration")
            print("  set <key> <value>    - Set a configuration value")
            print("  get <key>            - Get a configuration value")
            print("  import <file>        - Import configuration from a file")
            print("  export <file>        - Export configuration to a file")
        elif arg == "credentials":
            print("Usage: credentials <subcommand> [options]")
            print("\nSubcommands:")
            print("  add <site> --username <username> --password <password>")
            print("                       - Add credentials")
            print("  get <site>           - Get credentials for a site")
            print("  list                 - List all stored credentials")
            print("  remove <site>        - Remove credentials for a site")
        elif arg == "plugins":
            print("Usage: plugins <subcommand> [options]")
            print("\nSubcommands:")
            print("  list                 - List all installed plugins")
            print("  info <plugin>        - Show information about a plugin")
            print("  install <plugin_path> - Install a plugin")
            print("  uninstall <plugin>   - Uninstall a plugin")
            print("  enable <plugin>      - Enable a plugin")
            print("  disable <plugin>     - Disable a plugin")
        elif arg == "report":
            print("Usage: report <subcommand> [options]")
            print("\nSubcommands:")
            print("  generate [--format <format>] - Generate a report")
            print("  show <report_id>     - Show a specific report")
            print("  list                 - List all reports")
            print("  export <report_id> <file> - Export a report to a file")
        else:
            print(f"No help available for {arg}")
        
        return True


def interactive_command(args: argparse.Namespace) -> int:
    """
    Handle the interactive command
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    logger = logging.getLogger(__name__)
    logger.info("Starting interactive shell")
    
    try:
        # Create and run the shell
        shell = AutoClickShell(verbose=args.verbose, quiet=args.quiet)
        shell.cmdloop()
        
        return 0
    except KeyboardInterrupt:
        print("\nInteractive shell terminated by user")
        return 1
    except Exception as e:
        logger.error(f"Error in interactive shell: {str(e)}")
        return 1
