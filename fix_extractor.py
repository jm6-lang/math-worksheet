import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 直接修改采集器内容提取逻辑 ===\n")

# 1. 读取当前采集器
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/collector.py", timeout=15)
collector = stdout.read().decode()

# 2. 找到extract_content函数位置并替换
lines = collector.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # 找到extract_content函数定义
    if 'def extract_content(url' in line or 'def trafilatura_extract' in line:
        new_lines.append(line)
        i += 1
        # 跳过旧的函数体
        indent = len(line) - len(line.lstrip())
        while i < len(lines):
            next_line = lines[i]
            if next_line.strip() and len(next_line) - len(next_line.lstrip()) <= indent:
                break
            i += 1
        # 添加新的提取函数
        new_content = '''    """Extract content using multiple methods"""
    import requests
    from bs4 import BeautifulSoup
    
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }
    
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = r.apparent_encoding or 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # 移除无关标签
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
            tag.decompose()
        
        # 中文网站常见内容选择器
        content_selectors = [
            'article',
            '[class*="content"]',
            '[class*="article"]',
            '[class*="post"]',
            '[class*="main"]',
            '[id*="content"]',
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
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = '\\n'.join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 30)
        
        if content and len(content) > 300:
            return content[:15000]
        return None
        
    except Exception as e:
        return None
'''
        new_lines.append(new_content)
        continue
    
    new_lines.append(line)
    i += 1

# 3. 写回
new_collector = '\n'.join(new_lines)
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(new_collector)
sftp.close()
print("1. 采集器内容提取函数已更新")

# 4. 再次测试
print("\n2. 测试采集器...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && timeout 120 python3 collector.py 2>&1 | tail -60", timeout=150)
result = stdout.read().decode().strip()
print(result[-2500:])

# 5. 检查数据库
stdin, stdout, stderr = ssh.exec_command("sqlite3 /www/wwwroot/resource_site/auto_collect/published.db 'SELECT COUNT(*) FROM pub; SELECT MAX(created) FROM pub;'", timeout=10)
print("\n3. 数据库状态:")
print(stdout.read().decode().strip())

ssh.close()
