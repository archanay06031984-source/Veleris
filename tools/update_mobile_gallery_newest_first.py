#!/usr/bin/env python3
"""
update_mobile_gallery_newest_first.py

Regenerate the <main class="wall-grid"> section in `mobile.html` from the
files currently present in `assets/wallpapers/mobile/`, sorted newest (highest number) first.

Usage:
  python tools/update_mobile_gallery_newest_first.py

This updates image hrefs and src to include a `v=` version (timestamp) to
help bust caches.
"""

from pathlib import Path
from datetime import datetime
import re


def list_images_newest_first(dirpath: Path):
    exts = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp'}
    files = [p.name for p in dirpath.iterdir() if p.is_file() and p.suffix.lower() in exts]
    # Sort in reverse order so highest numbers appear first
    files_sorted = sorted(files, reverse=True)
    return files_sorted


def build_grid_html(images, version):
    parts = []
    for name in images:
        href = f'mobile-view.html?img={name}&v={version}'
        src = f'assets/wallpapers/mobile/{name}?v={version}'
        parts.append(f'  <a class="wall-card" href="{href}"><img src="{src}" alt=""></a>')
    return "\n".join(parts)


def replace_main(html_text: str, new_inner: str) -> str:
    pattern = re.compile(r'(<main[^>]*class="wall-grid"[^>]*>)(.*?)(</main>)', re.DOTALL)
    new = pattern.sub(lambda m: m.group(1) + "\n" + new_inner + "\n" + m.group(3), html_text, count=1)
    if new == html_text:
        raise RuntimeError('Could not find <main class="wall-grid"> in mobile.html')
    return new


def main():
    base = Path.cwd()
    mobile_dir = base / 'assets' / 'wallpapers' / 'mobile'
    mobile_html = base / 'mobile.html'

    if not mobile_dir.exists():
        print('Mobile wallpapers folder not found:', mobile_dir)
        return
    if not mobile_html.exists():
        print('mobile.html not found:', mobile_html)
        return

    images = list_images_newest_first(mobile_dir)
    if not images:
        print('No mobile images found in', mobile_dir)
        return

    version = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    new_inner = build_grid_html(images, version)

    text = mobile_html.read_text(encoding='utf-8')
    new_text = replace_main(text, new_inner)
    mobile_html.write_text(new_text, encoding='utf-8')

    # also update index redirect version if present (replace any mobile.html?v=digits)
    index_html = base / 'index.html'
    if index_html.exists():
        idx_text = index_html.read_text(encoding='utf-8')
        idx_text = re.sub(r'mobile.html\?v=\d+', f'mobile.html?v={version}', idx_text)
        index_html.write_text(idx_text, encoding='utf-8')

    print(f'Updated mobile.html with {len(images)} images in reverse order (newest first) (v={version})')


if __name__ == '__main__':
    main()
