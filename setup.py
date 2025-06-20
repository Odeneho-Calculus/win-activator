#!/usr/bin/env python3
"""
Setup script for Windows Activator Pro
Handles installation of dependencies and building executable
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {platform.python_version()}")
        return False
    print(f"✅ Python version: {platform.python_version()}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def build_executable():
    """Build executable using PyInstaller"""
    print("\n🔨 Building executable...")

    # PyInstaller command with options for Windows
    cmd = [
        "pyinstaller",
        "--onefile",                    # Create single executable
        "--windowed",                   # No console window
        "--name=WindowsActivatorPro",   # Executable name
        "--icon=icon.ico",              # Icon (if exists)
        "--add-data=README.md;.",       # Include README
        "--hidden-import=PyQt5.sip",    # Include hidden imports
        "--clean",                      # Clean cache
        "main.py"
    ]

    # Remove icon option if icon file doesn't exist
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")

    # Remove README option if file doesn't exist
    if not os.path.exists("README.md"):
        cmd.remove("--add-data=README.md;.")

    try:
        subprocess.check_call(cmd)
        print("✅ Executable built successfully!")
        print("📁 Executable location: dist/WindowsActivatorPro.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build executable: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return build_executable()

def create_spec_file():
    """Create PyInstaller spec file for advanced configuration"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5.sip'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WindowsActivatorPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''

    with open("WindowsActivatorPro.spec", "w") as f:
        f.write(spec_content)
    print("✅ Spec file created: WindowsActivatorPro.spec")

def create_version_info():
    """Create version info file for executable"""
    version_info = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1,0,0,0),
    prodvers=(1,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Windows Activator Pro'),
        StringStruct(u'FileDescription', u'Windows Activator Pro - Modern GUI'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'WindowsActivatorPro'),
        StringStruct(u'LegalCopyright', u'© 2024 Windows Activator Pro'),
        StringStruct(u'OriginalFilename', u'WindowsActivatorPro.exe'),
        StringStruct(u'ProductName', u'Windows Activator Pro'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''

    with open("version_info.txt", "w") as f:
        f.write(version_info)
    print("✅ Version info created: version_info.txt")

def create_batch_launcher():
    """Create batch file to run as administrator"""
    batch_content = '''@echo off
title Windows Activator Pro Launcher
echo Starting Windows Activator Pro...
echo.
echo This application requires administrator privileges.
echo Please click "Yes" when prompted by Windows UAC.
echo.
pause
powershell -Command "Start-Process 'WindowsActivatorPro.exe' -Verb RunAs"
'''

    with open("RunAsAdmin.bat", "w") as f:
        f.write(batch_content)
    print("✅ Admin launcher created: RunAsAdmin.bat")

def main():
    """Main setup function"""
    print("🚀 Windows Activator Pro Setup")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        return False

    # Install dependencies
    if not install_dependencies():
        return False

    # Ask user what to do
    print("\n📋 Setup Options:")
    print("1. Install dependencies only")
    print("2. Build executable")
    print("3. Create advanced build files")
    print("4. Full setup (dependencies + executable)")

    choice = input("\nEnter your choice (1-4): ").strip()

    if choice == "1":
        print("✅ Dependencies installed successfully!")

    elif choice == "2":
        if build_executable():
            create_batch_launcher()
            print("\n🎉 Build completed successfully!")
            print("📁 Files created:")
            print("   - dist/WindowsActivatorPro.exe")
            print("   - RunAsAdmin.bat")

    elif choice == "3":
        create_spec_file()
        create_version_info()
        print("\n✅ Advanced build files created!")
        print("📝 You can now customize WindowsActivatorPro.spec and run:")
        print("   pyinstaller WindowsActivatorPro.spec")

    elif choice == "4":
        create_spec_file()
        create_version_info()
        if build_executable():
            create_batch_launcher()
            print("\n🎉 Full setup completed successfully!")
            print("📁 Files created:")
            print("   - dist/WindowsActivatorPro.exe")
            print("   - RunAsAdmin.bat")
            print("   - WindowsActivatorPro.spec")
            print("   - version_info.txt")
    else:
        print("❌ Invalid choice!")
        return False

    print("\n📖 Usage Instructions:")
    print("1. Run 'python main.py' to test the application")
    print("2. Use 'RunAsAdmin.bat' to run the executable as administrator")
    print("3. The application requires admin privileges to modify Windows activation")

    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")

    input("\nPress Enter to exit...")