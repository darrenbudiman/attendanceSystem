@echo off
title HKECC Attendance System

echo ================================
echo  HKECC Attendance System
echo ================================
echo.

REM Move to the folder where this CMD file is located
cd /d "%~dp0"

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH.
    pause
    exit /b
)

echo.
echo Installing required packages (if missing)...
pip install --quiet flask openpyxl

echo.
echo Starting Flask server...
echo.

REM Start Flask in a new window
start cmd /k python app.py

REM Wait a moment for server to start
timeout /t 2 >nul

echo Opening browser...
start http://127.0.0.1:5000/

echo.
echo ✅ Attendance system is running.
echo Do NOT close the Flask window while using the system.
echo.

pause
