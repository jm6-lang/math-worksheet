import urllib.request, json

def get_share_token(pwd_id):
    url = 'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/token?pr=ucpro&fr=pc'
    data = json.dumps({'pwd_id': pwd_id, 'passcode': ''}).encode()
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json',
    })
    r = urllib.request.urlopen(req, timeout=8)
    d = json.loads(r.read())
    return d['data']['stoken'], d['data']['share_type']

def get_file_list(pwd_id, stoken, share_type):
    url = 'https://drive-pc.quark.cn/1/clouddrive/share/sharepage/detail'
    data = json.dumps({'pwd_id': pwd_id, 'stoken': stoken, 'share_type': share_type,
                        'page': 1, 'size': 20, 'order_by': 'name', 'order_dir': 'asc'}).encode()
    req = urllib.request.Request(url, data=data, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': 'application/json',
    })
    r = urllib.request.urlopen(req, timeout=8)
    return json.loads(r.read())

links = [
    ('movies', 'post_127', '83a2aface3a4'),
    ('movies', 'post_128', 'c5cf90a62b23'),
    ('curriculum', 'post_034', '8363225a0eed'),
    ('curriculum', 'post_035', 'e91162128386'),
    ('curriculum', 'post_105', 'f67180336b4e'),
    ('curriculum', 'post_106', '37db7af0aad7'),
]

for d, fn, pwd_id in links:
    try:
        stoken, share_type = get_share_token(pwd_id)
        result = get_file_list(pwd_id, stoken, share_type)
        files = result.get('data', {}).get('list', [])
        if files:
            names = [f.get('name', '') for f in files[:5]]
            print(f'{d}/{fn}: {names}')
        else:
            print(f'{d}/{fn}: no files, resp={str(result)[:200]}')
    except Exception as e:
        print(f'{d}/{fn}: ERROR - {e}')
