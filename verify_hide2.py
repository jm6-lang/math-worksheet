import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('Checking if reward section is completely hidden from HTML...')
try:
    req = urllib.request.Request('https://www.skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
    resp = urllib.request.urlopen(req, timeout=15, context=ctx)
    html = resp.read().decode('utf-8', errors='replace')
    
    # 检查是否包含打赏相关内容
    checks = [
        ('support-us-container', '打赏容器'),
        ('微信扫码支付', '微信支付文字'),
        ('支付宝扫码支付', '支付宝文字'),
        ('PayPal 捐赠', 'PayPal文字'),
        ('打赏', '打赏文字'),
        ('SUPPORT US', '英文标题'),
    ]
    
    found_any = False
    for keyword, desc in checks:
        if keyword in html:
            print(f'  [发现] {desc}: {keyword}')
            found_any = True
    
    if not found_any:
        print('  [OK] 打赏板块已彻底从 HTML 移除')
        print('  [OK] AdSense 爬虫看不到任何打赏相关内容')
    else:
        print('  [警告] 仍有打赏内容，可能需要清理缓存')
        
except Exception as e:
    print('Error:', e)
