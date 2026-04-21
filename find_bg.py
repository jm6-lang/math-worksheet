import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.skillxm.cn/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
})
resp = urllib.request.urlopen(req, timeout=20, context=ctx)
html = resp.read().decode('utf-8', errors='replace')

# 搜索底部背景图
print('=== 搜索底部/页脚背景图 ===\n')

# 查找所有带 background 的元素
bg_matches = re.findall(r'<[^>]+style="[^"]*(?:background|bg-image|bg-img)[^"]*"[^>]*>', html, re.IGNORECASE)
if bg_matches:
    print(f'[发现背景样式] {len(bg_matches)} 个:')
    for m in bg_matches[:10]:
        print(f'  {m[:300]}')
else:
    print('  未在 HTML 中直接找到背景样式')

# 查找 footer 附近的背景
print('\n=== 搜索页脚背景 ===')
footer_idx = html.lower().find('yy-footer')
if footer_idx > 0:
    footer_area = html[max(0, footer_idx-200):footer_idx+500]
    print(footer_area)

# 搜索 CSS 文件中的背景
print('\n\n=== 搜索 CSS 中的底部背景 ===')
# 搜索所有 background-image
bg_images = re.findall(r'background(?:-image)?\s*:\s*[^;]+url\([^)]+\)[^;]*', html, re.IGNORECASE)
if bg_images:
    print(f'找到 {len(bg_images)} 个背景图:')
    for b in bg_images:
        print(f'  {b[:200]}')

# 搜索 yy-site 或 main wrapper 的背景
print('\n=== 搜索主容器背景 ===')
site_match = re.search(r'<div[^>]+class="[^"]*yy-site[^"]*"[^>]*>', html)
if site_match:
    print(site_match.group())

# 搜索 body 背景
body_match = re.search(r'<body[^>]+style="[^"]*background[^"]*"', html)
if body_match:
    print(f'\nbody 背景: {body_match.group()}')

# 搜索最后几个 section 的背景
print('\n=== 搜索最后一个 section ===')
# 找最后一个 </section> 附近的内容
last_section = html.rfind('</section>')
if last_section > 0:
    area = html[max(0, last_section-300):last_section+200]
    if 'background' in area.lower():
        print('最后一个 section 有背景:')
        print(area)
    else:
        print('最后一个 section 附近区域:')
        print(area[-200:])

# 搜索带有 url() 的 style 属性
print('\n\n=== 搜索所有 url 背景 ===')
url_styles = re.findall(r'style="[^"]*url\([^)]+\)[^"]*"', html, re.IGNORECASE)
if url_styles:
    for s in url_styles:
        print(f'  {s[:200]}')

print('\n检查完成')
