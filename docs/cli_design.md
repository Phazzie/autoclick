# AUTOCLICK Command-Line Interface Design

This document outlines the design of the AUTOCLICK command-line interface (CLI).

## Command Structure

The AUTOCLICK CLI follows a command-subcommand structure:

```
autoclick <command> <subcommand> [options]
```

## Main Commands

### 1. Run Command

Execute automation scripts.

```
autoclick run <script_path> [options]
```

Options:

- `--browser <browser>`: Browser to use (chrome, firefox, edge)
- `--headless`: Run in headless mode
- `--timeout <seconds>`: Set timeout in seconds
- `--config <config_file>`: Use a specific configuration file

Examples:

```
autoclick run scripts/login.py
autoclick run scripts/data_extraction.py --browser firefox --headless
autoclick run scripts/ --parallel --max-workers 4
```

### 2. Config Command

Manage configuration settings.

```
autoclick config <subcommand> [options]
```

Subcommands:

- `show`: Show current configuration
- `set <key> <value>`: Set a configuration value
- `get <key>`: Get a configuration value
- `import <file>`: Import configuration from a file
- `export <file>`: Export configuration to a file

Examples:

```
autoclick config show
autoclick config set browser firefox
autoclick config import my_config.json
```

### 3. Credentials Command

Manage stored credentials.

```
autoclick credentials <subcommand> [options]
```

Subcommands:

- `add <site> --username <username> --password <password>`: Add credentials
- `get <site>`: Get credentials for a site
- `list`: List all stored credentials
- `remove <site>`: Remove credentials for a site

Examples:

```
autoclick credentials add example.com --username user1 --password pass1
autoclick credentials list
```

### 4. Plugins Command

Manage plugins.

```
autoclick plugins <subcommand> [options]
```

Subcommands:

- `list`: List all installed plugins
- `info <plugin>`: Show information about a plugin
- `install <plugin_path>`: Install a plugin
- `uninstall <plugin>`: Uninstall a plugin
- `enable <plugin>`: Enable a plugin
- `disable <plugin>`: Disable a plugin

Examples:

```
autoclick plugins list
autoclick plugins install ./my_plugin
```

### 5. Report Command

Generate and manage reports.

```
autoclick report <subcommand> [options]
```

Subcommands:

- `generate [--format <format>]`: Generate a report
- `show <report_id>`: Show a specific report
- `list`: List all reports
- `export <report_id> <file>`: Export a report to a file

Examples:

```
autoclick report generate --format html
autoclick report export latest report.html
```

## Global Options

These options can be used with any command:

- `--verbose`: Enable verbose output
- `--quiet`: Suppress all output except errors
- `--help`: Show help for a command
- `--version`: Show version information

## Interactive Mode

AUTOCLICK also supports an interactive shell mode:

```
autoclick interactive
```

This starts a REPL (Read-Eval-Print Loop) where commands can be entered interactively.

## Exit Codes

- `0`: Success
- `1`: General error
- `2`: Invalid command or arguments
- `3`: Configuration error
- `4`: Execution error
- `5`: Plugin error
