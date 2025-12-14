import os, shutil

root = os.path.join('assets', 'wallpapers', 'gradients')
files = sorted([f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))])

# Remove accidental files containing double-dots created earlier
for f in files:
    if '..' in f:
        p = os.path.join(root, f)
        try:
            os.remove(p)
            print('Removed accidental file', f)
        except Exception as e:
            print('Failed to remove', f, e)

# Re-read files
files = sorted([f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f))])

targets = []
for f in files:
    if f.endswith('_.png') or f.endswith('_.jpg') or f.endswith('_.jpeg'):
        if f.endswith('_.png'):
            new = f[:-5] + '.png'
        elif f.endswith('_.jpg'):
            new = f[:-5] + '.jpg'
        else:
            new = f[:-6] + '.jpeg'
        src = os.path.join(root, f)
        dst = os.path.join(root, new)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print('Copied', f, '->', new)
            targets.append(new)
        else:
            print('Target already exists, skipped', new)

print('Done')
