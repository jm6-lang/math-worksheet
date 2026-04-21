#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网站推广脚本 - 多渠道提交
"""
import urllib.request
import urllib.parse
import ssl
import time
import re
import json

SITE_URL = "https://www.skillxm.cn"
SITEMAP_URL = "https://www.skillxm.cn/sitemap_index.xml"
BAIDU_TOKEN = "zJsDaj5ibt8ZlVgz"

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_urls_from_sitemap():
    """从sitemap获取URL列表"""
    urls = []
    try:
        ctx = create_ssl_context()
        req = urllib.request.Request(SITEMAP_URL, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            xml = r.read().decode('utf-8', errors='ignore')
        
        # 提取所有URL
        urls = re.findall(r'<loc>(.*?)</loc>', xml)
        print(f"  从sitemap获取到 {len(urls)} 个URL")
    except Exception as e:
        print(f"  获取sitemap失败: {e}")
    return urls

def push_to_baidu(urls):
    """推送URL到百度"""
    if not urls:
        return False
    
    # 只推送前100个（百度限制）
    urls_to_push = urls[:100]
    print(f"  推送 {len(urls_to_push)} 个URL到百度...")
    
    try:
        data = "\n".join(urls_to_push)
        url = f"http://data.zz.baidu.com/urls?site={SITE_URL}&token={BAIDU_TOKEN}"
        
        req = urllib.request.Request(url, 
            data=data.encode('utf-8'),
            headers={
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "text/plain"
            })
        
        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            result = r.read().decode('utf-8')
        
        print(f"  百度结果: {result}")
        return True
    except Exception as e:
        print(f"  百度推送失败: {e}")
        return False

def submit_to_google():
    """提交sitemap到Google"""
    try:
        sitemap_url = "https://www.google.com/ping?sitemap=" + urllib.parse.quote(SITEMAP_URL)
        req = urllib.request.Request(sitemap_url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            if r.status == 200:
                print("  ✅ Google Sitemap提交成功")
                return True
    except Exception as e:
        print(f"  Google提交失败: {e}")
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
            if r.status == 200:
                print("  ✅ Bing Sitemap提交成功")
                return True
    except Exception as e:
        print(f"  Bing提交失败: {e}")
    return False

def submit_to_360():
    """提交sitemap到360搜索"""
    try:
        url = f"http://zhanzhang.360.cn/url_submit/url_submit.php"
        data = urllib.parse.urlencode({
            "url": SITEMAP_URL
        }).encode('utf-8')
        
        req = urllib.request.Request(url, data=data, headers={
            "User-Agent": "Mozilla/5.0"
        })
        
        with urllib.request.urlopen(req, timeout=15) as r:
            result = r.read().decode('utf-8')
            print(f"  360搜索结果: {result}")
            return True
    except Exception as e:
        print(f"  360搜索提交失败: {e}")
    return False

def submit_to_sogou():
    """提交sitemap到搜狗"""
    try:
        sogou_url = f"https://www.sogou.com/webrobot/imgs?url={urllib.parse.quote(SITE_URL)}&docid={urllib.parse.quote(SITEMAP_URL)}&te"
        req = urllib.request.Request(sogou_url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        ctx = create_ssl_context()
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            print(f"  ✅ 搜狗提交完成")
            return True
    except Exception as e:
        print(f"  搜狗提交失败: {e}")
    return False

def submit_to_directories():
    """提交到网址导航/目录"""
    directories = [
        # hao123网址之家
        ("hao123", "https://site.hao123.com/add?url=" + urllib.parse.quote(SITE_URL) + "&info=" + urllib.parse.quote("小二郎资源网 - 互联网项目教程，提供副业赚钱教程、创业项目、电商运营教程等资源")),
    ]
    
    results = []
    for name, url in directories:
        try:
            print(f"  正在提交到 {name}...")
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0"
            })
            ctx = create_ssl_context()
            with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
                print(f"    ✅ {name} 提交完成")
                results.append(name)
        except Exception as e:
            print(f"    ⚠️ {name} 提交失败: {str(e)[:50]}")
        time.sleep(1)
    
    return results

def main():
    print("="*60)
    print("网站推广脚本 - skillxm.cn")
    print("="*60)
    
    # 1. 获取URL列表
    print("\n[1/5] 获取网站URL...")
    urls = fetch_urls_from_sitemap()
    if not urls:
        print("  获取URL失败，退出")
        return
    
    # 2. 百度推送
    print("\n[2/5] 百度搜索推送...")
    push_to_baidu(urls)
    
    # 3. 搜索引擎Sitemap提交
    print("\n[3/5] 提交Sitemap到搜索引擎...")
    submit_to_google()
    submit_to_bing()
    submit_to_360()
    submit_to_sogou()
    
    # 4. 网址导航提交
    print("\n[4/5] 提交到网址导航...")
    submit_to_directories()
    
    # 5. 完成
    print("\n" + "="*60)
    print("✅ 推广完成！")
    print("="*60)
    print("\n建议手动操作:")
    print("1. Google Search Console: https://search.google.com/search-console")
    print("2. 百度搜索资源平台: https://ziyuan.baidu.com")
    print("3. 搜狗站长平台: https://zhanzhang.sogou.com")
    print("4. 360站长平台: https://zhanzhang.360.cn")

if __name__ == "__main__":
    main()
