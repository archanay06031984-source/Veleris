#!/usr/bin/env python3
"""
Generate gallery cards for car brand pages by scanning
assets/wallpapers/cars/<brand>/ for image files and injecting
HTML article cards into car-<brand>.html files.

Run from project root:
    python .\tools\generate_car_galleries.py

This script rewrites the section inside <div class="gallery-grid" data-brand="..."> <!-- generator:cards -->
with generated <article class="wall-card"> elements.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
WALLPAPERS = ROOT / 'assets' / 'wallpapers' / 'cars'

IMG_EXT = ('.png', '.jpg', '.jpeg', '.webp', '.gif')

BRAND_PAGE_TEMPLATE = 'car-{}.html'


def slug_to_title(slug: str) -> str:
    # lamborghini-1.jpg -> Lamborghini 1
    s = pathlib.Path(slug).stem
    s = s.replace('_', ' ').replace('-', ' ')
    # if ends with a number, split
    return s.title()


def generate_card_html(img_path: pathlib.Path, brand: str, idx: int) -> str:
    rel = img_path.as_posix()
    title = slug_to_title(img_path.name)
    # fallback short title
    short = f"{brand.title()} #{idx}"
    return (
        '      <article class="wall-card">\n'
        f'        <div class="thumb" style="background-image: url(\'{rel}\');"></div>\n'
        '        <div class="wall-info">\n'
        f'          <h3>{title}</h3>\n'
        f'          <p>{brand.title()} • 4K</p>\n'
        f'          <a href="{rel}" download class="download-link">Download</a>\n'
        '        </div>\n'
        '      </article>\n'
    )


def inject_cards_into_page(page_path: pathlib.Path, brand: str, cards_html: str):
    txt = page_path.read_text(encoding='utf-8')
    # find the generator marker region
    pattern = r'(<div[^>]*class="gallery-grid"[^>]*data-brand="' + re.escape(brand) + r'"[^>]*>)([\s\S]*?)(<\/div>)'
    m = re.search(pattern, txt)
    if not m:
        print(f"Marker not found in {page_path}; skipping")
        return
    start, old_content, end = m.group(1), m.group(2), m.group(3)
    new_content = '\n' + (cards_html if cards_html else '      <!-- no images found for this brand yet -->\n')
    replaced = start + new_content + '    ' + end
    new_txt = txt[:m.start()] + replaced + txt[m.end():]
    page_path.write_text(new_txt, encoding='utf-8')
    print(f"Injected {len(cards_html.splitlines())} lines into {page_path}")


def main():
    if not WALLPAPERS.exists():
        print("No car wallpapers folder found at", WALLPAPERS)
        return

    brands = [p.name for p in WALLPAPERS.iterdir() if p.is_dir()]
    if not brands:
        print("No brand folders found under", WALLPAPERS)

    for brand in brands:
        brand_dir = WALLPAPERS / brand
        images = sorted([p for p in brand_dir.iterdir() if p.suffix.lower() in IMG_EXT])
        cards = []
        for i, img in enumerate(images, start=1):
            cards.append(generate_card_html(img, brand, i))
        cards_html = ''.join(cards)
        page = ROOT / (BRAND_PAGE_TEMPLATE.format(brand))
        if page.exists():
            inject_cards_into_page(page, brand, cards_html)
        else:
            print(f"Page {page} not found for brand {brand}; skipping")


if __name__ == '__main__':
    main()
