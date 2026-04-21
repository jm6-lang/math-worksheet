import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 创建新的extract_content函数 ===\n")

# 新函数
new_extract_func = '''def extract_content(url, html=None, session=None):
    """Extract content using BeautifulSoup (primary) + trafilatura (fallback)"""
    import requests
    from bs4 import BeautifulSoup
    
    imgs = []
    try:
        if html is None:
            r = (session or requests).get(url, headers={"User-Agent": random.choice(UAS)}, timeout=15)
            html = r.text
        
        try:
            soup = BeautifulSoup(html, "lxml")
        except:
            soup = BeautifulSoup(html, "html.parser")
        
        for tag in soup(["script", "style", "nav", "header", "footer", "aside", "iframe", "noscript"]):
            tag.decompose()
        
        title_tag = soup.select_one("title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        
        content_selectors = [
            "article", "[class*=article]", "[class*=content]", "[class*=post]",
            "[class*=entry]", "[class*=main]", "[class*=detail]", "[class*=text]",
            "[id*=article]", "[id*=content]", "[id*=main]", ".rich_media_content",
            ".article-content", ".post-content", ".entry-content", ".main-content",
        ]
        
        content_text = ""
        for selector in content_selectors:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(separator="\\n", strip=True)
                if len(text) > 300:
                    content_text = text
                    break
        
        if not content_text:
            paragraphs = soup.find_all("p")
            content_parts = [p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20]
            content_text = "\\n".join(content_parts)
        
        for img in soup.select("article img, .content img, main img, .article img")[:5]:
            src = img.get("data-src") or img.get("data-original") or img.get("src") or ""
            if src and "http" in src and not src.startswith("data:"):
                if src.startswith("//"): src = "https:" + src
                imgs.append(src)
        
        lines = [l.strip() for l in content_text.split("\\n") if l.strip()]
        content_text = "\\n".join(lines)
        
        min_len = CFG.get("min_content_length", 400)
        if len(content_text) < min_len:
            try:
                text = trafilatura.extract(html, output_format="html", include_images=False)
                if text:
                    clean = re.sub(r"<[^>]+>", "", text).strip()
                    if len(clean) > min_len:
                        content_text = clean
            except: pass
        
        if title and len(title) > 3 and len(content_text) > 200:
            return {"title": title[:200], "html": content_text[:15000], "imgs": imgs[:5], "url": url}
        return None
    except Exception as e:
        log.debug("Extract err {}: {}".format(url, e))
        return None

'''

# 1. 获取extract_content前后的代码
stdin, stdout, stderr = ssh.exec_command("sed -n '1,138p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
before = stdout.read().decode()

stdin, stdout, stderr = ssh.exec_command("sed -n '196,$p' /www/wwwroot/resource_site/auto_collect/collector.py", timeout=10)
after = stdout.read().decode()

# 2. 组合
new_collector = before + new_extract_func + "\\n" + after

# 3. 写回
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(new_collector)
sftp.close()

print("1. extract_content函数已替换")

# 4. 测试
print("\\n2. 测试采集器（2分钟）...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && timeout 120 python3 collector.py 2>&1 | grep -E 'INFO|Skip|published|Error|content|Extracted'", timeout=150)
result = stdout.read().decode().strip()
print(result[-3000:] if len(result) > 3000 else result)

# 5. 检查数据库
stdin, stdout, stderr = ssh.exec_command("sqlite3 /www/wwwroot/resource_site/auto_collect/published.db 'SELECT COUNT(*) FROM pub; SELECT MAX(created) FROM pub;'", timeout=10)
print("\\n3. 数据库:", stdout.read().decode().strip())

ssh.close()
