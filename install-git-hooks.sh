#!/bin/bash

# Script to install git hooks

# Create .git/hooks directory if it doesn't exist
mkdir -p .git/hooks

# Copy pre-commit hook
cp .githooks/pre-commit .git/hooks/
chmod +x .git/hooks/pre-commit

# Set git to use the hooks directory
git config core.hooksPath .githooks

echo "Git hooks installed successfully!"
echo "To use the hooks, run: git config core.hooksPath .githooks"
