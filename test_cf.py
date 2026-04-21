import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Testing https://skillxm.cn/ ...')
try:
    req = urllib.request.Request('https://skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    headers = dict(resp.headers)
    print('Status:', resp.status)
    for k, v in headers.items():
        print(f'{k}: {v}')
except Exception as e:
    print('Error:', e)

print('\n' + '='*50)
print('Testing https://www.skillxm.cn/ ...')
try:
    req = urllib.request.Request('https://www.skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    headers = dict(resp.headers)
    print('Status:', resp.status)
    for k, v in headers.items():
        print(f'{k}: {v}')
except Exception as e:
    print('Error:', e)

# 检查是否有 CF-Ray
print('\n' + '='*50)
print('Checking for Cloudflare indicators...')
