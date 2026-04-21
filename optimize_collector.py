import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 优化采集器 - 中文内容提取 ===\n")

# 1. 读取当前采集器脚本
stdin, stdout, stderr = ssh.exec_command("wc -l /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
print("1. 当前采集器行数:", stdout.read().decode().strip())

# 2. 创建中文内容提取函数
chinese_extractor = '''#!/usr/bin/env python3
"""Chinese content extractor for auto-collector"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
}

def extract_content(url, timeout=15):
    """Extract article content from Chinese websites"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.encoding = r.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 移除脚本和样式
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside']):
            tag.decompose()
        
        # 尝试多种文章容器选择器
        content_selectors = [
            'article',
            '[class*="content"]',
            '[class*="article"]',
            '[class*="post"]',
            '[id*="content"]',
            '[id*="article"]',
            '.entry-content',
            '.post-content',
            '.article-content',
            '.main-content',
        ]
        
        content = None
        for selector in content_selectors:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(separator='\\n', strip=True)
                if len(text) > 200:
                    content = text
                    break
        
        if not content:
            # 尝试获取所有段落
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = '\\n'.join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 50)
        
        if content and len(content) > 200:
            return content[:15000]  # 限制长度
        return None
        
    except Exception as e:
        print(f"提取失败: {e}")
        return None

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        content = extract_content(url)
        if content:
            print(content[:500])
        else:
            print("提取失败")
'''

# 3. 上传中文提取器
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/chinese_extractor.py', 'w') as f:
    f.write(chinese_extractor)
sftp.close()
print("2. 中文内容提取器已创建")

# 4. 测试提取器
print("\n3. 测试中文提取器...")
test_urls = [
    "https://www.36kr.com/p/2802345785685255",
    "https://www.ifeng.com/",
]

for url in test_urls[:1]:
    stdin, stdout, stderr = ssh.exec_command(f"cd /www/wwwroot/resource_site/auto_collect && python3 chinese_extractor.py '{url}'", timeout=30)
    result = stdout.read().decode().strip()
    print(f"   {url[:40]}...: {'成功' if result and '提取失败' not in result else '失败'}")
    if result and '提取失败' not in result:
        print(f"   内容预览: {result[:200]}...")

# 5. 更新配置，添加中文友好RSS源
new_rss_feeds = [
    "https://www.36kr.com/feed",
    "https://sspai.com/feed",
    "https://rsshub.app/zhihu/hotlist",
    "https://rsshub.app/ithome/ranking/daily",
    "https://www.zaobao.com.sg/rss/realtime/china",
    "https://www.admin5.com/rss/",  # A5站长网
    "https://www.chinaz.com/news/rss.php",  # 站长之家
    "https://feed.yixies.com/",  # 互联网的一些事
    "https://www.a.com.cn/rss.xml",  # A5创业网
]

stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/config.json", timeout=10)
config = json.loads(stdout.read().decode().strip())
config['rss_feeds'] = new_rss_feeds
config['min_content_length'] = 300  # 降低要求

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/config.json', 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
sftp.close()
print("\n4. 配置已更新 - 添加更多中文RSS源")

ssh.close()
print("\n=== 优化完成 ===")
