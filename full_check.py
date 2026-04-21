import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print('=' * 60)
print('全面检查网站是否有打赏相关内容（AdSense 可检测到的）')
print('=' * 60)

# 获取完整 HTML
req = urllib.request.Request('https://www.skillxm.cn/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
})
resp = urllib.request.urlopen(req, timeout=20, context=ctx)
html = resp.read().decode('utf-8', errors='replace')

print(f'\n[1] HTML 总长度: {len(html)} 字符')

# 全面关键词检查
print('\n[2] 关键词扫描:')
keywords = [
    # 中文
    ('打赏', '打赏'),
    ('赞助', '赞助'),
    ('捐赠', '捐赠'),
    ('捐款', '捐款'),
    ('支持我们', '支持我们'),
    ('微信扫码', '微信支付'),
    ('支付宝扫码', '支付宝'),
    ('PayPal', 'PayPal'),
    ('wechat', '微信英文'),
    ('alipay', '支付宝英文'),
    ('donate', '捐赠英文'),
    ('support us', '支持我们英文'),
    ('二维码', '二维码'),
    ('收款', '收款'),
    ('赏', '打赏简写'),
    # 图片相关
    ('Ad570807796524843b97705c212e925b41.png', '微信收款码图片'),
    ('Ade7b3d92013749c4b1cc18dc18fccfa5c.jpg', '支付宝收款码图片'),
    ('paypalobjects.com', 'PayPal图片'),
    ('pp_cc_mark', 'PayPal标记'),
]

found_issues = []
for keyword, desc in keywords:
    if keyword.lower() in html.lower():
        # 找到上下文
        idx = html.lower().find(keyword.lower())
        context = html[max(0, idx-50):idx+len(keyword)+50]
        found_issues.append((desc, keyword, context))
        print(f'  [发现] {desc}: "{keyword}"')
        print(f'         上下文: ...{context}...')
    else:
        pass  # 不打印没找到的

if not found_issues:
    print('  [OK] 未发现任何打赏/捐赠相关关键词')
else:
    print(f'\n  [警告] 发现 {len(found_issues)} 个问题!')

# 检查 CSS 文件
print('\n[3] 检查 style.css 是否有残留:')
try:
    req_css = urllib.request.Request('https://www.skillxm.cn/wp-content/themes/yymarket/style.css')
    resp_css = urllib.request.urlopen(req_css, timeout=15, context=ctx)
    css = resp_css.read().decode('utf-8', errors='replace')
    
    if 'support-us' in css:
        print('  [发现] style.css 中有 support-us 相关')
    else:
        print('  [OK] style.css 中无打赏相关内容')
except Exception as e:
    print(f'  [跳过] 无法获取 style.css: {e}')

# 检查 JS 文件中是否有打赏相关
print('\n[4] 检查内联 JS 中是否有打赏相关:')
if 'donate' in html.lower() or 'reward' in html.lower():
    print('  [发现] 页面 JS 中有捐赠相关代码')
else:
    print('  [OK] 内联 JS 中无打赏相关')

# 检查 meta 标签
print('\n[5] 检查 meta 标签:')
meta_pattern = r'<meta[^>]+(?:donate|reward|打赏|赞助)[^>]*>'
meta_matches = re.findall(meta_pattern, html, re.IGNORECASE)
if meta_matches:
    print(f'  [发现] meta 标签: {meta_matches}')
else:
    print('  [OK] meta 标签中无打赏相关')

# 检查 alt 属性
print('\n[6] 检查 img alt 属性:')
alt_pattern = r'<img[^>]+alt=["\'][^"\']*(?:打赏|赞助|捐赠|donate|reward)[^"\']*["\']'
alt_matches = re.findall(alt_pattern, html, re.IGNORECASE)
if alt_matches:
    print(f'  [发现] img alt 属性: {alt_matches}')
else:
    print('  [OK] img alt 属性中无打赏相关')

# 总结
print('\n' + '=' * 60)
if found_issues:
    print(f'[结论] 发现 {len(found_issues)} 个问题需要处理')
    for desc, kw, ctx in found_issues:
        print(f'  - {desc}: {kw}')
else:
    print('[结论] 未发现任何打赏/捐赠相关内容')
    print('[安全] AdSense 审核不会检测到打赏板块')
print('=' * 60)
