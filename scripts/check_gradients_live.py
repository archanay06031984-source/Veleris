import os
import urllib.request
import urllib.error

ROOT = 'assets/wallpapers/gradients'
THUMB_ROOT = 'assets/wallpapers_thumbs'
BASE = 'https://veleris.in'

files = sorted([f for f in os.listdir(ROOT) if os.path.isfile(os.path.join(ROOT,f))])
results = []

for f in files:
    if not f.lower().endswith(('.jpg','.jpeg','.png','.webp')):
        continue
    full_url = f"{BASE}/assets/wallpapers/gradients/{f}"
    thumb_url = f"{BASE}/assets/wallpapers_thumbs/{f}"
    for url, kind in ((full_url,'full'),(thumb_url,'thumb')):
        req = urllib.request.Request(url, method='HEAD')
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                code = resp.getcode()
        except urllib.error.HTTPError as e:
            code = e.code
        except Exception as e:
            code = str(e)
        results.append((f, kind, url, code))

# Print concise report
ok_full = [r for r in results if r[1]=='full' and r[3]==200]
ok_thumb = [r for r in results if r[1]=='thumb' and r[3]==200]
missing_full = [r for r in results if r[1]=='full' and r[3]!=200]
missing_thumb = [r for r in results if r[1]=='thumb' and r[3]!=200]

print(f"Total gradient files locally: {len(files)}")
print(f"Full-res OK: {len(ok_full)}, Missing/Errors: {len(missing_full)}")
print(f"Thumbs OK: {len(ok_thumb)}, Missing/Errors: {len(missing_thumb)}")

if missing_full:
    print('\nMissing full-res:')
    for f,kind,url,code in missing_full:
        print(f"- {f}: {code} -> {url}")
if missing_thumb:
    print('\nMissing/thumb errors:')
    for f,kind,url,code in missing_thumb:
        print(f"- {f}: {code} -> {url}")

# Exit code 0
