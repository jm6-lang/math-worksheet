import paramiko
import sys
import urllib.request
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Check for caching plugins
cmd = "ls /www/wwwroot/resource_site/wp-content/plugins/ 2>/dev/null | grep -i cache"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
plugins = stdout.read().decode('utf-8', errors='ignore')
print("Caching plugins: %s" % plugins.strip() or "none")

# Check for wp-config.php caching settings
cmd = "grep -i 'WP_CACHE\\|SUPER_CACHE\\|W3TC' /www/wwwroot/resource_site/wp-config.php 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
cache_config = stdout.read().decode('utf-8', errors='ignore')
print("Cache config: %s" % cache_config.strip() or "none")

ssh.close()

# Test with cache bypass query string
print("\n=== Testing with cache bypass ===")
urls_to_test = [
    "https://www.skillxm.cn/?p=1812&nocache=1",
    "https://www.skillxm.cn/?p=1812&t=%d" % int(__import__('time').time()),
]

for url in urls_to_test:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8', errors='ignore')
            
            if 'GEO Structured Data' in body:
                print("%s: GEO FOUND!" % url)
                break
            else:
                schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
                print("%s: JSON-LD=%d" % (url, len(schemas)))
    except Exception as e:
        print("%s: ERROR - %s" % (url, str(e)[:50]))

# If still not working, let's inject directly into header instead of footer
# And use direct output buffering at init
print("\n=== Alternative: Direct injection via theme footer ===")
