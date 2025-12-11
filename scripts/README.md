This folder contains helper scripts to generate SEO/OpenGraph images and gallery thumbnails.

Requirements
- Python 3.8+
- Pillow (install with `pip install pillow`)

Scripts
- `make_og_images.py` — creates 1200x630 PNGs in `assets/seo/`.
  Usage: `python scripts/make_og_images.py`

- `make_thumbs.py` — creates 1000px-wide thumbnails for all images under `assets/wallpapers/*` and saves them into `assets/wallpapers_thumbs/`.
  Usage: `python scripts/make_thumbs.py`

Notes
- Both scripts default to using `assets/preview.PNG` as the source for the OG images. Replace the source paths inside `make_og_images.py` if you have unique source images for each target.
- If you prefer ImageMagick, use the shell commands described in the project notes instead.
