#!/bin/bash

echo "==============================="
echo " HKECC Attendance System"
echo "==============================="
echo ""

# Go to the directory where this script is located
cd "$(dirname "$0")" || exit

echo "Checking Python..."
python3 --version
if [ $? -ne 0 ]; then
  echo "❌ Python 3 is not installed."
  read -p "Press Enter to exit..."
  exit 1
fi

echo ""
echo "Installing required packages (if missing)..."
pip3 install --quiet flask openpyxl

echo ""
echo "Starting Flask server..."
python3 app.py &

# Give Flask time to start
sleep 2

echo "Opening browser..."
open http://127.0.0.1:5000/

echo ""
echo "✅ Attendance system is running."
echo "Do NOT close this window while using the system."
echo ""
read -p "Press Enter to stop the server..."
