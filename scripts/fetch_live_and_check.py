import requests, re

urls = [
 'https://veleris.in/',
 'https://veleris.in/collections.html',
 'https://veleris.in/collection-minimal.html',
 'https://veleris.in/collection-abstract.html',
 'https://veleris.in/collection-nature.html',
 'https://veleris.in/collection-anime.html'
]

headers={'User-Agent':'Mozilla/5.0'}

results = []
for u in urls:
    r = {'url': u}
    try:
        resp = requests.get(u, headers=headers, timeout=20)
        r['status'] = resp.status_code
        html = resp.text
        m = re.search(r'<title[^>]*>(.*?)</title>', html, flags=re.S|re.I)
        r['title'] = m.group(1).strip() if m else '(none)'
        m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html, flags=re.S|re.I)
        r['canonical'] = m.group(1) if m else '(none)'
        m = re.search(r'<meta[^>]*(?:property|name)=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', html, flags=re.S|re.I)
        r['og_image'] = m.group(1) if m else '(none)'
    except Exception as e:
        r['status'] = '(error)'
        r['error'] = str(e)
    results.append(r)

# HEAD checks for sample thumbnail and full image
samples = [
 'https://veleris.in/assets/wallpapers_thumbs/minimal-01.jpg',
 'https://veleris.in/assets/wallpapers/minimal-01.jpg'
]
head_results = []
for s in samples:
    h = {'url': s}
    try:
        resp = requests.head(s, headers=headers, timeout=15, allow_redirects=True)
        h['status'] = resp.status_code
    except Exception as e:
        h['status'] = '(error)'
        h['error'] = str(e)
    head_results.append(h)

# Print summary
for r in results:
    print('===', r['url'], '===')
    print('Status:', r.get('status'))
    if 'error' in r:
        print('Error:', r['error'])
    print('Title:', r.get('title'))
    print('Canonical:', r.get('canonical'))
    print('og:image:', r.get('og_image'))
    print()

print('--- HEAD checks ---')
for h in head_results:
    print(h['url'], '->', h.get('status'), h.get('error',''))
