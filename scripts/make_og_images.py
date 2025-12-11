from PIL import Image
import os

os.makedirs("assets/seo", exist_ok=True)

# Map target -> source (if you only have one preview, use same source for all)
sources = {
    "preview": "assets/preview.PNG",
    "collections-preview": "assets/preview.PNG",
    "minimal-preview": "assets/preview.PNG",
    "abstract-preview": "assets/preview.PNG",
    "nature-preview": "assets/preview.PNG",
    "anime-preview": "assets/preview.PNG",
}

TARGET_SIZE = (1200, 630)
QUALITY = 85  # 0-100

for name, src in sources.items():
    if not os.path.exists(src):
        print(f"[WARN] source missing: {src} -> skipping {name}")
        continue
    im = Image.open(src).convert("RGBA")
    im_ratio = im.width / im.height
    target_ratio = TARGET_SIZE[0] / TARGET_SIZE[1]

    # Crop to match ratio
    if im_ratio > target_ratio:
        # crop sides
        new_w = int(im.height * target_ratio)
        left = (im.width - new_w) // 2
        im = im.crop((left, 0, left + new_w, im.height))
    else:
        # crop top/bottom
        new_h = int(im.width / target_ratio)
        top = (im.height - new_h) // 2
        im = im.crop((0, top, im.width, top + new_h))

    im = im.resize(TARGET_SIZE, Image.LANCZOS)
    out_path = f"assets/seo/{name}.png"
    im.save(out_path, optimize=True, quality=QUALITY)
    print("Saved", out_path)
