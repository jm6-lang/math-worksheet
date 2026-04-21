import paramiko
import urllib.request

# 1. 获取目标站结构
print("=== 获取目标站 jichuanglm.cn 结构 ===")
req = urllib.request.Request('https://www.jichuanglm.cn/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
r = urllib.request.urlopen(req, timeout=20)
target_html = r.read().decode('utf-8', errors='ignore')

# 提取关键样式和结构
print(f"目标站页面大小: {len(target_html)}")

# 提取主色调
import re
colors = re.findall(r'(#[0-9a-fA-F]{6}|#[0-9a-fA-F]{3}|rgb\([^)]+\))', target_html)
print(f"发现颜色: {list(set(colors))[:10]}")

# 提取主题样式链接
theme_links = re.findall(r'href="([^"]*theme[^"]*\.css[^"]*)"', target_html)
print(f"主题CSS: {theme_links[:5]}")

# 2. 获取当前站结构
print("\n=== 获取当前站 skillxm.cn 结构 ===")
req2 = urllib.request.Request('https://skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'})
r2 = urllib.request.urlopen(req2, timeout=20)
current_html = r2.read().decode('utf-8', errors='ignore')
print(f"当前站页面大小: {len(current_html)}")

# 3. 提取目标站的关键布局元素
print("\n=== 目标站关键布局 ===")

# Banner区域
banner_start = target_html.find('header-slider')
if banner_start > 0:
    print("发现 Banner/轮播区域")

# 分类图标区
cat_start = target_html.find('widget-graphic-cover')
if cat_start > 0:
    print("发现分类图标区域")
    # 提取分类链接
    cat_section = target_html[cat_start:cat_start+3000]
    cat_links = re.findall(r'href="([^"]*)"[^>]*>\s*<div[^>]*graphic[^>]*>.*?<img[^>]*src="([^"]*)"', cat_section, re.DOTALL)
    print(f"分类图标数量: {len(cat_links)}")

# 文章卡片区
post_start = target_html.find('posts-item')
if post_start > 0:
    print("发现文章卡片区域")

# VIP按钮
vip_btn = target_html.find('开通会员')
if vip_btn > 0:
    print("发现VIP会员按钮")

print("\n完成分析")