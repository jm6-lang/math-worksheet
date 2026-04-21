#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站推广脚本 - 多渠道提交 (优化版)
"""
import urllib.request
import urllib.parse
import ssl
import time
import re
import sys

# 设置输出编码
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

SITE_URL = "https://www.skillxm.cn"
SITEMAP_URL = "https://www.skillxm.cn/sitemap_index.xml"
BAIDU_TOKEN = "zJsDaj5ibt8ZlVgz"

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_all_urls():
    """递归获取所有sitemap中的URL"""
    all_urls = []
    visited = set()
    
    def fetch_sitemap(url):
        if url in visited:
            return
        visited.add(url)
        
        try:
            ctx = create_ssl_context()
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
                xml = r.read().decode('utf-8', errors='ignore')
            
            # 检查是sitemap index还是urlset
            if '<sitemapindex' in xml:
                # 获取子sitemap
                sub_sitemaps = re.findall(r'<loc>(.*?)</loc>', xml)
                for sub in sub_sitemaps:
                    fetch_sitemap(sub)
            else:
                # 获取URL
                urls = re.findall(r'<loc>(.*?)</loc>', xml)
                all_urls.extend(urls)
                
        except Exception as e:
            print(f"    Error fetching {url}: {e}")
    
    print("  Fetching sitemap_index...")
    fetch_sitemap(SITEMAP_URL)
    print(f"  Total URLs found: {len(all_urls)}")
    return all_urls

def push_to_baidu(urls):
    """推送URL到百度"""
    if not urls:
        return False
    
    # 分批推送，每批2000个
    batch_size = 2000
    for i in range(0, min(len(urls), 10000), batch_size):
        batch = urls[i:i+batch_size]
        print(f"  Pushing batch {i//batch_size + 1}: {len(batch)} URLs...")
        
        try:
            data = "\n".join(batch)
            api_url = f"http://data.zz.baidu.com/urls?site={SITE_URL}&token={BAIDU_TOKEN}"
            
            req = urllib.request.Request(api_url, 
                data=data.encode('utf-8'),
                headers={
                    "User-Agent": "curl/7.68.0",
                    "Content-Type": "text/plain"
                })
            
            with urllib.request.urlopen(req, timeout=20) as r:
                result = r.read().decode('utf-8')
                print(f"    Result: {result}")
                
        except Exception as e:
            print(f"    Push failed: {e}")
            break
        
        time.sleep(1)
    
    return True

def submit_to_baidu_zz():
    """使用百度站长平台API"""
    print("\n[2b] Submitting to Baidu Ziyuan...")
    try:
        # 百度主动推送API
        url = f"http://data.zz.baidu.com/urls?site={SITE_URL}&token={BAIDU_TOKEN}"
        data = SITEMAP_URL  # 直接推送sitemap地址
        
        req = urllib.request.Request(url, 
            data=data.encode('utf-8'),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "text/plain"
            })
        
        with urllib.request.urlopen(req, timeout=15) as r:
            result = r.read().decode('utf-8')
            print(f"  Baidu Sitemap: {result}")
    except Exception as e:
        print(f"  Baidu submit failed: {e}")

def submit_to_google():
    """提交sitemap到Google"""
    print("\n[3] Submitting Sitemap to search engines...")
    try:
        sitemap_param = urllib.parse.quote(SITEMAP_URL)
        google_url = f"https://www.google.com/ping?sitemap={sitemap_param}"
        
        req = urllib.request.Request(google_url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            print(f"  [OK] Google Sitemap submitted")
            return True
    except Exception as e:
        print(f"  [FAIL] Google: {e}")
    return False

def submit_to_bing():
    """提交sitemap到Bing"""
    try:
        bing_url = f"https://www.bing.com/ping?sitemap={urllib.parse.quote(SITEMAP_URL)}"
        req = urllib.request.Request(bing_url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            print(f"  [OK] Bing Sitemap submitted")
            return True
    except Exception as e:
        print(f"  [FAIL] Bing: {e}")
    return False

def main():
    print("=" * 60)
    print("Website Promotion - skillxm.cn")
    print("=" * 60)
    
    # Step 1: Get all URLs
    print("\n[1] Fetching all URLs from sitemap...")
    urls = fetch_all_urls()
    
    if not urls:
        print("  Failed to get URLs!")
        return
    
    # Step 2: Baidu push
    print("\n[2] Pushing to Baidu...")
    push_to_baidu(urls)
    
    # Step 3: Search engine submissions
    submit_to_google()
    submit_to_bing()
    
    # Summary
    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)
    print(f"\nTotal URLs: {len(urls)}")
    print(f"\nManual steps:")
    print("1. Google: https://search.google.com/search-console")
    print("2. Baidu: https://ziyuan.baidu.com")
    print("3. Sogou: https://zhanzhang.sogou.com")
    print("4. 360: https://zhanzhang.360.cn")

if __name__ == "__main__":
    main()
