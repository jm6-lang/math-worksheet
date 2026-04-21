import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Checking if reward section is hidden...')
try:
    req = urllib.request.Request('https://www.skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    html = resp.read().decode('utf-8', errors='replace')
    
    # 检查是否包含 support-us-container
    if 'support-us-container' in html:
        # 检查是否有 display:none
        if 'display: none' in html or 'display:none' in html:
            print('OK - Reward section exists but hidden via CSS')
        else:
            print('WARNING - Reward section exists, CSS may not be loaded')
    else:
        print('OK - Reward section not found in HTML')
    
    # 检查 CSS 文件是否被加载
    if 'style.css' in html:
        print('OK - style.css is loaded')
    else:
        print('INFO - style.css might be minified or combined')
        
except Exception as e:
    print('Error:', e)
