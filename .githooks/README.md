# Git Hooks

This directory contains Git hooks for the AUTOCLICK project.

## Available Hooks

### pre-commit

The pre-commit hook checks for:

- Merge conflict markers
- Null bytes in Python files (which may indicate UTF-16 encoding)
- Empty files or files with only whitespace
- Correct encoding for workflow_view.py (must be UTF-8)

## Installation

To install the hooks, run:

```bash
# Option 1: Copy the hooks to the .git/hooks directory
cp .githooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Option 2: Configure Git to use the hooks directory
git config core.hooksPath .githooks
```

Or use the provided script:

```bash
./install-git-hooks.sh
```

## Adding New Hooks

To add a new hook:

1. Create a new file in the `.githooks` directory with the name of the hook (e.g., `pre-push`)
2. Make the file executable: `chmod +x .githooks/pre-push`
3. Add the hook to the installation script if needed

## Available Git Hooks

- `pre-commit`: Runs before a commit is created
- `prepare-commit-msg`: Runs before the commit message editor is launched
- `commit-msg`: Runs after the commit message is saved
- `post-commit`: Runs after a commit is created
- `pre-push`: Runs before a push is executed
- `pre-rebase`: Runs before a branch is rebased
- `post-checkout`: Runs after a checkout is executed
- `post-merge`: Runs after a merge is executed

For more information, see the [Git documentation on hooks](https://git-scm.com/docs/githooks).
