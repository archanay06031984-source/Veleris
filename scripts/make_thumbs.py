from PIL import Image
import os

# Create thumbs dir if needed
os.makedirs("assets/wallpapers_thumbs", exist_ok=True)

# You can adjust this to match your wallpapers subfolders
WALLPAPERS_ROOT = "assets/wallpapers"
TARGET_WIDTH = 1000
QUALITY = 85

for root, dirs, files in os.walk(WALLPAPERS_ROOT):
    for fname in files:
        if not fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        src_path = os.path.join(root, fname)
        out_name = os.path.basename(fname)
        out_path = os.path.join("assets/wallpapers_thumbs", out_name)

        try:
            im = Image.open(src_path).convert("RGB")
            wpercent = (TARGET_WIDTH / float(im.width))
            hsize = int((float(im.height) * float(wpercent)))
            im = im.resize((TARGET_WIDTH, hsize), Image.LANCZOS)
            im.save(out_path, optimize=True, quality=QUALITY)
            print("Thumb saved:", out_path)
        except Exception as e:
            print("Failed to process", src_path, "->", e)
