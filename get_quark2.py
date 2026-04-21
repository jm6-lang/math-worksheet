import urllib.request, json

def get_file_info(pwd_id):
    # Try different API endpoints
    urls = [
        f'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/token?pr=ucpro&fr=pc&pwd_id={pwd_id}&passcode=',
        f'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail?pr=ucpro&fr=pc&pwd_id={pwd_id}&stoken=&page=1&size=10',
    ]
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                'Accept': 'application/json',
            })
            r = urllib.request.urlopen(req, timeout=8)
            data = json.loads(r.read())
            print(f'  URL worked: {url[:60]}')
            print(f'  Response: {str(data)[:300]}')
            return data
        except Exception as e:
            print(f'  Failed: {e}')
    return None

links = [
    ('movies', 'post_127', '83a2aface3a4'),
    ('movies', 'post_128', 'c5cf90a62b23'),
]

for d, fn, pwd_id in links:
    print(f'\n{d}/{fn}:')
    get_file_info(pwd_id)
