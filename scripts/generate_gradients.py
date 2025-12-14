from PIL import Image
import os

OUT_DIR = os.path.join('assets', 'wallpapers', 'gradients')
THUMB_DIR = os.path.join('assets', 'wallpapers_thumbs')
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

WIDTH, HEIGHT = 3840, 2160
THUMB_W = 1000

palettes = [
    (('#ff7e5f','#feb47b')),
    (('#6a11cb','#2575fc')),
    (('#00b09b','#96c93d')),
    (('#e65c00','#f9d423')),
    (('#8E2DE2','#4A00E0')),
    (('#f7971e','#ffd200')),
    (('#43cea2','#185a9d')),
    (('#ffafbd','#ffc3a0'))
]

for i, pair in enumerate(palettes, start=1):
    a_hex, b_hex = pair
    def hex_to_rgb(h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    a = hex_to_rgb(a_hex)
    b = hex_to_rgb(b_hex)

    img = Image.new('RGB', (WIDTH, HEIGHT), color=0)
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        r = int(a[0] * (1 - t) + b[0] * t)
        g = int(a[1] * (1 - t) + b[1] * t)
        bl = int(a[2] * (1 - t) + b[2] * t)
        Image.new('RGB', (1,1), (r,g,bl))
        img.paste(Image.new('RGB', (WIDTH,1), (r,g,bl)), (0,y))

    name = f'gradients-{i:02d}.jpg'
    out_path = os.path.join(OUT_DIR, name)
    img.save(out_path, quality=92)

    # create thumbnail preserving aspect ratio
    thumb = img.copy()
    thumb.thumbnail((THUMB_W, THUMB_W*2))
    thumb_path = os.path.join(THUMB_DIR, name)
    thumb.save(thumb_path, quality=85)

    print('Created', out_path, 'and', thumb_path)
