@echo off
title Windows Activator Pro - Build Script
color 0B

echo.
echo ==========================================
echo   Windows Activator Pro - Build Script
echo ==========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo ✅ Python found:
python --version
echo.

REM Install/Update dependencies
echo 📦 Installing/Updating dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies!
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully
echo.

REM Create icon if it doesn't exist
if not exist "icon.ico" (
    echo 🎨 Creating application icon...
    python create_icon.py
    echo.
)

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "*.spec" del "*.spec"
echo ✅ Cleanup completed
echo.

REM Build executable
echo 🔨 Building executable...
echo This may take a few minutes...
echo.

pyinstaller ^
    --onefile ^
    --windowed ^
    --name=WindowsActivatorPro ^
    --icon=icon.ico ^
    --add-data="README.md;." ^
    --add-data="config.json;." ^
    --hidden-import=PyQt5.sip ^
    --clean ^
    --noconfirm ^
    main.py

if %errorlevel% neq 0 (
    echo ❌ Build failed!
    pause
    exit /b 1
)

echo ✅ Build completed successfully!
echo.

REM Create admin launcher
echo 📝 Creating admin launcher...
echo @echo off > RunAsAdmin.bat
echo title Windows Activator Pro Launcher >> RunAsAdmin.bat
echo echo Starting Windows Activator Pro... >> RunAsAdmin.bat
echo echo. >> RunAsAdmin.bat
echo echo This application requires administrator privileges. >> RunAsAdmin.bat
echo echo Please click "Yes" when prompted by Windows UAC. >> RunAsAdmin.bat
echo echo. >> RunAsAdmin.bat
echo pause >> RunAsAdmin.bat
echo powershell -Command "Start-Process 'dist\WindowsActivatorPro.exe' -Verb RunAs" >> RunAsAdmin.bat

echo ✅ Admin launcher created: RunAsAdmin.bat
echo.

REM Create portable package
echo 📦 Creating portable package...
if not exist "portable" mkdir "portable"
copy "dist\WindowsActivatorPro.exe" "portable\"
copy "README.md" "portable\"
copy "RunAsAdmin.bat" "portable\"

echo ✅ Portable package created in 'portable' folder
echo.

REM Display results
echo 🎉 Build Process Completed Successfully!
echo.
echo 📁 Generated Files:
echo    - dist\WindowsActivatorPro.exe (Main executable)
echo    - RunAsAdmin.bat (Admin launcher)
echo    - portable\ (Portable package)
echo.
echo 📖 Usage Instructions:
echo    1. Use RunAsAdmin.bat to run with administrator privileges
echo    2. Or manually run dist\WindowsActivatorPro.exe as administrator
echo    3. The portable folder contains all files needed for distribution
echo.
echo 🔒 Important: The application requires administrator privileges to function properly!
echo.

REM Test the executable
echo 🧪 Would you like to test the executable now? (Y/N)
set /p test_choice=
if /i "%test_choice%"=="Y" (
    echo.
    echo 🚀 Testing executable...
    echo Note: This will run without admin privileges for testing only
    start "" "dist\WindowsActivatorPro.exe"
)

echo.
echo Press any key to exit...
pause >nul