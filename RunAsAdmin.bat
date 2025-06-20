@echo off
title Windows Activator Pro Launcher
echo Starting Windows Activator Pro...
echo.
echo This application requires administrator privileges.
echo Please click "Yes" when prompted by Windows UAC.
echo.
pause
powershell -Command "Start-Process 'WindowsActivatorPro.exe' -Verb RunAs"
