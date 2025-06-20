@echo off
title Windows Activator Pro - Development Mode
color 0A

echo.
echo ========================================
echo   Windows Activator Pro - Dev Mode
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.7+ from python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if main.py exists
if not exist "main.py" (
    echo ❌ main.py not found!
    echo Please ensure you're in the correct directory.
    echo.
    pause
    exit /b 1
)

echo ✅ main.py found

REM Check if requirements are installed
echo.
echo 📦 Checking dependencies...
python -c "import PyQt5" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ PyQt5 not found. Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies!
        pause
        exit /b 1
    )
) else (
    echo ✅ Dependencies found
)

REM Check for admin privileges
echo.
echo 🔒 Checking administrator privileges...
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  WARNING: Not running as administrator!
    echo The application may not function properly.
    echo Please run this batch file as administrator for full functionality.
    echo.
    echo Press any key to continue anyway, or Ctrl+C to exit...
    pause >nul
) else (
    echo ✅ Running as administrator
)

REM Run the application
echo.
echo 🚀 Starting Windows Activator Pro...
echo.
python main.py

REM Check exit code
if %errorlevel% neq 0 (
    echo.
    echo ❌ Application exited with error code: %errorlevel%
) else (
    echo.
    echo ✅ Application closed normally
)

echo.
echo Press any key to exit...
pause >nul