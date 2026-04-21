import urllib.request, re

resources = [
    ('中华玄学文化书系', 'https://pan.quark.cn/s/0e7cc71c170e', '0e7cc71c170e'),
    ('风水玄学合集', 'https://pan.quark.cn/s/0c74d5077d75', '0c74d5077d75'),
    ('民间秘术大全', 'https://pan.quark.cn/s/e0235f7937f2', 'e0235f7937f2'),
    ('风水学', 'https://pan.quark.cn/s/79eba9118e5e', '79eba9118e5e'),
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for title, url, sid in resources:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as r:
            data = r.read().decode('utf-8', errors='replace')
        # Try to find size info
        size_m = re.search(r'([0-9]+\.?[0-9]*\s*[GMKT]B?)', data)
        # Try to find description
        desc_m = re.search(r'content="([^"]{20,200})"', data)
        # Find folder/file name from title
        print(f'TITLE: {title}')
        print(f'URL: {url}')
        print(f'SIZE: {size_m.group(1) if size_m else "未知"}')
        print(f'DESC: {desc_m.group(1)[:100] if desc_m else "无"}')
        print()
    except Exception as e:
        print(f'ERROR {title}: {e}')
        print()
