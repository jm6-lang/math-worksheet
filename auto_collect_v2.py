import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 创建自动采集脚本 ===\n")

# 创建采集脚本
collector_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网赚教程自动采集脚本
自动采集RSS内容并发布到WordPress
"""

import feedparser
import requests
import json
import time
import re
from datetime import datetime

# WordPress配置
WP_URL = "https://skillxm.cn/wp-json/wp/v2"
API_TOKEN = "s6eW 2kHy 8yqu XNuY JjoK HHOR"
CATEGORY_ID = 7  # 网赚项目

# RSS源配置 - 网赚教程相关
RSS_FEEDS = [
    {"name": "36氪", "url": "https://www.36kr.com/feed", "category": "创业"},
    {"name": "少数派", "url": "https://sspai.com/feed", "category": "科技"},
    {"name": "IT之家", "url": "https://www.ithome.com/rss/IT", "category": "科技"},
    {"name": "创业邦", "url": "https://www.cyzone.cn/rss/", "category": "创业"},
]

# 已发布链接记录文件
POSTED_FILE = "/www/wwwroot/resource_site/auto_collect/posted_urls.txt"

def load_posted_urls():
    """加载已发布的URL列表"""
    try:
        with open(POSTED_FILE, 'r', encoding='utf-8') as f:
            return set(line.strip() for line in f)
    except:
        return set()

def save_posted_url(url):
    """保存已发布的URL"""
    with open(POSTED_FILE, 'a', encoding='utf-8') as f:
        f.write(url + '\\n')

def clean_html(html):
    """清理HTML标签，提取纯文本"""
    # 移除script和style标签
    html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    # 移除HTML注释
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # 移除多余空白
    html = re.sub(r'\\s+', ' ', html)
    # 转义HTML实体
    html = html.replace('&nbsp;', ' ')
    html = html.replace('&amp;', '&')
    html = html.replace('&lt;', '<')
    html = html.replace('&gt;', '>')
    html = html.replace('&quot;', '"')
    # 移除所有HTML标签
    html = re.sub(r'<[^>]+>', '', html)
    return html.strip()

def post_to_wordpress(title, content, category_id):
    """发布文章到WordPress"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    data = {
        "title": title,
        "content": content,
        "status": "publish",
        "categories": [category_id]
    }
    
    try:
        response = requests.post(
            f"{WP_URL}/posts",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print(f"  ✓ 发布成功: {title[:30]}...")
            return True, result.get('link', '')
        else:
            print(f"  ✗ 发布失败: {response.status_code} - {response.text[:100]}")
            return False, ''
    except Exception as e:
        print(f"  ✗ 错误: {str(e)}")
        return False, ''

def collect_from_rss(feed_info, posted_urls, max_posts=2):
    """从RSS采集内容"""
    print(f"\\n正在采集: {feed_info['name']}...")
    
    try:
        feed = feedparser.parse(feed_info['url'], timeout=10)
        
        if not feed.entries:
            print(f"  无内容")
            return 0
        
        count = 0
        for entry in feed.entries[:max_posts]:
            # 检查是否已发布
            if hasattr(entry, 'link') and entry.link in posted_urls:
                print(f"  - 已发布，跳过: {entry.title[:30]}")
                continue
            
            # 获取内容
            if hasattr(entry, 'summary'):
                content = entry.summary
            elif hasattr(entry, 'content') and entry.content:
                content = entry.content[0].value
            else:
                content = entry.title
            
            # 清理内容
            content = clean_html(content)
            
            if len(content) < 100:
                content = content + f"\\n\\n来源: {entry.link}"
            
            # 添加版权信息
            content = f'''<p>本文内容整理自网络，仅供学习交流使用。</p>
<div class="article-content">{content}</div>
<p>原文链接: <a href="{entry.link}" target="_blank">{entry.link}</a></p>'''
            
            # 发布到WordPress
            title = entry.title if hasattr(entry, 'title') else "无标题"
            success, url = post_to_wordpress(title, content, CATEGORY_ID)
            
            if success:
                posted_urls.add(entry.link)
                save_posted_url(entry.link)
                count += 1
                time.sleep(2)  # 避免请求过快
        
        print(f"  完成: 采集 {count} 篇")
        return count
        
    except Exception as e:
        print(f"  采集失败: {str(e)}")
        return 0

def main():
    """主函数"""
    print("=" * 50)
    print("网赚教程自动采集")
    print("=" * 50)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    posted_urls = load_posted_urls()
    print(f"已发布文章数: {len(posted_urls)}")
    
    total = 0
    for feed in RSS_FEEDS:
        count = collect_from_rss(feed, posted_urls, max_posts=2)
        total += count
        if total >= 6:  # 每天最多6篇
            break
        time.sleep(3)
    
    print("\\n" + "=" * 50)
    print(f"采集完成! 共采集 {total} 篇")
    print("=" * 50)

if __name__ == "__main__":
    main()
'''

# 创建脚本目录
cmd = """mkdir -p /www/wwwroot/resource_site/auto_collect"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)

# 上传脚本
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector_v2.py', 'w') as f:
    f.write(collector_script)
sftp.close()
print("1. 采集脚本已上传")

# 设置权限
cmd = """chmod +x /www/wwwroot/resource_site/auto_collect/collector_v2.py"""
ssh.exec_command(cmd, timeout=10)
print("2. 权限已设置")

# 测试运行
print("\n3. 测试运行...")
cmd = """cd /www/wwwroot/resource_site/auto_collect && /usr/bin/python3 collector_v2.py 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=120)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:3000])

ssh.close()
