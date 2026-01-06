@echo off
setlocal enabledelayedexpansion

echo ===============================
echo  HKECC Attendance System
echo ===============================
echo.

REM Go to the directory where this script is located
cd /d "%~dp0"

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
  py --version >nul 2>&1
  if errorlevel 1 (
    echo ❌ Python 3 is not installed or not in PATH.
    pause
    exit /b 1
  ) else (
    set "PY=py"
  )
) else (
  set "PY=python"
)

echo.
echo Setting up virtual environment...
set "VENV_DIR=.venv"

if not exist "%VENV_DIR%\Scripts\python.exe" (
  echo Creating venv in %VENV_DIR%...
  %PY% -m venv "%VENV_DIR%"
  if errorlevel 1 (
    echo ❌ Failed to create virtual environment.
    pause
    exit /b 1
  )
) else (
  echo venv already exists.
)

echo Activating venv...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
  echo ❌ Failed to activate virtual environment.
  pause
  exit /b 1
)

echo.
echo Upgrading pip (recommended)...
python -m pip install --quiet --upgrade pip

echo.
echo Installing required packages (if missing)...
python -m pip install --quiet flask openpyxl

echo.
echo Starting Flask server...
start "HKECC Attendance Server" /min cmd /c "call \"%VENV_DIR%\Scripts\activate.bat\" ^& python app.py"

echo.
echo Opening browser...
start "" "http://127.0.0.1:5000/"

echo.
echo ✅ Attendance system is running.
echo A separate minimized window was opened for the server.
echo Close that server window to stop the system.
echo.
pause
endlocal