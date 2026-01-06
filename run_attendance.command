#!/bin/bash

echo "==============================="
echo " HKECC Attendance System"
echo "==============================="
echo ""

# Go to the directory where this script is located
cd "$(dirname "$0")" || exit 1

echo "Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
  echo "❌ Python 3 is not installed."
  read -p "Press Enter to exit..."
  exit 1
fi

echo ""
echo "Setting up virtual environment..."

VENV_DIR=".venv"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating venv in $VENV_DIR..."
  python3 -m venv "$VENV_DIR"
  if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment."
    read -p "Press Enter to exit..."
    exit 1
  fi
else
  echo "venv already exists."
fi

echo "Activating venv..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"
if [ $? -ne 0 ]; then
  echo "❌ Failed to activate virtual environment."
  read -p "Press Enter to exit..."
  exit 1
fi

echo ""
echo "Upgrading pip (recommended)..."
python -m pip install --quiet --upgrade pip

echo ""
echo "Installing required packages (if missing)..."
python -m pip install --quiet flask openpyxl

echo ""
echo "Starting Flask server..."
python app.py &
FLASK_PID=$!

# Give Flask time to start
sleep 2

echo "Opening browser..."
open http://127.0.0.1:5000/

echo ""
echo "✅ Attendance system is running."
echo "Do NOT close this window while using the system."
echo ""
read -p "Press Enter to stop the server..."

echo "Stopping server..."
kill $FLASK_PID 2>/dev/null

echo "Done."