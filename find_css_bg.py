import urllib.request, ssl, re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 获取 style.css
req_css = urllib.request.Request('https://www.skillxm.cn/wp-content/themes/yymarket/style.css')
resp_css = urllib.request.urlopen(req_css, timeout=15, context=ctx)
css = resp_css.read().decode('utf-8', errors='replace')

print('=== style.css 中的背景相关样式 ===\n')

# 搜索所有 background-image
bg_images = re.findall(r'[^{]+\{[^{}]*background-image\s*:[^;]+url\([^)]+\)[^}]*\}', css, re.IGNORECASE)
if bg_images:
    print(f'[背景图片] 找到 {len(bg_images)} 个:')
    for b in bg_images[:10]:
        print(f'  {b[:250]}')
else:
    print('  style.css 中无 background-image')

# 搜索 body/html 背景
print('\n=== body/html 背景 ===')
body_html = re.findall(r'(?:^html|^body)[^{]*\{[^}]*background[^}]*\}', css, re.IGNORECASE | re.MULTILINE)
if body_html:
    for bh in body_html[:5]:
        print(f'  {bh[:300]}')
else:
    print('  未找到')

# 搜索 yy-site 背景
print('\n=== .yy-site 背景 ===')
yy_site = re.findall(r'\.yy-site[^{]*\{[^}]*background[^}]*\}', css, re.IGNORECASE)
if yy_site:
    for y in yy_site[:3]:
        print(f'  {y[:300]}')
else:
    print('  未找到')

# 搜索 footer 背景
print('\n=== footer 背景 ===')
footer_bg = re.findall(r'(?:^|\s)(?:footer|yy-footer)[^.#]*\{[^}]*background[^}]*\}', css, re.IGNORECASE | re.MULTILINE)
if footer_bg:
    for f in footer_bg[:3]:
        print(f'  {f[:300]}')
else:
    print('  未找到')

# 所有 url 资源
print('\n\n=== 所有图片/视频 url ===')
all_urls = re.findall(r'url\([^)]+\)', css)
unique = list(dict.fromkeys(all_urls))
for u in unique:
    if any(ext in u.lower() for ext in ['.jpg','.jpeg','.png','.gif','.webp','.svg','.mp4','.webm']):
        print(f'  {u}')

print('\n检查完成')
