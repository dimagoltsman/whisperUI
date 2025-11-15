#!/bin/bash
# Build script using PyInstaller (better for complex dependencies)

echo "Building WhisperOSX.app with PyInstaller..."

# Use the virtual environment's Python and pip
VENV_PYTHON="./venv/bin/python"
VENV_PIP="./venv/bin/pip"
VENV_PYINSTALLER="./venv/bin/pyinstaller"

# Check if venv exists
if [ ! -f "$VENV_PYTHON" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create it first with: python3 -m venv venv"
    exit 1
fi

# Install PyInstaller
echo "Installing PyInstaller..."
$VENV_PIP install pyinstaller

# Clean previous builds
rm -rf build dist *.spec

# Build the app
echo "Building app bundle..."
$VENV_PYINSTALLER \
    --name "WhisperOSX" \
    --windowed \
    --noconfirm \
    --clean \
    --hidden-import=tkinter \
    --hidden-import=faster_whisper \
    --hidden-import=ctranslate2 \
    --hidden-import=av \
    --hidden-import=tokenizers \
    --hidden-import=huggingface_hub \
    --hidden-import=onnxruntime \
    --collect-all faster_whisper \
    --collect-all ctranslate2 \
    --collect-all tokenizers \
    main.py

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
