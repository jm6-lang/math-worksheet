import urllib.request
import re

req = urllib.request.Request('https://skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0'})
r = urllib.request.urlopen(req, timeout=20)
html = r.read().decode('utf-8', errors='ignore')

# 提取完整的导航区域
nav_start = html.find('id="menus"')
if nav_start > 0:
    nav_end = html.find('</div>', nav_start + 500)
    nav_section = html[nav_start:nav_end+6]
    
    print("=== 导航菜单区域 ===")
    # 提取所有链接
    links = re.findall(r'<a[^>]*href="([^"]*)"[^>]*>([^<]*)</a>', nav_section)
    for href, text in links:
        if href and text:
            print(f"  {text.strip()} -> {href}")

# 检查页面主体结构
print("\n=== 页面主体结构 ===")
print(f"有轮播/Banner: {'carousel' in html.lower() or 'slider' in html.lower()}")
print(f"有搜索框: {'search' in html.lower()}")
print(f"有文章列表: {'post-item' in html}")
print(f"有侧边栏: {'sidebar' in html.lower()}")

# 检查是否有重复元素
print("\n=== 重复元素检查 ===")
h1_count = html.count('<h1')
h2_count = html.count('<h2')
print(f"H1标签数: {h1_count}")
print(f"H2标签数: {h2_count}")

# 检查分类
print("\n=== 分类检查 ===")
cat_links = re.findall(r'/category/([^/"\']+)', html)
unique_cats = list(set(cat_links))
print(f"发现的分类: {unique_cats}")