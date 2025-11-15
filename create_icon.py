#!/usr/bin/env python3
"""
Create a nice icon for WhisperOSX app
"""
from PIL import Image, ImageDraw
import math

def create_icon(size=1024):
    """Create a modern icon with audio waveform design"""
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw gradient background circle
    center = size // 2
    radius = int(size * 0.45)

    # Create a nice gradient from blue to purple
    for i in range(radius, 0, -1):
        # Calculate color gradient
        ratio = i / radius
        r = int(66 + (138 - 66) * (1 - ratio))    # 66 -> 138
        g = int(135 + (43 - 135) * (1 - ratio))   # 135 -> 43
        b = int(245 + (226 - 245) * (1 - ratio))  # 245 -> 226
        alpha = 255

        draw.ellipse(
            [center - i, center - i, center + i, center + i],
            fill=(r, g, b, alpha),
            outline=None
        )

    # Draw waveform
    wave_height = int(size * 0.15)
    wave_width = int(size * 0.6)
    wave_start_x = center - wave_width // 2
    wave_y = center

    # Create multiple sine waves for a richer audio visualization
    num_bars = 11
    bar_width = wave_width // num_bars

    for i in range(num_bars):
        x = wave_start_x + i * bar_width + bar_width // 2

        # Vary bar heights to create a waveform pattern
        if i == 5:  # Middle bar tallest
            height = wave_height
        elif i in [4, 6]:
            height = int(wave_height * 0.85)
        elif i in [3, 7]:
            height = int(wave_height * 0.65)
        elif i in [2, 8]:
            height = int(wave_height * 0.75)
        elif i in [1, 9]:
            height = int(wave_height * 0.50)
        else:
            height = int(wave_height * 0.35)

        bar_rect = [
            x - bar_width // 3,
            wave_y - height // 2,
            x + bar_width // 3,
            wave_y + height // 2
        ]

        draw.rounded_rectangle(
            bar_rect,
            radius=bar_width // 6,
            fill=(255, 255, 255, 255)
        )

    # Add a subtle outer ring
    ring_width = int(size * 0.02)
    draw.ellipse(
        [
            center - radius - ring_width,
            center - radius - ring_width,
            center + radius + ring_width,
            center + radius + ring_width
        ],
        outline=(255, 255, 255, 180),
        width=ring_width
    )

    return img


def save_icon_sizes(base_img):
    """Save icon in various sizes needed for macOS"""
    sizes = [16, 32, 64, 128, 256, 512, 1024]

    # Create iconset directory
    import os
    iconset_dir = "icon.iconset"
    os.makedirs(iconset_dir, exist_ok=True)

    for size in sizes:
        # Normal resolution
        resized = base_img.resize((size, size), Image.Resampling.LANCZOS)
        resized.save(f"{iconset_dir}/icon_{size}x{size}.png")

        # Retina resolution (@2x) for smaller sizes
        if size <= 512:
            size_2x = size * 2
            resized_2x = base_img.resize((size_2x, size_2x), Image.Resampling.LANCZOS)
            resized_2x.save(f"{iconset_dir}/icon_{size}x{size}@2x.png")

    print(f"✓ Icon images created in {iconset_dir}/")
    return iconset_dir


if __name__ == "__main__":
    print("Creating WhisperOSX icon...")

    # Create base icon at highest resolution
    icon = create_icon(1024)

    # Save in all required sizes
    iconset_dir = save_icon_sizes(icon)

    print("\nTo convert to .icns format, run:")
    print(f"  iconutil -c icns {iconset_dir}")
