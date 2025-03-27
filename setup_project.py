"""Setup project and git repository"""
import os
import subprocess
from pathlib import Path


def setup_project():
    """Initialize git repository and install hooks"""
    root = Path(__file__).parent

    # Initialize git repository if not already initialized
    if not (root / ".git").exists():
        print("Initializing git repository...")
        subprocess.run(["git", "init"], check=True)

        # Set up initial .gitignore
        gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.env
.venv
env/
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# Project specific
logs/
*.log
"""
        (root / ".gitignore").write_text(gitignore_content)

        # Create hooks directory
        hooks_dir = root / ".git" / "hooks"
        hooks_dir.mkdir(exist_ok=True)

        # Create pre-commit hook
        pre_commit_content = """#!/bin/sh

# First, run the code formatter to fix common issues
python tools/code_formatter.py

# If formatter fails, prevent the commit
if [ $? -ne 0 ]; then
    echo "[ERROR] Code formatting failed. Commit blocked."
    exit 1
fi

# Then run our code quality checks
python tools/code_quality_checker.py

# If checks fail, prevent the commit
if [ $? -ne 0 ]; then
    echo "[ERROR] Code quality checks failed. Commit blocked."
    exit 1
fi

echo "[SUCCESS] Code quality checks passed!"
"""
        pre_commit_path = hooks_dir / "pre-commit"
        pre_commit_path.write_text(pre_commit_content)

        # Make hook executable
        os.chmod(pre_commit_path, 0o755)

        print("✅ Git repository initialized successfully!")
        print("✅ Git hooks installed successfully!")
        print("\nNext steps:")
        print("1. git add .")
        print("2. git commit -m 'Initial commit'")
    else:
        print("Git repository already initialized!")


if __name__ == "__main__":
    setup_project()
