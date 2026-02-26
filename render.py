#!/usr/bin/env python3
"""
Render HTML templates to PNG at exact Instagram dimensions.

Usage:
  Single post:
    python3 render.py input.html output.png 1080 1350

  Carousel (multiple slides):
    python3 render.py --carousel output_dir/ slide1.html slide2.html slide3.html

  With custom dimensions:
    python3 render.py input.html output.png 1080 1080      # Square (accessory/part)
    python3 render.py input.html output.png 1080 1920      # Reels/Story

Preset formats:
    python3 render.py input.html output.png --format carousel   # 1080x1350
    python3 render.py input.html output.png --format square     # 1080x1080
    python3 render.py input.html output.png --format reels      # 1080x1920

Requirements:
    pip install playwright --break-system-packages
    playwright install chromium
"""

import asyncio
import sys
import os
from pathlib import Path

FORMATS = {
    "carousel":  (1080, 1350),
    "feed":      (1080, 1350),
    "square":    (1080, 1080),
    "reels":     (1080, 1920),
    "story":     (1080, 1920),
}


async def render_single(html_path: str, output_path: str, width: int, height: int):
    """Render a single HTML file to PNG."""
    from playwright.async_api import async_playwright

    html_path = os.path.abspath(html_path)
    output_path = os.path.abspath(output_path)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=1
        )
        await page.goto(f"file://{html_path}")
        # Wait for fonts and images to load
        await page.wait_for_timeout(1500)

        await page.screenshot(
            path=output_path,
            full_page=False,
            type="png"
        )
        await browser.close()

    print(f"✅ {output_path} ({width}x{height})")


async def render_carousel(output_dir: str, html_files: list, width: int = 1080, height: int = 1350):
    """Render multiple HTML files as numbered carousel slides."""
    os.makedirs(output_dir, exist_ok=True)

    for i, html_file in enumerate(html_files, 1):
        name = Path(html_file).stem
        output_path = os.path.join(output_dir, f"{name}.png")
        await render_single(html_file, output_path, width, height)

    print(f"\n🎯 Carousel rendered: {len(html_files)} slides in {output_dir}/")


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)

    # Carousel mode
    if args[0] == "--carousel":
        if len(args) < 3:
            print("Usage: render.py --carousel output_dir/ slide1.html slide2.html ...")
            sys.exit(1)
        output_dir = args[1]
        html_files = args[2:]
        asyncio.run(render_carousel(output_dir, html_files))
        return

    # Single file mode
    html_path = args[0]
    output_path = args[1] if len(args) > 1 else html_path.replace(".html", ".png")

    # Determine dimensions
    width, height = 1080, 1350  # Default: feed 4:5

    if len(args) > 2 and args[2].startswith("--format"):
        fmt = args[2].split("=")[1] if "=" in args[2] else args[3]
        if fmt in FORMATS:
            width, height = FORMATS[fmt]
        else:
            print(f"Unknown format '{fmt}'. Available: {', '.join(FORMATS.keys())}")
            sys.exit(1)
    elif len(args) > 3:
        try:
            width = int(args[2])
            height = int(args[3])
        except ValueError:
            print("Width and height must be integers.")
            sys.exit(1)

    asyncio.run(render_single(html_path, output_path, width, height))


if __name__ == "__main__":
    main()
