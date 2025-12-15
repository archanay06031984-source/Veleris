````markdown
Gallery generator tools (moved to tools/disabled)

These tools were moved to `tools/disabled/` to avoid accidental automatic runs.
If you need to re-enable them, move them back to `tools/` or copy the files.

Files moved:
- `generate_gallery.py`
- `generate_all_galleries.py`
- `generate_car_galleries.py`
- `update_mobile_gallery.py`

Quick local usage (PowerShell)

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

````