import paramiko
import sys
import urllib.request
import re

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Check current theme for structured data
cmd = "grep -r 'schema.org\\|JSON-LD\\|structured-data' /www/wwwroot/resource_site/wp-content/themes/yymarket/*.php 2>/dev/null | head -20"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("=== 当前主题结构化数据 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# Check if Yoast/AllInOneSEO is adding structured data
cmd = "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT option_value FROM wp_options WHERE option_name IN ('yst_google_seo','aioseo_options','wpseo_schema') LIMIT 5;\" 2>/dev/null | head -20"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("\n=== SEO插件配置 ===")
print(stdout.read().decode('utf-8', errors='ignore'))

# Check homepage content structure
req = urllib.request.Request("https://www.skillxm.cn/", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    
    # Check for existing schema
    schemas = re.findall(r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', body, re.DOTALL)
    print("\n=== 当前首页 JSON-LD ===")
    if schemas:
        for s in schemas[:3]:
            print(s[:500])
    else:
        print("无 JSON-LD 结构化数据")
    
    # Check meta tags
    desc = re.search(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', body, re.I)
    keywords = re.search(r'<meta[^>]*name=["\']keywords["\'][^>]*content=["\']([^"\']+)["\']', body, re.I)
    print("\n=== Meta 标签 ===")
    if desc:
        print("description: %s" % desc.group(1)[:80])
    if keywords:
        print("keywords: %s" % keywords.group(1))

ssh.close()
