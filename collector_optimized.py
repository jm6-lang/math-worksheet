#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版自动采集器 - 副业赚钱教程
增强版：更多RSS源 + 更宽松的过滤 + 更好的日志
"""
import feedparser
import subprocess
import time
import re
import os
import json
import urllib.request
import ssl
from datetime import datetime

WP_PATH = "/www/wwwroot/resource_site"
CATEGORY_ID = 53  # 网赚项目
MAX_POSTS = 10  # 每次采集数量
PUBLISHED_FILE = os.path.join(os.path.dirname(__file__), "published.json")
LOG_FILE = os.path.join(os.path.dirname(__file__), "collector.log")
BAIDU_TOKEN = "zJsDaj5ibt8ZlVgz"
BAIDU_PUSH_URL = "http://data.zz.baidu.com/urls?site=https://www.skillxm.cn&token=" + BAIDU_TOKEN

# 扩展RSS源 - 副业赚钱相关
RSS_FEEDS = [
    # 创业网赚
    "https://www.cyzone.cn/rss/",
    "https://www.woshipm.com/feed",
    "https://www.aiyingli.com/feed",
    "https://sspai.com/feed",
    "https://www.v2ex.com/index.xml",
    # 短视频电商
    "https://www.yizhiw.tv/feed",
    "https://www.dsguang.com/feed",
    # 追加更多源
    "https://www.zuoxi.com/feed",
    "https://www.53shop.com/rss",
]

# 正面关键词 - 更宽松
POSITIVE_KW = [
    "副业", "赚钱", "网赚", "兼职", "创业", "项目", "教程", "变现", "收入", "盈利", "利润",
    "引流", "私域", "自媒体", "短视频", "直播", "电商", "拼多多", "抖音", "快手", "视频号",
    "闲鱼", "小红书", "公众号", "流量", "运营", "SEO", "带货", "知识付费", "付费社群",
    "AI赚钱", "AI变现", "GPT", "ChatGPT", "AIGC", "被动收入", "理财", "投资", "基金",
    "接单", "自由职业", "远程办公", "获客", "转化", "成交", "裂变", "社群", "营销",
    "暴富", "搞钱", "日入", "月入", "利润", "红利", "风口", "赛道", "需求", "痛点",
    "商业模式", "盈利模式", "赚钱模式", "低成本", "轻创业", "副业收入", "兼职赚钱",
]

# 负面关键词 - 过滤掉
NEGATIVE_KW = [
    "融资", "上市", "IPO", "财报", "裁员", "年报", "股价", "市值", "股票",
    "涨停", "跌停", "股市", "A股", "港股", "美股", "机器人", "芯片", "半导体",
    "新能源车", "锂电池", "光伏", "房地产", "学区房", "限购", "贷款", "信用卡",
    "期货", "外汇", "加密货币", "比特币", "区块链", "虚拟币", "元宇宙", "Web3",
]

# Unsplash图片
THUMB_IMAGES = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1537432376149-e8937dfb6564?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=500&fit=crop",
]

def log(msg):
    """写日志"""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except:
        pass

def load_published():
    try:
        with open(PUBLISHED_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except:
        return set()

def save_published(urls):
    with open(PUBLISHED_FILE, "w", encoding="utf-8") as f:
        json.dump(list(urls), f)

def clean_html(html):
    if not html:
        return ""
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
    html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    html = re.sub(r"<[^>]+>", " ", html)
    html = re.sub(r"\s+", " ", html)
    return html.strip()[:2000]  # 限制长度

def is_relevant(title, content=""):
    """检查文章是否与副业赚钱相关"""
    title = title.lower()
    content = (content or "").lower()
    
    # 负面过滤 - 标题中有直接跳过
    for kw in NEGATIVE_KW:
        if kw.lower() in title:
            return False
    
    # 正面匹配 - 标题或内容中有即可
    for kw in POSITIVE_KW:
        if kw.lower() in title:
            return True
        if kw.lower() in content[:500]:  # 只检查前500字提高效率
            return True
    
    return False

COPYRIGHT_PATTERNS = [
    r"未经.*许可.*禁止转载",
    r"未经作者许可.*禁止转载",
    r"未经授权.*转载",
    r"谢绝转载",
    r"严禁转载",
    r"版权所有",
    r"转载需.*授权",
    r"本文.*原创",
    r"原创.*必究",
]

def has_copyright_restriction(text):
    if not text:
        return False
    for pattern in COPYRIGHT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

def download_image(url, filepath):
    """下载图片，带SSL验证跳过"""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
            d = r.read()
            if len(d) < 5000:
                raise Exception("too small")
            with open(filepath, "wb") as f:
                f.write(d)
            return True
    except Exception as e:
        log(f"  下载图片失败: {e}")
        try:
            fb = "https://placehold.co/800x500/2563eb/ffffff?text=Resource"
            req = urllib.request.Request(fb, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                with open(filepath, "wb") as f:
                    f.write(r.read())
            return True
        except:
            return False

def set_thumbnail(post_id):
    """下载图片并设置为缩略图"""
    idx = int(post_id) % len(THUMB_IMAGES)
    url = THUMB_IMAGES[idx]
    tmp = f"/tmp/th_{post_id}.jpg"
    
    if not download_image(url, tmp):
        return
    
    try:
        # 导入图片
        ci = f'cd {WP_PATH} && wp media import "{tmp}" --porcelain --allow-root 2>/dev/null'
        ri = subprocess.run(ci, shell=True, capture_output=True, text=True, timeout=30)
        mid = ri.stdout.strip()
        
        if mid and mid.isdigit():
            # 设置缩略图
            ct = f'cd {WP_PATH} && wp post meta update {post_id} _thumbnail_id {mid} --allow-root 2>/dev/null'
            subprocess.run(ct, shell=True, capture_output=True, timeout=10)
            log(f"  已设置缩略图: {mid}")
    except Exception as e:
        log(f"  设置缩略图失败: {e}")
    
    try:
        os.remove(tmp)
    except:
        pass

def fetch_article_content(url):
    """抓取文章详细内容"""
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
        with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
            html = r.read().decode('utf-8', errors='ignore')
        
        # 提取主要内容 - 简单方法
        # 移除脚本和样式
        html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.DOTALL)
        html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.DOTALL)
        html = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
        
        # 提取article或main标签内容
        match = re.search(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
        if not match:
            match = re.search(r'<main[^>]*>(.*?)</main>', html, re.DOTALL)
        if not match:
            match = re.search(r'<div class=["\']content["\'][^>]*>(.*?)</div>', html, re.DOTALL)
        
        if match:
            content = match.group(1)
        else:
            # 取body内容
            match = re.search(r'<body[^>]*>(.*?)</body>', html, re.DOTALL)
            content = match.group(1) if match else html
        
        # 清理HTML
        content = clean_html(content)
        return content[:3000]  # 限制长度
        
    except Exception as e:
        log(f"  抓取内容失败: {e}")
        return ""

def wp_post(title, content, cat_id):
    """发布文章到WordPress"""
    content_file = "/tmp/wp_post_content.txt"
    with open(content_file, "w", encoding="utf-8") as f:
        f.write(content)

    safe_title = title.replace("\\", "\\\\").replace('"', '\\"')
    cmd = (
        f'cd {WP_PATH} && '
        'wp post create '
        f'--post_type=post '
        f'--post_title="{safe_title}" '
        '--post_content="$(cat %s)" '
        f"--post_category={cat_id} "
        "--post_status=publish "
        "--allow-root 2>&1"
    ) % content_file
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        output = result.stdout + result.stderr
        
        if "Success" in output or "Created post" in output:
            m = re.search(r"Created post (\d+)", output)
            if m:
                post_id = m.group(1)
                log(f"  发布成功: #{post_id}")
                return True, post_id
        else:
            log(f"  WP错误: {output[:100]}")
            return False, ""
    except Exception as e:
        log(f"  发布异常: {e}")
        return False, ""

def push_baidu(urls):
    """推送URL到百度"""
    if not urls:
        return
    try:
        with open("/tmp/baidu_push.txt", "w") as f:
            f.write("\n".join(urls))
        cmd = f'curl -s --data-binary @/tmp/baidu_push.txt "{BAIDU_PUSH_URL}" -H "Content-Type:text/plain"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.stdout.strip():
            log(f"  百度推送: {result.stdout.strip()[:50]}")
    except Exception as e:
        log(f"  百度推送失败: {e}")

def main():
    log("="*50)
    log("开始采集 (优化版)")
    
    published = load_published()
    log(f"已发布缓存: {len(published)} 条")

    new_urls = []
    total_found = 0
    total_published = 0

    for rss_url in RSS_FEEDS:
        source_name = rss_url.split("/")[2] if "//" in rss_url else rss_url[:30]
        log(f"\n正在检查: {source_name}")
        
        try:
            feed = feedparser.parse(rss_url, request_headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })
            
            if not feed.entries:
                log("  无内容")
                continue
            
            log(f"  获取到 {len(feed.entries)} 条")
            
            # 检查更多条目
            for entry in feed.entries[:15]:  # 从5条增加到15条
                link = getattr(entry, "link", "")
                if not link or link in published:
                    continue
                
                title = getattr(entry, "title", "无标题")
                summary = clean_html(getattr(entry, "summary", ""))
                
                # 关键词过滤
                if not is_relevant(title, summary):
                    continue
                
                total_found += 1
                log(f"  相关: {title[:40]}...")
                
                # 抓取完整内容
                content = fetch_article_content(link)
                
                if not content or len(content) < 100:
                    log("  内容太少，跳过")
                    continue
                
                # 检查版权
                if has_copyright_restriction(content):
                    log("  有版权声明，跳过")
                    published.add(link)
                    continue
                
                # 发布
                success, post_id = wp_post(title, content, CATEGORY_ID)
                
                if success and post_id:
                    # 设置缩略图
                    set_thumbnail(post_id)
                    
                    new_urls.append(link)
                    published.add(link)
                    total_published += 1
                    
                    # 达到目标数量
                    if total_published >= MAX_POSTS:
                        break
                
                time.sleep(1)  # 避免请求过快
            
            if total_published >= MAX_POSTS:
                break
                
        except Exception as e:
            log(f"  错误: {e}")
            continue

    # 保存已发布URL
    save_published(published)
    
    # 百度推送
    if new_urls:
        push_baidu(new_urls)
    
    log(f"\n完成! 相关:{total_found} 发布:{total_published}")

if __name__ == "__main__":
    main()
