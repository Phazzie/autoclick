"""Development environment setup tool"""
import subprocess
import sys
from pathlib import Path
from typing import List


def run_command(command: List[str]) -> bool:
    """Run a command and return success status"""
    try:
        subprocess.run(command, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def setup_dev_environment() -> None:
    """Setup development environment"""
    project_root = Path(__file__).parent.parent.resolve()
    print("Setting up development environment...")

    # Create required directories
    required_dirs = ["src", "tests", "tools", ".vscode", "src/plugins"]
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            print(f"Creating {dir_name} directory...")
            dir_path.mkdir(parents=True)

    # Install development requirements
    print("\nInstalling development requirements...")
    if not run_command(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(project_root / "requirements.txt"),
        ]
    ):
        print("Error: Failed to install requirements")
        sys.exit(1)

    # Setup VSCode settings if not exists
    vscode_settings = project_root / ".vscode" / "settings.json"
    if not vscode_settings.exists():
        print("\nSetting up VSCode configuration...")
        vscode_settings.write_text(
            """{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.mypyEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": ["--line-length", "100"],
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    },
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "python.testing.pytestArgs": [
        "tests"
    ]
}"""
        )

    print("\n✅ Development environment setup complete!")
    print("\nTo start developing:")
    print("1. Open project in VSCode")
    print("2. Select Python interpreter (Ctrl+Shift+P -> Python: Select Interpreter)")
    print("3. Install recommended extensions when prompted")
    print("4. Run tests with 'pytest' or debug with F5")


if __name__ == "__main__":
    setup_dev_environment()
