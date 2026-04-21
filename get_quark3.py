import urllib.request, json

# Try Quark mobile API which sometimes works without auth
def try_quark_api(pwd_id):
    # Mobile API endpoint
    url = f'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/token?pr=ucpro&fr=pc&uc_param_str=&pwd_id={pwd_id}&passcode='
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Referer': 'https://pan.quark.cn/',
        })
        r = urllib.request.urlopen(req, timeout=8)
        d = json.loads(r.read())
        stoken = d.get('data', {}).get('stoken', '')
        share_type = d.get('data', {}).get('share_type', 0)
        
        # Now get file list
        url2 = f'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail?pr=ucpro&fr=pc&pwd_id={pwd_id}&stoken={stoken}&share_type={share_type}&page=1&size=10'
        req2 = urllib.request.Request(url2, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Referer': 'https://pan.quark.cn/',
        })
        r2 = urllib.request.urlopen(req2, timeout=8)
        d2 = json.loads(r2.read())
        files = d2.get('data', {}).get('list', [])
        return [f.get('name', '') for f in files]
    except Exception as e:
        return str(e)

links = [
    ('movies', 'post_127', '83a2aface3a4'),
    ('movies', 'post_128', 'c5cf90a62b23'),
    ('curriculum', 'post_034', '8363225a0eed'),
    ('curriculum', 'post_035', 'e91162128386'),
    ('curriculum', 'post_105', 'f67180336b4e'),
    ('curriculum', 'post_106', '37db7af0aad7'),
]

for d, fn, pwd_id in links:
    result = try_quark_api(pwd_id)
    print(f'{d}/{fn}: {result}')
