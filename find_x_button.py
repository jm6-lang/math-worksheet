import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://www.skillxm.cn/', headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
})
resp = urllib.request.urlopen(req, timeout=20, context=ctx)
html = resp.read().decode('utf-8', errors='replace')

# 查找 X 关闭按钮、右上角按钮、modal、popup 相关代码
import re

print('搜索关闭按钮/X按钮相关代码:')
patterns = [
    (r'class="[^"]*(?:close|btn-close)[^"]*"[^>]*>', 'close button'),
    (r'onclick="[^"]*(?:close|dismiss|hide|remove)[^"]*"', 'onclick close'),
    (r'data-(?:toggle|dismiss|close)[^"]*', 'data-close/dismiss'),
    (r'<button[^>]*>[\s\S]{0,50}X[\s\S]{0,50}</button>', 'button with X text'),
    (r'class="[^"]*(?:modal|popup|overlay|float)[^"]*"', 'modal/popup/overlay'),
    (r'class="[^"]*(?:sidebar|side-panel|drawer)[^"]*"', 'sidebar/drawer'),
    (r'<a[^>]+>[\s]*×[\s]*</a>', '× link'),
    (r'>[\s]*×[\s]*<', '× character'),
]

for pat, desc in patterns:
    matches = re.findall(pat, html, re.IGNORECASE)
    if matches:
        print(f'\n[{desc}] 找到 {len(matches)} 个:')
        for m in matches[:5]:
            print(f'  {m[:150]}')

# 查找 style 中有 fixed/absolute + top/right 的元素
print('\n\n搜索固定定位元素（可能是浮动 X 按钮）:')
fixed_pattern = r'<(\w+)[^>]*(?:style="[^"]*(?:position\s*:\s*(?:fixed|absolute)|top\s*:[^;]+;|right\s*:[^;]+)[^"]*"|class="[^"]*(?:fixed|sticky|float)[^"]*")[^>]*>'
fixed_matches = re.findall(fixed_pattern, html)
if fixed_matches:
    print(f'固定定位元素: {set(fixed_matches)}')
else:
    print('未找到固定定位元素')

# 搜索带 close 类或 onclick 关闭的悬浮元素
print('\n搜索悬浮关闭按钮:')
close_html = re.findall(r'<[^>]+(?:class="[^"]*close[^"]*"|class="[^"]*x-btn[^"]*"|class="[^"]*close-btn[^"]*")[^>]*>', html, re.IGNORECASE)
if close_html:
    for c in close_html:
        print(f'  {c}')
else:
    print('  未找到')

# 搜索所有带 fixed/absolute 定位的 div
print('\n搜索所有固定/绝对定位元素:')
all_pos = re.findall(r'<(\w+)[^>]+style="[^"]*(?:position\s*:\s*(?:fixed|absolute))[^"]*"', html)
if all_pos:
    print(f'定位元素: {set(all_pos)}')
    for p in all_pos:
        # 找到这个元素的完整代码
        pattern = rf'<\w+[^>]+style="[^"]*(?:position\s*:\s*(?:fixed|absolute))[^"]*"[^>]*>.*?</\w+>'
        for m in re.finditer(pattern, html):
            print(f'\n  {m.group()[:300]}')
else:
    print('未找到')

# 查找 onclick 里有 window.location 或 href 跳转
print('\n\n搜索页面跳转代码:')
goto = re.findall(r'onclick="[^"]*(?:location|href|window\.)[^"]*"', html)
if goto:
    for g in goto[:10]:
        print(f'  {g}')

# 搜索 modal 或 popup
print('\n搜索 modal/popup:')
modals = re.findall(r'<div[^>]*class="[^"]*(?:modal|popup|modal-backdrop)[^"]*"[^>]*>', html, re.IGNORECASE)
if modals:
    for m in modals:
        print(f'  {m[:200]}')
else:
    print('  未找到 modal/popup')

print('\n检查完成')
