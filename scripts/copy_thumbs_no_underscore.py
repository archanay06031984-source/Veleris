import os, shutil
root = os.path.join('assets','wallpapers_thumbs')
files = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root,f))]
for f in files:
    if f.endswith('_.png'):
        new = f[:-5] + '.png'
        src = os.path.join(root,f)
        dst = os.path.join(root,new)
        if not os.path.exists(dst):
            shutil.copy2(src,dst)
            print('Copied thumb', f, '->', new)
        else:
            print('Thumb exists, skipped', new)
