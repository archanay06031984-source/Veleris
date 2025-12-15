Gallery generator tools

This folder contains scripts to keep `collection-*.html` pages in sync with
the images in `assets/wallpapers/*/`.

Files
- `generate_gallery.py` — generate a single collection HTML from a wallpapers folder.
- `generate_all_galleries.py` — regenerate all collections that declare a `data-gallery-prefix`.

Quick usage (PowerShell)

1) Regenerate all collections locally

```powershell
python .\tools\generate_all_galleries.py
git add collection-*.html
git commit -m "chore(collections): sync galleries"
git push origin main
```

2) Regenerate a single collection (example: gradients)

```powershell
python .\tools\generate_gallery.py gradients collection-gradients.html
git add collection-gradients.html
git commit -m "chore(collections): sync gradients"
git push origin main
```

3) If GitHub Pages shows stale content, force a rebuild

```powershell
git commit --allow-empty -m "chore(pages): trigger rebuild"
git push origin main
```

Automation
- A GitHub Actions workflow `.github/workflows/generate-galleries.yml` is included.
  When you push to `main`, the workflow runs `generate_all_galleries.py` and
  commits any updated `collection-*.html` back to the repo automatically.

Notes
- The scripts expect images to live under `assets/wallpapers/<collection>/`.
- If you add or remove images, either push your changes (the Action will run),
  or run the generator locally before pushing to preview the updated HTML.

Troubleshooting
- If a page didn't update in the site, check the Actions tab for errors.
- If you see caching/stale pages, use the empty commit rebuild command above.

Questions? Reply here and I can clarify or add examples for specific collections.
