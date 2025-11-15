# Whisper Transcription Tool

A cross-platform desktop application for transcribing audio and video files using OpenAI's Whisper model via the faster-whisper library.

**Available for macOS and Windows**

## Features

- 🎵 Support for multiple audio/video formats (MP3, MP4, WAV, M4A, AVI, MOV, etc.)
- 🚀 Optimized for Intel Macs using faster-whisper with int8 quantization
- ⏱️ Timestamp support for each transcribed segment
- 🌍 Automatic language detection
- 💾 Multiple export formats:
  - Plain text transcription
  - SRT subtitle format with segment timestamps
  - SRT with word-level timestamps for precise subtitling
- 🎛️ Multiple model sizes (tiny to large-v3)

## Installation

### Prerequisites

- Python 3.8 or higher
- **macOS** (Intel or Apple Silicon) or **Windows** (10 or higher, 64-bit)

### Setup (macOS / Linux)

For Windows setup instructions, see [WINDOWS_BUILD.md](WINDOWS_BUILD.md)

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```bash
   python main.py
   ```

2. **Select a model size:**
   - `tiny` - Fastest, least accurate (~75MB)
   - `base` - Good balance (~150MB) **[Recommended for Intel Macs]**
   - `small` - Better accuracy (~500MB)
   - `medium` - High accuracy (~1.5GB)
   - `large-v2/v3` - Best accuracy (~3GB)

3. **Click "Select Audio/Video File"** and choose your file

4. **Wait for transcription** (progress bar will show activity)

5. **Save the result** using one of the save buttons:
   - **Save Text** - Plain text transcription with timestamps
   - **Save SRT** - Standard SRT subtitle format with segment-level timestamps
   - **Save SRT (Words)** - Karaoke-style SRT where each word is underlined as it's spoken (great for language learning!)

## Performance Notes

- **First run**: The selected model will be downloaded automatically
- **Intel Macs**: The `base` or `small` models provide the best speed/accuracy balance
- **Apple Silicon Macs**: Can handle larger models more efficiently
- Models are cached in `~/.cache/huggingface/` after first download

## Supported File Formats

- **Audio**: MP3, WAV, M4A, FLAC, OGG, WMA, AAC
- **Video**: MP4, AVI, MOV, MKV

## Download Pre-built Releases

**The easiest way to get the app is to download pre-built releases from GitHub:**

👉 **[Download Latest Release](https://github.com/dimagoltsman/whisperUI/releases/latest)**

Available builds:
- **macOS (Apple Silicon)** - For M1/M2/M3/M4 Macs
- **macOS (Intel)** - For Intel-based Macs
- **Windows (64-bit)** - For Windows 10/11

All builds are automatically created using GitHub Actions whenever a new version is released.

## Building Standalone Applications

### Automated Builds (GitHub Actions)

This project uses GitHub Actions to automatically build for all platforms:

1. **Fork or clone this repository**
2. **Push a version tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
3. **GitHub Actions will automatically build**:
   - macOS app (Apple Silicon)
   - macOS app (Intel)
   - Windows executable

4. **Download from the Releases page**

See [RELEASING.md](RELEASING.md) for detailed instructions.

### Manual Local Builds

#### macOS App

To create a standalone macOS .app bundle:

1. **Make sure you're in the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run the build script:**
   ```bash
   ./build_pyinstaller.sh
   ```

3. **The app will be created in the `dist/` folder:**
   ```bash
   open dist/
   ```

4. **Drag `WhisperOSX.app` to your Applications folder**

**Note:** The first time you open the app, macOS may show a security warning because it's not signed. Right-click the app and select "Open" to bypass this.

### Intel vs Apple Silicon

**Building for Intel Macs from Apple Silicon:**

If you're on an Apple Silicon Mac but need an Intel-compatible version:

```bash
./build_intel.sh
```

This uses Rosetta 2 to create an x86_64 version that works on Intel Macs.

**Building for your native architecture:**

```bash
./build_pyinstaller.sh   # Creates ARM64 on Apple Silicon, x86_64 on Intel
```

The build scripts will create:
- `WhisperUI.app` - Native architecture version
- `WhisperUI_Intel.app` - Intel (x86_64) version (from build_intel.sh)

### macOS Build Details

- Uses **PyInstaller** (works better with complex ML dependencies)
- Creates a ~500MB app bundle (includes Python + all dependencies)
- First run will download the selected Whisper model
- Build time: ~30 seconds

### Windows Executable

To create a standalone Windows .exe:

**Important:** You must build on a Windows machine. PyInstaller cannot cross-compile from macOS to Windows.

1. **Copy the project to a Windows computer**

2. **Open Command Prompt or PowerShell** in the project directory

3. **Run the build script:**
   ```batch
   build_windows.bat
   ```

4. **The executable will be created in `dist\WhisperUI\`**

For detailed Windows build instructions, see [WINDOWS_BUILD.md](WINDOWS_BUILD.md)

### Windows Build Details

- Uses **PyInstaller** for packaging
- Creates a ~500MB executable folder (includes Python + all dependencies)
- Distribute the entire `dist\WhisperUI` folder
- Optionally create an installer using Inno Setup or NSIS

## Troubleshooting

### "No module named 'faster_whisper'"
Make sure you've activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Slow transcription
- Try using a smaller model (tiny or base)
- Ensure no other CPU-intensive applications are running

### Out of memory
- Use a smaller model size
- Close other applications to free up RAM

## License

MIT License - feel free to modify and distribute
