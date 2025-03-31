@echo off
echo Running AUTOCLICK Error Detection Script...
python detect_errors.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================================
    echo ERROR: Issues were found in the codebase. Please fix them before running the app.
    echo ======================================================================
    echo.
    echo To automatically fix merge conflicts, run: detect_errors.bat --fix
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ======================================================================
    echo SUCCESS: No critical issues found. The app should run correctly.
    echo ======================================================================
    echo.
    pause
)
