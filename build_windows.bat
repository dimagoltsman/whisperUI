@echo off
REM Build Windows .exe for Whisper Transcription Tool
REM Run this script on a Windows machine

echo Building Whisper Transcription Tool for Windows...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv_win" (
    echo Creating virtual environment...
    python -m venv venv_win
)

REM Activate virtual environment
echo Activating virtual environment...
call venv_win\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Install PyInstaller
echo Installing PyInstaller...
pip install pyinstaller

REM Build the executable
echo Building Windows executable...
pyinstaller ^
    --name "WhisperTranscription" ^
    --windowed ^
    --noconfirm ^
    --clean ^
    --icon=icon.ico ^
    --hidden-import=tkinter ^
    --hidden-import=faster_whisper ^
    --hidden-import=ctranslate2 ^
    --hidden-import=av ^
    --hidden-import=tokenizers ^
    --hidden-import=huggingface_hub ^
    --hidden-import=onnxruntime ^
    --collect-all faster_whisper ^
    --collect-all ctranslate2 ^
    --collect-all tokenizers ^
    main.py

if exist "dist\WhisperTranscription" (
    echo.
    echo ✓ Build successful!
    echo Executable location: dist\WhisperTranscription\WhisperTranscription.exe
    echo.
    echo You can now distribute the entire dist\WhisperTranscription folder
    echo or create an installer using NSIS, Inno Setup, etc.
) else (
    echo.
    echo ✗ Build failed
    exit /b 1
)

pause
