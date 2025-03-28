"""Setup git hooks for the project"""
import os
from pathlib import Path


def setup_hooks():
    """Install git hooks"""
    # Get project root
    root = Path(__file__).parent
    hooks_dir = root / ".git" / "hooks"
    pre_commit_path = hooks_dir / "pre-commit"

    # Create pre-commit hook content
    hook_content = """#!/bin/sh

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

    # Write the pre-commit hook
    pre_commit_path.write_text(hook_content)

    # Make hook executable
    os.chmod(pre_commit_path, 0o755)

    print("✅ Git hooks installed successfully!")


if __name__ == "__main__":
    setup_hooks()
