#!/bin/bash
# Build script for WhisperOSX macOS application

echo "Building WhisperOSX.app..."

# Clean previous builds
rm -rf build dist

# Use the virtual environment's Python and pip
VENV_PYTHON="./venv/bin/python"
VENV_PIP="./venv/bin/pip"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create it first with: python3 -m venv venv"
    exit 1
fi

# Ensure py2app is installed
echo "Installing py2app..."
$VENV_PIP install py2app

# Build the app using venv's Python
echo "Building app bundle..."
$VENV_PYTHON setup.py py2app

if [ -d "dist/WhisperOSX.app" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "App location: dist/WhisperOSX.app"
    echo ""
    echo "To install, drag WhisperOSX.app to your Applications folder"
    echo "Or run: open dist/"
else
    echo "✗ Build failed"
    exit 1
fi
