#!/usr/bin/env python3
"""
Convert the macOS icon to Windows .ico format
"""
from PIL import Image

def create_windows_icon():
    """Create Windows .ico icon from the existing PNG"""
    print("Creating Windows .ico icon...")

    # Read the 256x256 icon from the iconset
    icon_path = "icon.iconset/icon_256x256.png"

    try:
        img = Image.open(icon_path)

        # Windows ICO files support multiple sizes
        # Create common Windows icon sizes
        icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

        # Save as ICO with multiple sizes
        img.save(
            "icon.ico",
            format='ICO',
            sizes=icon_sizes
        )

        print("✓ Windows icon created: icon.ico")

    except FileNotFoundError:
        print("Error: icon.iconset/icon_256x256.png not found")
        print("Please run create_icon.py first to generate the icon")
        return False

    return True

if __name__ == "__main__":
    create_windows_icon()
