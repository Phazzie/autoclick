@echo off
echo Installing Git hooks...

if not exist .git\hooks mkdir .git\hooks
copy /Y .githooks\pre-commit .git\hooks\
git config core.hooksPath .githooks

echo Git hooks installed successfully!
echo To use the hooks, Git has been configured to use the .githooks directory
pause