from PIL import Image, ImageDraw
import os

OUT_DIR = "assets/seo"
os.makedirs(OUT_DIR, exist_ok=True)

# Base size (high-res) to draw and then downscale
BASE = 512
bg = (245,239,228)  # #f5efe4
fg = (0,0,0)

# create base image
img = Image.new("RGBA", (BASE, BASE), bg)
d = ImageDraw.Draw(img)

# Define a V-shaped polygon (points tuned visually)
pts = [
    (BASE*0.15, BASE*0.18),
    (BASE*0.30, BASE*0.18),
    (BASE*0.50, BASE*0.62),
    (BASE*0.70, BASE*0.18),
    (BASE*0.85, BASE*0.18),
    (BASE*0.50, BASE*0.82),
]

# Draw filled polygon (V)
d.polygon(pts, fill=fg)

sizes = [512, 192, 96, 48, 32, 16]
png_paths = []
for s in sizes:
    out = img.resize((s, s), Image.LANCZOS)
    path = os.path.join(OUT_DIR, f"favicon-{s}.png")
    out.save(path, optimize=True)
    png_paths.append(path)
    print("Saved:", path)

# Save ICO (multi-size)
ico_path = os.path.join(OUT_DIR, "favicon.ico")
# Pillow can save ICO with sizes by passing 'sizes' argument
img.save(ico_path, format='ICO', sizes=[(16,16),(32,32),(48,48),(96,96),(192,192)])
print("Saved:", ico_path)

# Write SVG outline (using polygon points scaled)
svg_pts = " ".join(f"{int(x)},{int(y)}" for x,y in pts)
svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {BASE} {BASE}" width="{BASE}" height="{BASE}" role="img" aria-label="Veleris favicon">
  <rect width="100%" height="100%" fill="#f5efe4"/>
  <polygon points="{svg_pts}" fill="#000" />
</svg>
'''

svg_path_root = "favicon.svg"
svg_path_seo = os.path.join(OUT_DIR, "favicon.svg")
with open(svg_path_root, "w", encoding="utf-8") as f:
    f.write(svg_content)
with open(svg_path_seo, "w", encoding="utf-8") as f:
    f.write(svg_content)
print("Written SVG:", svg_path_root, svg_path_seo)
