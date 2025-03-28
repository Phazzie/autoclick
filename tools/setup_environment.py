"""Setup development environment with required dependencies"""
import subprocess
import sys
from pathlib import Path


def install_dependencies() -> bool:
    """Install required development dependencies"""
    print("Installing development dependencies...")

    # Core dependencies from requirements.txt
    try:
        subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Installed core dependencies")
    except subprocess.CalledProcessError:
        print("❌ Failed to install core dependencies")
        return False

    # Additional development dependencies
    dev_dependencies = [
        "black",
        "isort",
        "pylint",
        "mypy",
        "pytest",
        "pytest-cov",
        "coverage",
        "selenium",
    ]

    try:
        subprocess.run(["pip", "install"] + dev_dependencies, check=True)
        print("✅ Installed development dependencies")
    except subprocess.CalledProcessError:
        print("❌ Failed to install development dependencies")
        return False

    print("\n✅ Environment setup complete!")
    return True


def setup_project() -> bool:
    """Setup project structure and git hooks"""
    project_root = Path(__file__).parent.parent

    # Run setup_project.py
    try:
        subprocess.run(["python", str(project_root / "setup_project.py")], check=True)
        print("✅ Project setup complete")
    except subprocess.CalledProcessError:
        print("❌ Failed to setup project")
        return False

    # Run setup_hooks.py
    try:
        subprocess.run(["python", str(project_root / "setup_hooks.py")], check=True)
        print("✅ Git hooks setup complete")
    except subprocess.CalledProcessError:
        print("❌ Failed to setup git hooks")
        return False

    return True


if __name__ == "__main__":
    if not install_dependencies():
        sys.exit(1)

    if not setup_project():
        sys.exit(1)

    print("\n✅ Environment setup complete! You're ready to start developing.")
    sys.exit(0)
