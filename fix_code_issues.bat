@echo off
echo Running AUTOCLICK Code Issue Fixer...
python fix_code_issues.py %*
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ======================================================================
    echo WARNING: Some issues could not be fixed automatically.
    echo ======================================================================
    echo.
    echo Run the app to see if the fixed issues resolved the problems.
    echo If not, you may need to manually fix the remaining issues.
    echo.
    pause
) else (
    echo.
    echo ======================================================================
    echo SUCCESS: All issues have been fixed or no issues were found.
    echo ======================================================================
    echo.
    echo The app should now run correctly.
    echo.
    pause
)
