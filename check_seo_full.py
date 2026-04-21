import paramiko
import sys
import urllib.request
import urllib.parse
import json
import time

sys.stdout.reconfigure(encoding='utf-8')

BAIDU_TOKEN = "zJsDaj5ibt8ZlVgz"

print("=" * 55)
print("百度SEO全面诊断")
print("=" * 55)

# 1. Check indexing status via Baidu API
print("\n[1] 百度索引量 API")
try:
    # Get yesterday's date
    yesterday = time.strftime("%Y%m%d", time.localtime(time.time() - 86400))
    url = "http://openapi.baidu.com/rest/2.0/mtg/s?query=ind%3A%s&resource_id=6002&post_data={}" % yesterday
    # Alternative: use the official API
    api_url = "https://openapi.baidu.com/rest/2.0/mtg/s?query=index&resource_id=6006&post_data={}"
    req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        print("  " + r.read().decode('utf-8', errors='ignore'))
except Exception as e:
    print("  API不可用: %s" % str(e)[:60])

# 2. Check post-sitemap content count
print("\n[2] Sitemap文章数")
for i in range(1, 5):
    try:
        req = urllib.request.Request(
            "https://www.skillxm.cn/post-sitemap%d.xml" % i,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8', errors='ignore')
            import re
            urls = re.findall(r'<url>', body)
            print("  post-sitemap%d.xml: %d 篇" % (i, len(urls)))
    except:
        break

# 3. Check push status
print("\n[3] 百度推送状态")
try:
    # Push a test URL to check quota
    test_url = "https://www.skillxm.cn/\n"
    push_url = "http://data.zz.baidu.com/urls?site=https://www.skillxm.cn&token=%s" % BAIDU_TOKEN
    req = urllib.request.Request(push_url, data=test_url.encode('utf-8'), headers={
        "Content-Type": "text/plain",
        "User-Agent": "Mozilla/5.0"
    })
    with urllib.request.urlopen(req, timeout=10) as r:
        result = json.loads(r.read().decode('utf-8'))
        print("  响应: %s" % json.dumps(result, ensure_ascii=False))
        if 'remain' in result:
            print("  今日剩余推送额度: %d" % result['remain'])
        if 'success' in result:
            print("  本次成功: %d" % result['success'])
except Exception as e:
    print("  Error: %s" % e)

# 4. Check SSL
print("\n[4] HTTPS状态")
try:
    req = urllib.request.Request("https://www.skillxm.cn/", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=10) as r:
        print("  HTTPS: OK")
        # Check for www redirect
        final = r.url
        if "www." in final:
            print("  域名带www: %s" % final)
        else:
            print("  域名: %s" % final)
except Exception as e:
    print("  Error: %s" % e)

# 5. Quick site:skillxm.cn search via a different approach
print("\n[5] 百度收录估算")
try:
    # Use the old baidu search page
    req = urllib.request.Request(
        "https://www.baidu.com/s?wd=site:skillxm.cn&rn=10",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html",
            "Accept-Language": "zh-CN,zh;q=0.9",
        }
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        body = r.read().decode('utf-8', errors='ignore')
        # Look for result count patterns
        patterns = [
            r'百度为您找到相关结果约([\d,]+)个',
            r'找到相关结果约?([\d,]+)',
            r'"resultNum"[^"]*([\d,]+)',
            r'(\d[\d,]*)\s*个相关结果',
        ]
        for p in patterns:
            m = re.search(p, body)
            if m:
                print("  收录数量: %s" % m.group(1))
                break
        else:
            # Check if captcha
            if 'captcha' in body.lower() or '验证' in body:
                print("  被验证码拦截，无法直接查询")
            # Check if results exist
            results = re.findall(r'<h3[^>]*>', body)
            if results:
                print("  搜索结果有 %d 条标题（说明已被收录）" % len(results))
                # Extract titles
                titles = re.findall(r'<h3[^>]*>(.*?)</h3>', body, re.DOTALL)
                for t in titles[:5]:
                    clean = re.sub(r'<[^>]+>', '', t).strip()
                    if clean:
                        print("    - %s" % clean[:60])
            else:
                print("  未检测到搜索结果标题")
                if '未找到' in body:
                    print("  百度提示未找到相关结果")
                else:
                    print("  页面可能被反爬拦截")
except Exception as e:
    print("  Error: %s" % e)

# 6. Check page sitemap
print("\n[6] Page Sitemap")
try:
    req = urllib.request.Request(
        "https://www.skillxm.cn/page-sitemap.xml",
        headers={"User-Agent": "Mozilla/5.0"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        body = r.read().decode('utf-8', errors='ignore')
        urls = re.findall(r'<loc>(.*?)</loc>', body)
        print("  Pages: %d" % len(urls))
        for u in urls:
            print("    %s" % u)
except Exception as e:
    print("  Error: %s" % e)

print("\n" + "=" * 55)
print("建议:")
print("  - 百度新站收录通常需要1-4周")
print("  - 主动推送(已配) + sitemap提交加速收录")
print("  - 每天保持更新有助于提升收录速度")
print("  - 登录百度搜索资源平台查看详细索引数据")
print("  https://ziyuan.baidu.com/")
