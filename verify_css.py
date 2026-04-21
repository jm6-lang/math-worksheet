import urllib.request

# 检查CSS文件是否可访问
try:
    req = urllib.request.Request('https://skillxm.cn/wp-content/themes/puock/assets/css/custom-style.css', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=15)
    css_content = r.read().decode('utf-8')
    print(f"CSS文件可访问: {len(css_content)} bytes")
    print(f"内容预览: {css_content[:200]}")
except Exception as e:
    print(f"CSS文件访问失败: {e}")

# 检查首页是否引用了自定义CSS
try:
    req = urllib.request.Request('https://skillxm.cn/', headers={'User-Agent': 'Mozilla/5.0'})
    r = urllib.request.urlopen(req, timeout=15)
    html = r.read().decode('utf-8', errors='ignore')
    print(f"\n首页大小: {len(html)}")
    print(f"引用自定义CSS: {'custom-style.css' in html}")
    
    # 检查主要样式元素
    print(f"\n样式检查:")
    print(f"- 导航栏: {'navbar' in html}")
    print(f"- 文章卡片: {'post-item' in html}")
    print(f"- 分类图标: {'graphic' in html}")
except Exception as e:
    print(f"首页访问失败: {e}")