@echo off
REM ============================================================
REM 🏭 Personal Branding Factory — Windows Launcher
REM ============================================================
REM Double-click this file to launch the Branding Factory GUI.
REM ============================================================

title Personal Branding Factory

REM Find project directory (where this .bat lives)
cd /d "%~dp0"

REM Check if profile.yaml exists
if not exist "profile.yaml" (
    echo.
    echo ⚠️  No profile found! Running setup wizard...
    echo.
    python setup_profile.py
    if errorlevel 1 (
        echo.
        echo ❌ Setup failed. Make sure Python is installed.
        pause
        exit /b 1
    )
)

REM Try python, then python3
where python >nul 2>nul
if %errorlevel%==0 (
    python app.py
) else (
    where python3 >nul 2>nul
    if %errorlevel%==0 (
        python3 app.py
    ) else (
        echo.
        echo ❌ Python not found! Please install Python 3.10+ from python.org
        echo    Make sure to check "Add Python to PATH" during install.
        echo.
        pause
        exit /b 1
    )
)
