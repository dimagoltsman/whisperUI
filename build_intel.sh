#!/bin/bash
# Build Intel (x86_64) version on Apple Silicon Mac using Rosetta 2

echo "Building Intel (x86_64) version using Rosetta 2..."

# Check if we're on Apple Silicon
if [[ $(uname -m) != "arm64" ]]; then
    echo "This script is for Apple Silicon Macs only."
    echo "Intel Macs should use ./build_pyinstaller.sh directly"
    exit 1
fi

# Clean previous builds
rm -rf build dist *.spec venv_intel

echo "Step 1/3: Creating x86_64 virtual environment..."
# Use arch command to force x86_64 mode
arch -x86_64 /usr/local/bin/python3 -m venv venv_intel

echo "Step 2/3: Installing dependencies (this may take a few minutes)..."
arch -x86_64 ./venv_intel/bin/pip install --upgrade pip
arch -x86_64 ./venv_intel/bin/pip install -r requirements.txt

echo "Step 3/3: Building x86_64 app bundle..."
arch -x86_64 ./venv_intel/bin/pyinstaller \
    --name "WhisperOSX_Intel" \
    --windowed \
    --noconfirm \
    --clean \
    --icon=icon.icns \
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

if [ -d "dist/WhisperOSX_Intel.app" ]; then
    ARCH=$(file dist/WhisperOSX_Intel.app/Contents/MacOS/WhisperOSX_Intel | grep -o "x86_64\|arm64")
    echo ""
    echo "✓ Build successful!"
    echo "App location: dist/WhisperOSX_Intel.app"
    echo "Architecture: $ARCH"
    echo ""
    if [[ "$ARCH" == "x86_64" ]]; then
        echo "✓ This version will work on Intel Macs!"
    else
        echo "⚠ Warning: Built for $ARCH, not x86_64"
    fi
else
    echo "✗ Build failed"
    exit 1
fi
