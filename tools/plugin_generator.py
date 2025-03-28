import argparse
import logging
import re
import sys
from dataclasses import dataclass
from importlib import import_module, util
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class PluginConfig:
    """Immutable configuration for plugin generation"""

    name: str
    type: str
    force: bool = False
    base_path: Path = Path.cwd()


class PluginGeneratorError(Exception):
    """Base exception for plugin generation errors"""

    pass


class InvalidPluginNameError(PluginGeneratorError):
    """Raised when plugin name is invalid"""

    pass


class InvalidPluginTypeError(PluginGeneratorError):
    """Raised when plugin type is invalid"""

    pass


class InterfaceNotFoundError(PluginGeneratorError):
    """Raised when required interface is not found"""

    pass


class PluginGenerator:
    """Handles generation of plugin files with proper structure and validation"""

    VALID_PLUGIN_TYPES = {"reporters", "runners", "storage"}
    NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

    def __init__(self, base_path: Path | str) -> None:
        """
        Initialize generator with base project path

        Args:
            base_path: Root path of the project
        """
        self.base_path = Path(base_path)
        self.logger = self._setup_logging()

    @staticmethod
    def _setup_logging() -> logging.Logger:
        """Configure logging for the generator

        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(__name__)
        if not logger.handlers:  # Avoid adding handlers multiple times
            handler = logging.StreamHandler()
            formatter = logging.Formatter("%(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def validate_plugin_name(self, name: str) -> None:
        """
        Validate plugin name follows naming conventions

        Args:
            name: Plugin name to validate

        Raises:
            InvalidPluginNameError: If name is invalid
        """
        if not self.NAME_PATTERN.match(name):
            raise InvalidPluginNameError(
                "Plugin name must start with a letter and contain only "
                "lowercase letters, numbers, and underscores"
            )

    def validate_plugin_type(self, plugin_type: str) -> None:
        """
        Validate plugin type is supported

        Args:
            plugin_type: Type of plugin to validate

        Raises:
            InvalidPluginTypeError: If type is invalid
        """
        if plugin_type not in self.VALID_PLUGIN_TYPES:
            raise InvalidPluginTypeError(
                f"Plugin type must be one of: {', '.join(self.VALID_PLUGIN_TYPES)}"
            )

    def validate_interface_exists(self, plugin_type: str) -> None:
        """
        Validate that the required interface exists

        Args:
            plugin_type: Type of plugin to validate

        Raises:
            InterfaceNotFoundError: If interface module cannot be found
        """
        interface_path = self.base_path / "src" / "core" / "interfaces.py"
        if not interface_path.exists():
            raise InterfaceNotFoundError(
                f"Interface file not found at {interface_path}"
            )

        try:
            spec = util.spec_from_file_location("interfaces", interface_path)
            if spec is None or spec.loader is None:
                raise InterfaceNotFoundError("Failed to load interface module")

            module = util.module_from_spec(spec)
            spec.loader.exec_module(module)

            interface_name = f"{plugin_type.capitalize()}Interface"
            if not hasattr(module, interface_name):
                raise InterfaceNotFoundError(f"Interface {interface_name} not found")
        except Exception as e:
            raise InterfaceNotFoundError(f"Failed to validate interface: {str(e)}")

    def get_plugin_path(self, config: PluginConfig) -> Path:
        """
        Get the full path for the plugin file

        Args:
            config: Plugin configuration

        Returns:
            Path object for the plugin file
        """
        return self.base_path / "src" / "plugins" / config.type / f"{config.name}.py"

    def plugin_exists(self, config: PluginConfig) -> bool:
        """
        Check if plugin already exists

        Args:
            config: Plugin configuration

        Returns:
            True if plugin exists, False otherwise
        """
        return self.get_plugin_path(config).exists()

    def generate_plugin_content(self, config: PluginConfig) -> str:
        """
        Generate the plugin file content

        Args:
            config: Plugin configuration

        Returns:
            String containing the plugin code
        """
        interface_name = f"{config.type.capitalize()}Interface"
        class_name = f"{config.name.capitalize()}Plugin"

        return f'''"""
{config.name.capitalize()} plugin for {config.type}
"""
from typing import Dict, Any
from src.core.interfaces import {interface_name}

class {class_name}({interface_name}):
    """
    {config.name.capitalize()} plugin implementation
    """

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        Initialize the plugin

        Args:
            config: Plugin configuration dictionary
        """
        self.config = config

    # TODO: Implement interface methods
'''

    def create_plugin(self, config: PluginConfig) -> Path:
        """
        Creates a new plugin with proper structure and validation

        Args:
            config: Plugin configuration

        Returns:
            Path to the created plugin file

        Raises:
            PluginGeneratorError: On validation or creation errors
        """
        self.validate_plugin_name(config.name)
        self.validate_plugin_type(config.type)
        self.validate_interface_exists(config.type)

        plugin_path = self.get_plugin_path(config)

        if self.plugin_exists(config) and not config.force:
            raise PluginGeneratorError(
                f"Plugin '{config.name}' already exists in {config.type}. "
                "Use --force to overwrite."
            )

        plugin_path.parent.mkdir(parents=True, exist_ok=True)
        plugin_path.write_text(self.generate_plugin_content(config))

        self.logger.info(f"Successfully created plugin: {plugin_path}")
        return plugin_path


def parse_args() -> PluginConfig:
    """
    Parse command line arguments using argparse

    Returns:
        PluginConfig object
    """
    parser = argparse.ArgumentParser(
        description="Generate plugin files for the project"
    )
    parser.add_argument("name", help="Name of the plugin")
    parser.add_argument(
        "type", choices=PluginGenerator.VALID_PLUGIN_TYPES, help="Type of the plugin"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force overwrite if plugin already exists"
    )
    parser.add_argument(
        "--base-path", type=Path, default=Path.cwd(), help="Base path of the project"
    )

    args = parser.parse_args()
    return PluginConfig(
        name=args.name, type=args.type, force=args.force, base_path=args.base_path
    )


def main() -> None:
    """Main entry point for the plugin generator"""
    try:
        config = parse_args()
        generator = PluginGenerator(config.base_path)
        plugin_path = generator.create_plugin(config)
        sys.exit(0)
    except PluginGeneratorError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
