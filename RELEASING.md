# Release Process

This project uses GitHub Actions to automatically build executables for macOS and Windows.

## Automatic Builds

The workflow (`.github/workflows/build.yml`) automatically builds on:

1. **Version tags** (e.g., `v1.0.0`) - Creates a GitHub Release with all builds
2. **Manual trigger** - Build without creating a release
3. **Pull requests** - Build to verify changes work

## Creating a Release

### Method 1: Using Git Tags (Recommended)

1. **Update version information** (optional):
   ```bash
   # Update version in main.py or add a VERSION file
   ```

2. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Release v1.0.0"
   ```

3. **Create and push a tag**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

4. **GitHub Actions will automatically**:
   - Build for macOS (ARM64)
   - Build for macOS (Intel x86_64)
   - Build for Windows (64-bit)
   - Create a GitHub Release with all builds as downloadable ZIP files

5. **Check the release**:
   - Go to your GitHub repository
   - Click "Releases" on the right sidebar
   - You'll see your new release with 3 ZIP files:
     - `WhisperTranscription-macOS.zip` (Apple Silicon)
     - `WhisperTranscription-macOS-Intel.zip` (Intel)
     - `WhisperTranscription-Windows.zip`

### Method 2: Manual Trigger

1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "Build Whisper Transcription Tool"
4. Click "Run workflow" dropdown
5. Select the branch and click "Run workflow"

This builds all platforms but doesn't create a release. Artifacts are available for 30 days in the workflow run.

## Build Artifacts

After a successful build, you can download the artifacts:

1. Go to "Actions" tab
2. Click on the workflow run
3. Scroll down to "Artifacts"
4. Download the ZIP files:
   - `WhisperTranscription-macOS.zip`
   - `WhisperTranscription-macOS-Intel.zip` (only on tagged releases)
   - `WhisperTranscription-Windows.zip`

## What Gets Built

### macOS (Apple Silicon - ARM64)
- Runs on: `macos-latest` (macOS 14 Sonoma, ARM64)
- Output: `WhisperOSX.app`
- Compatible with: M1, M2, M3, M4 Macs

### macOS (Intel - x86_64)
- Runs on: `macos-13` (macOS 13 Ventura, Intel)
- Output: `WhisperOSX_Intel.app`
- Compatible with: Intel-based Macs
- Only built on tagged releases (to save CI time)

### Windows (64-bit)
- Runs on: `windows-latest` (Windows Server 2022)
- Output: `WhisperTranscription.exe` (in a folder with dependencies)
- Compatible with: Windows 10/11 (64-bit)

## Testing Builds Locally

Before creating a release, test builds locally:

### macOS (ARM64):
```bash
./build_pyinstaller.sh
```

### macOS (Intel):
```bash
./build_intel.sh
```

### Windows:
```batch
build_windows.bat
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., `v1.2.3`)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

Examples:
- `v1.0.0` - First stable release
- `v1.1.0` - Added SRT export feature
- `v1.1.1` - Fixed SRT double extension bug
- `v2.0.0` - Major UI redesign (breaking change)

## Troubleshooting

### Build fails in GitHub Actions

1. **Check the logs**:
   - Go to Actions → Click on failed run → Click on the job → Expand failed step

2. **Common issues**:
   - Missing dependencies: Update `requirements.txt`
   - Build script errors: Test locally first
   - Timeout: Builds should complete in 10-15 minutes

### Release not created

- Make sure the tag starts with `v` (e.g., `v1.0.0`, not `1.0.0`)
- Check that you pushed the tag: `git push origin v1.0.0`
- Verify GITHUB_TOKEN has permissions (usually automatic)

### Artifacts not appearing

- Check if the build succeeded (green checkmark)
- Artifacts expire after 30 days
- For permanent storage, create a release using tags

## CI/CD Workflow Details

The workflow:
1. Triggers on tag push or manual trigger
2. Sets up Python 3.10 on each platform
3. Installs dependencies from `requirements.txt`
4. Runs the appropriate build script
5. Creates ZIP archives
6. Uploads artifacts
7. Creates GitHub Release (only for tags)

Build time: ~10-15 minutes total (runs in parallel)

## Distribution

### For End Users

Share the GitHub Release URL:
```
https://github.com/dimagoltsman/whisperUI/releases/latest
```

Users download the ZIP for their platform, extract, and run.

### For Developers

Clone the repo and run locally:
```bash
git clone https://github.com/dimagoltsman/whisperUI.git
cd whisperUI
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat on Windows
pip install -r requirements.txt
python main.py
```
