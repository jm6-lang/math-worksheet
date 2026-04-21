import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

print("=== Bing site:skillxm.cn 详细 ===\n")
try:
    req = urllib.request.Request(
        "https://www.bing.com/search?q=site%3Askillxm.cn&count=20",
        headers=headers
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        body = r.read().decode('utf-8', errors='ignore')
        
        # Better result count extraction
        count_match = re.search(r'id="b_tween"[^>]*>.*?of\s*([\d,]+)\s*results', body, re.DOTALL)
        if not count_match:
            count_match = re.search(r'class="sb_count"[^>]*>([^<]*)</', body)
        
        if count_match:
            print("Bing显示: %s\n" % count_match.group(1).strip())
        
        # Extract ALL skillxm.cn URLs from page
        all_urls = re.findall(r'https?://(?:www\.)?skillxm\.cn[^\s"\'<>]*', body)
        # Deduplicate
        unique = list(dict.fromkeys(all_urls))
        
        print("页面中出现的 skillxm.cn URL (%d个):\n" % len(unique))
        for url in unique[:20]:
            print("  %s" % url)
        
        if not unique:
            # Try to see if there are any results at all
            if 'b_algo' in body:
                print("页面有搜索结果，但没有 skillxm.cn 的链接")
                # Extract what URLs are there
                all_links = re.findall(r'<a[^>]*href="([^"]*)"', body)
                for link in all_links[:10]:
                    print("  实际链接: %s" % link[:80])
            else:
                print("页面没有搜索结果")
                # Show part of body for debug
                clean = re.sub(r'<[^>]+>', ' ', body)
                clean = re.sub(r'\s+', ' ', clean)
                print("  页面摘要: %s" % clean[:500])

except Exception as e:
    print("Error: %s" % e)

# Also try direct fetch of a specific post to see if it's indexable
print("\n=== 文章页HTTP检查 ===\n")
test_urls = [
    "https://www.skillxm.cn/",
    "https://www.skillxm.cn/?p=1812",
    "https://www.skillxm.cn/?p=1822",
]
for url in test_urls:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            status = r.status
            length = len(r.read())
            print("  %s => HTTP %d (%d bytes)" % (url, status, length))
    except Exception as e:
        print("  %s => Error: %s" % (url, str(e)[:50]))
