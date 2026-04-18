#!/bin/bash
set -e

echo "Creating environment"
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies"
pip install --upgrade pip
pip install -r requirements.txt

echo "Building app"
pyinstaller \
  --windowed \
  --onedir \
  --name YTDL \
  --add-data "ui:ui" \
  app.py

echo ""
echo "DONE"
echo "Open: dist/YTDL.app"
echo "If blocked by macOS:"
echo "xattr -dr com.apple.quarantine dist/YTDL.app"
