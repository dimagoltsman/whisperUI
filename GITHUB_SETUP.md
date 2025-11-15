# GitHub Setup Guide

Quick guide to set up this repository on GitHub and enable automatic builds.

## Initial Setup

### 1. Create a GitHub Repository

1. Go to [github.com](https://github.com) and sign in
2. Click the "+" icon → "New repository"
3. Name it: `whisper-transcription` (or any name you prefer)
4. Choose Public or Private
5. **Don't** initialize with README (we already have one)
6. Click "Create repository"

### 2. Push Your Code

In your project directory:

```bash
# Initialize git if you haven't already
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Whisper Transcription Tool"

# Add your GitHub repository as remote
git remote add origin https://github.com/dimagoltsman/whisperUI.git

# Push to GitHub
git push -u origin main
```

If you're on `master` branch instead of `main`:
```bash
git branch -M main
git push -u origin main
```

### 3. Verify Links

The README has been updated with the correct repository URL:

```markdown
👉 **[Download Latest Release](https://github.com/dimagoltsman/whisperUI/releases/latest)**
```

Everything is ready to push!

### 4. Verify GitHub Actions

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see "Build Whisper Transcription Tool" workflow listed
4. If prompted, click "I understand my workflows, go ahead and enable them"

## Creating Your First Release

### Create and push a version tag:

```bash
# Make sure you're on main branch and everything is committed
git checkout main
git pull

# Create a version tag
git tag v1.0.0

# Push the tag
git push origin v1.0.0
```

### What happens next:

1. GitHub Actions automatically starts building
2. Builds run in parallel:
   - macOS (Apple Silicon) - ~10 minutes
   - macOS (Intel) - ~10 minutes
   - Windows - ~10 minutes
3. When finished, a new Release appears with all 3 builds
4. Users can download from: `https://github.com/dimagoltsman/whisperUI/releases`

### Monitor the build:

1. Go to "Actions" tab
2. Click on the running workflow
3. Watch the progress of each build
4. If something fails, click on the failed job to see logs

## Testing Without Creating a Release

You can trigger builds manually without creating a release:

1. Go to "Actions" tab
2. Click "Build Whisper Transcription Tool"
3. Click "Run workflow" dropdown on the right
4. Select branch (usually `main`)
5. Click "Run workflow" button

This will build all platforms and upload artifacts for 30 days, but won't create a public release.

## Troubleshooting

### "Actions" tab not visible
- Make sure the repository is yours (not a fork without permissions)
- Check Settings → Actions → General → ensure workflows are enabled

### Build fails
- Check the workflow logs in Actions tab
- Common issues:
  - Missing files (check `.gitignore`)
  - Syntax errors in workflow file
  - Missing dependencies in `requirements.txt`

### Release not created
- Make sure tag starts with `v` (e.g., `v1.0.0`)
- Verify you pushed the tag: `git push origin v1.0.0`
- Check Actions tab for errors

## Repository Settings (Optional)

### Enable Discussions
Settings → General → Features → Check "Discussions"

### Add Topics/Tags
Settings → About (top right) → Topics → Add:
- `whisper`
- `transcription`
- `speech-to-text`
- `macos`
- `windows`
- `srt-subtitles`

### Add Description
Settings → About → Description:
```
Cross-platform desktop app for audio/video transcription using OpenAI's Whisper. Supports SRT export with karaoke-style word highlighting.
```

## Next Steps

- **Share your repository**: Send people to your GitHub URL
- **Create releases**: Tag new versions as you add features
- **Accept contributions**: Enable Issues and Pull Requests
- **Add a license**: Add a LICENSE file (MIT recommended)

## Useful Commands

```bash
# List tags
git tag

# Delete a tag locally
git tag -d v1.0.0

# Delete a tag on GitHub
git push origin --delete v1.0.0

# Create a tag for specific commit
git tag v1.0.0 <commit-hash>

# View workflow runs
# Visit: https://github.com/dimagoltsman/whisperUI/actions
```

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Creating Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
- [Git Tagging](https://git-scm.com/book/en/v2/Git-Basics-Tagging)
