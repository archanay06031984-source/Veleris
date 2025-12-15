#!/usr/bin/env python3
"""
generate_all_galleries.py

Scan all collection-*.html files and run the gallery generator for pages that declare
a `data-gallery-prefix` or `data-gallery-list` attribute.

Usage:
  python tools\generate_all_galleries.py

It will call `generate_gallery.py` for each collection page found.
"""

import subprocess
from pathlib import Path
import re


def find_collection_pages(root: Path):
    return sorted(root.glob('collection-*.html'))


def extract_prefix(html_path: Path):
    text = html_path.read_text(encoding='utf-8')
    m = re.search(r'data-gallery-prefix\s*=\s*"([^"]+)"', text)
    if m:
        return m.group(1)
    # fallback: look for data-gallery-list — we still need a prefix
    m2 = re.search(r'data-gallery-list\s*=\s*"([^"]+)"', text)
    if m2:
        # try to find a nearby data-gallery-prefix or guess folder name from html filename
        m3 = re.search(r'data-gallery-prefix\s*=\s*"([^"]+)"', text)
        if m3:
            return m3.group(1)
    return None


def folder_from_prefix(prefix: str):
    # prefix expected like 'assets/wallpapers/gradients/' or 'assets/wallpapers/abstract/abstract-'
    p = Path(prefix)
    parts = list(p.parts)
    try:
        idx = parts.index('wallpapers')
        folder = parts[idx + 1]
        return folder
    except ValueError:
        return None
    except IndexError:
        return None


def main():
    root = Path.cwd()
    pages = find_collection_pages(root)
    if not pages:
        print('No collection pages found')
        return

    for page in pages:
        prefix = extract_prefix(page)
        if not prefix:
            print(f'Skipping {page.name}: no gallery prefix/list')
            continue

        folder = folder_from_prefix(prefix)
        if not folder:
            print(f'Could not determine folder for {page.name} (prefix={prefix})')
            continue

        print(f'Generating gallery for {page.name} from assets/wallpapers/{folder}/')
        # call the generator
        subprocess.run(['python', str(root / 'tools' / 'generate_gallery.py'), folder, str(page)], check=True)


if __name__ == '__main__':
    main()
