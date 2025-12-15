#!/usr/bin/env python3
"""
generate_gallery.py

Scan a wallpapers folder and update collection HTML to match current files.

Usage:
  python tools\generate_gallery.py gradients collection-gradients.html

This will:
  - read files from `assets/wallpapers/gradients/`
  - update the `data-gallery-list` attribute in the collection HTML
  - populate the `<div class="gallery-grid" data-gallery-root>` with static markup

Run this after you add/remove images so the collection page stays in sync.
"""

import sys
from pathlib import Path
import re


def get_images(folder: Path):
    exts = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    return sorted([p.name for p in folder.iterdir() if p.suffix.lower() in exts])


def build_gallery_html(prefix: str, images):
    parts = []
    for name in images:
        src = f"{prefix}{name}"
        # Each item is a clickable card linking to the full image
        parts.append(
            f'    <a class="wall-card" href="{src}">\n'
            f'      <div class="wall-thumb">\n'
            f'        <img src="{src}" alt="{name}">\n'
            f'      </div>\n'
            f'    </a>'
        )
    return "\n".join(parts)


def update_collection_html(html_path: Path, prefix: str, images):
    text = html_path.read_text(encoding='utf-8')

    # Update data-gallery-list attribute
    list_value = ', '.join(images)
    text = re.sub(r'(data-gallery-list=")[^"]*(")', rf'\1{list_value}\2', text)

    # Replace inner HTML of the gallery root div
    pattern = re.compile(r'(<div[^>]+data-gallery-root[^>]*>)(.*?)(</div>)', re.DOTALL)
    gallery_html = build_gallery_html(prefix, images)
    replacement = rf"\1\n{gallery_html}\n  \3"
    text, n = pattern.subn(replacement, text, count=1)
    if n == 0:
        raise RuntimeError('Could not find gallery root div with data-gallery-root')

    html_path.write_text(text, encoding='utf-8')


def main():
    if len(sys.argv) != 3:
        print('Usage: python tools\\generate_gallery.py <folder-name> <collection-html>')
        sys.exit(2)

    folder_name = sys.argv[1].strip()
    html_file = Path(sys.argv[2])

    base = Path.cwd()
    images_dir = base / 'assets' / 'wallpapers' / folder_name
    if not images_dir.exists():
        print('Images folder not found:', images_dir)
        sys.exit(1)

    images = get_images(images_dir)
    if not images:
        print('No images found in', images_dir)
        sys.exit(1)

    prefix = f'assets/wallpapers/{folder_name}/'
    update_collection_html(html_file, prefix, images)
    print(f'Updated {html_file} with {len(images)} images from {images_dir}')


if __name__ == '__main__':
    main()
