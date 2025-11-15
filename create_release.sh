#!/bin/bash
# Quick script to create and push a release tag

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Whisper Transcription Tool - Release Helper${NC}"
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}Error: Not a git repository${NC}"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${RED}Error: You have uncommitted changes. Please commit or stash them first.${NC}"
    git status --short
    exit 1
fi

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo -e "Current branch: ${GREEN}${CURRENT_BRANCH}${NC}"

# Check if on main/master
if [[ "$CURRENT_BRANCH" != "main" ]] && [[ "$CURRENT_BRANCH" != "master" ]]; then
    echo -e "${RED}Warning: You're not on main/master branch${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Get latest tags
echo ""
echo "Recent tags:"
git tag --sort=-v:refname | head -5

echo ""
echo "Enter the new version tag (e.g., v1.0.0):"
read -r VERSION_TAG

# Validate tag format
if [[ ! $VERSION_TAG =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo -e "${RED}Error: Tag must be in format vX.Y.Z (e.g., v1.0.0)${NC}"
    exit 1
fi

# Check if tag already exists
if git rev-parse "$VERSION_TAG" >/dev/null 2>&1; then
    echo -e "${RED}Error: Tag $VERSION_TAG already exists${NC}"
    exit 1
fi

# Confirm
echo ""
echo -e "Ready to create and push tag: ${GREEN}${VERSION_TAG}${NC}"
echo -e "This will trigger GitHub Actions to build:"
echo "  - macOS (Apple Silicon)"
echo "  - macOS (Intel)"
echo "  - Windows"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 1
fi

# Pull latest changes
echo ""
echo -e "${BLUE}Pulling latest changes...${NC}"
if ! git pull origin "$CURRENT_BRANCH"; then
    echo -e "${RED}Error: Failed to pull latest changes${NC}"
    exit 1
fi

# Create tag
echo -e "${BLUE}Creating tag ${VERSION_TAG}...${NC}"
git tag -a "$VERSION_TAG" -m "Release $VERSION_TAG"

# Push tag
echo -e "${BLUE}Pushing tag to GitHub...${NC}"
if git push origin "$VERSION_TAG"; then
    echo ""
    echo -e "${GREEN}✓ Success!${NC}"
    echo ""
    echo "Tag $VERSION_TAG has been pushed to GitHub"
    echo "GitHub Actions will now build the release"
    echo ""
    echo "Monitor progress at:"
    echo "https://github.com/dimagoltsman/whisperUI/actions"
    echo ""
    echo "Once complete, your release will be available at:"
    echo "https://github.com/dimagoltsman/whisperUI/releases/tag/$VERSION_TAG"
else
    echo -e "${RED}Error: Failed to push tag${NC}"
    echo "Deleting local tag..."
    git tag -d "$VERSION_TAG"
    exit 1
fi
