# Building for Windows

This guide explains how to build the Whisper Transcription Tool on Windows.

## Prerequisites

1. **Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"

2. **Git** (optional, for cloning the repository)
   - Download from [git-scm.com](https://git-scm.com/download/win)

## Quick Build (Automated)

1. **Open Command Prompt or PowerShell** in the project directory

2. **Run the build script:**
   ```batch
   build_windows.bat
   ```

3. **Wait for the build to complete**
   - The script will create a virtual environment
   - Install all dependencies
   - Build the executable

4. **Find your application:**
   ```
   dist\WhisperTranscription\WhisperTranscription.exe
   ```

## Manual Build Steps

If you prefer to build manually or the automated script fails:

### 1. Create Virtual Environment

```batch
python -m venv venv_win
venv_win\Scripts\activate.bat
```

### 2. Install Dependencies

```batch
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
```

### 3. Build the Executable

```batch
pyinstaller --name "WhisperTranscription" --windowed --noconfirm --clean --icon=icon.ico --hidden-import=tkinter --hidden-import=faster_whisper --hidden-import=ctranslate2 --hidden-import=av --hidden-import=tokenizers --hidden-import=huggingface_hub --hidden-import=onnxruntime --collect-all faster_whisper --collect-all ctranslate2 --collect-all tokenizers main.py
```

### 4. Run the Application

```batch
dist\WhisperTranscription\WhisperTranscription.exe
```

## Distribution

The `dist\WhisperTranscription` folder contains everything needed to run the application.

### Option 1: ZIP Archive
Simply compress the `dist\WhisperTranscription` folder and distribute it.

### Option 2: Create Installer (Advanced)
Use tools like:
- **Inno Setup** (free) - [jrsoftware.org/isinfo.php](https://jrsoftware.org/isinfo.php)
- **NSIS** (free) - [nsis.sourceforge.io](https://nsis.sourceforge.io/)
- **WiX Toolset** (free) - [wixtoolset.org](https://wixtoolset.org/)

## Troubleshooting

### "Python is not recognized"
- Make sure Python is installed and added to PATH
- Restart Command Prompt after installing Python

### "pip is not recognized"
```batch
python -m pip install --upgrade pip
```

### Build fails with DLL errors
- Install Microsoft Visual C++ Redistributable: [support.microsoft.com](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)

### Application won't start
- Run from Command Prompt to see error messages:
  ```batch
  dist\WhisperTranscription\WhisperTranscription.exe
  ```

### Model download fails
- Check your internet connection
- Models are cached in `%USERPROFILE%\.cache\huggingface\`

## Performance Notes

- **First run**: The selected Whisper model will be downloaded automatically
- **Recommended models**:
  - `base` - Good balance for most PCs (~150MB)
  - `small` - Better accuracy (~500MB)
  - `medium` - For powerful PCs (~1.5GB)

## System Requirements

- **OS**: Windows 10 or higher (64-bit)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2-5GB depending on model size
- **CPU**: Multi-core processor recommended for faster transcription
