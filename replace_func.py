import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 替换extract_content函数 ===\n")

# 新函数代码
new_func = '''def extract_content(url, html=None, session=None):
    """Extract content from Chinese websites using BeautifulSoup (primary) + trafilatura (fallback)"""
    import requests
    from bs4 import BeautifulSoup
    
    imgs = []
    try:
        # Download if not provided
        if html is None:
            r = (session or requests).get(url, headers={"User-Agent": random.choice(UAS)}, timeout=15)
            html = r.text
        
        # Parse with lxml for better performance
        try:
            soup = BeautifulSoup(html, "lxml")
        except:
            soup = BeautifulSoup(html, "html.parser")
        
        # Remove unwanted elements
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "noscript", "svg"]):
            tag.decompose()
        
        # Try to get title
        title_tag = soup.select_one("title") or soup.select_one("h1") or soup.find("meta", property="og:title")
        if title_tag:
            if hasattr(title_tag, 'get'):
                title = title_tag.get("content", "") or title_tag.get_text(strip=True)
            else:
                title = title_tag.get_text(strip=True)
        else:
            title = ""
        
        # Find content container - Chinese website selectors
        content_selectors = [
            "article",
            '[class*="article"]',
            '[class*="content"]',
            '[class*="post"]',
            '[class*="entry"]',
            '[class*="main"]',
            '[class*="detail"]',
            '[class*="text"]',
            '[id*="article"]',
            '[id*="content"]',
            '[id*="main"]',
            ".rich_media_content",  # 微信文章
            ".article-content",
            ".post-content", 
            ".entry-content",
            ".main-content",
            ".content-wrap",
            ".article-body",
            ".post-body",
        ]
        
        content_elem = None
        for selector in content_selectors:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(separator="\\n", strip=True)
                if len(text) > 300:
                    content_elem = elem
                    break
        
        # If no content container found, get all paragraphs
        if not content_elem:
            paragraphs = soup.find_all("p")
            if paragraphs:
                content_parts = []
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if len(text) > 20:
                        content_parts.append(text)
                if content_parts:
                    content_text = "\\n".join(content_parts)
                else:
                    content_text = soup.get_text(separator="\\n", strip=True)
            else:
                content_text = soup.get_text(separator="\\n", strip=True)
        else:
            content_text = content_elem.get_text(separator="\\n", strip=True)
        
        # Extract images from content
        img_selectors = ["article img", ".content img", ".article img", ".post img", "main img", 
                        ".rich_media_content img", ".article-content img", ".entry-content img",
                        "figure img", "[class*=thumb] img"]
        for selector in img_selectors:
            for img in soup.select(selector)[:5]:
                src = (img.get("data-src") or img.get("data-original") or 
                       img.get("data-lazy-src") or img.get("src") or "")
                if src and not src.startswith("data:") and ("http" in src or src.startswith("//")):
                    if src.startswith("//"):
                        src = "https:" + src
                    imgs.append(src)
        
        # Clean content - remove excessive whitespace
        lines = [l.strip() for l in content_text.split("\\n") if l.strip()]
        content_text = "\\n".join(lines)
        
        # Check minimum length
        min_len = CFG.get("min_content_length", 400)
        if len(content_text) < min_len:
            # Try trafilatura as fallback
            try:
                text = trafilatura.extract(html, output_format="html", include_images=False)
                if text:
                    clean = re.sub(r"<[^>]+>", "", text).strip()
                    if len(clean) > min_len:
                        content_text = clean
                        # Extract images from soup again
                        for img in soup.select("img")[:5]:
                            src = img.get("src") or ""
                            if src and "http" in src and not src.startswith("data:"):
                                imgs.append(src)
            except:
                pass
        
        if title and len(title) > 3 and len(content_text) > 200:
            return {"title": title[:200], "html": content_text[:15000], "imgs": imgs[:5], "url": url}
        
        return None
        
    except Exception as e:
        log.debug("Extract err {}: {}".format(url, e))
        return None

'''

# 读取collector.py
stdin, stdout, stderr = ssh.exec_command("wc -l /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
total_lines = int(stdout.read().decode().strip().split()[0])
print(f"总行数: {total_lines}")

# 找到extract_content函数开始和结束位置
stdin, stdout, stderr = ssh.exec_command("grep -n 'def extract_content' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
start_line = int(stdout.read().decode().strip().split(":")[0])
print(f"函数开始行: {start_line}")

# 找到下一个函数定义
stdin, stdout, stderr = ssh.exec_command(f"sed -n '{start_line+1},{total_lines}p' /www/wwwroot/resource_site/auto_collect/collector.py | grep -n '^def ' | head -1", timeout=10)
result = stdout.read().decode().strip()
if result:
    end_line = start_line + int(result.split(":")[0])
else:
    # 找到 WordPress 类
    stdin, stdout, stderr = ssh.exec_command(f"grep -n '^class ' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
    for line in stdout.read().decode().strip().split("\\n"):
        if line:
            cls_line = int(line.split(":")[0])
            if cls_line > start_line:
                end_line = cls_line
                break

print(f"函数结束行: {end_line}")

# 提取函数前后的代码
stdin, stdout, stderr = ssh.exec_command(f"sed -n '1,{start_line-1}p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
before = stdout.read().decode()

stdin, stdout, stderr = ssh.exec_command(f"sed -n '{end_line},$p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
after = stdout.read().decode()

# 组合新文件
new_content = before + new_func + "\\n" + after

# 写回
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(new_content)
sftp.close()

print("\\n1. extract_content函数已替换")

# 测试
print("\\n2. 测试采集器...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && timeout 180 python3 collector.py 2>&1 | tail -60", timeout=200)
result = stdout.read().decode().strip()
print(result[-2500:])

ssh.close()
