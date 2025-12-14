import shutil, os
files = ['ComfyUI_00033_.png','ComfyUI_00035_.png','ComfyUI_00036_.png','ComfyUI_00037_.png','ComfyUI_00038_.png','ComfyUI_00039_.png','ComfyUI_00040_.png']
root = os.path.join('assets','wallpapers','gradients')
for f in files:
    src = os.path.join(root,f)
    dst = os.path.join(root,f.replace('_','.'))
    if os.path.exists(src) and not os.path.exists(dst):
        shutil.copy2(src,dst)
        print('Copied', src, '->', dst)
    else:
        print('Skipped', src)
