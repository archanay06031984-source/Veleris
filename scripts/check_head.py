#!/usr/bin/env python3
import urllib.request
import re
urls=[
 'https://veleris.in/',
 'https://veleris.in/collections.html',
 'https://veleris.in/collection-minimal.html',
 'https://veleris.in/collection-abstract.html',
 'https://veleris.in/collection-nature.html',
 'https://veleris.in/collection-anime.html'
]

for u in urls:
    print('===', u, '===')
    try:
        req = urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            status = r.getcode()
            text = r.read().decode('utf-8', errors='replace')
        print('Status:', status)
        m = re.search(r'<title[^>]*>(.*?)</title>', text, flags=re.S|re.I)
        title = m.group(1).strip() if m else '(none)'
        print('Title:', title)
        m = re.search(r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', text, flags=re.S|re.I)
        canonical = m.group(1) if m else '(none)'
        print('Canonical:', canonical)
        m = re.search(r'<meta[^>]*(?:property|name)=["\']og:image["\'][^>]*content=["\']([^"\']+)["\']', text, flags=re.S|re.I)
        og = m.group(1) if m else '(none)'
        print('og:image:', og)
    except Exception as e:
        print('Fetch error:', e)
