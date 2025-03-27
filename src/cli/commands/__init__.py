"""Command handlers for the AUTOCLICK CLI"""
from src.cli.commands.run import run_command
from src.cli.commands.config import config_command
from src.cli.commands.credentials import credentials_command
from src.cli.commands.plugins import plugins_command
from src.cli.commands.report import report_command
from src.cli.commands.interactive import interactive_command
from src.cli.commands.screenshot import screenshot_command

__all__ = [
    "run_command",
    "config_command",
    "credentials_command",
    "plugins_command",
    "report_command",
    "interactive_command",
    "screenshot_command",
]
