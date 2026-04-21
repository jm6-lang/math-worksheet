import paramiko
import sys
import urllib.request
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Clear WP Super Cache
print("Clearing WP Super Cache...")
cmd = "cd /www/wwwroot/resource_site && wp cache flush --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("WP cache flush: %s" % stdout.read().decode().strip())

# Also delete cache files directly
cmd = "rm -rf /www/wwwroot/resource_site/wp-content/cache/wp-super-cache/* 2>/dev/null && echo 'Super cache cleared'"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("%s" % stdout.read().decode().strip())

ssh.close()

# Now verify with normal URL (no cache bypass)
import time
time.sleep(2)
req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("\nArticle page JSON-LD: %d schemas" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                stype = data.get('@type','?')
                print("  #%d: %s" % (i+1, stype))
                if stype == 'FAQPage':
                    faqs = data.get('mainEntity', [])
                    print("    %d FAQ questions:" % len(faqs))
                    for q in faqs[:2]:
                        print("      - %s" % q.get('name','')[:50])
                elif stype == 'Article':
                    print("    headline: %s" % data.get('headline','')[:50])
                    print("    image: %s" % ('yes' if data.get('image') else 'no'))
                    print("    section: %s" % data.get('articleSection',''))
        except:
            print("  #%d: parse error" % (i+1))
    
    if 'GEO Structured Data' in body:
        print("\nGEO marker: PRESENT")

# Check homepage too
time.sleep(1)
req = urllib.request.Request("https://www.skillxm.cn/", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("\nHomepage JSON-LD: %d schemas" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                print("  #%d: %s" % (i+1, data.get('@type','?')))
        except:
            print("  #%d: error" % (i+1))

# Set WP Super Cache to auto-prune and not cache pages with query strings
print("\n=== Cache settings ===")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Disable WP Super Cache (we don't need it, it blocks our dynamic content)
cmd = "cd /www/wwwroot/resource_site && wp plugin deactivate wp-super-cache --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("WP Super Cache deactivated: %s" % stdout.read().decode().strip())

cmd = "cd /www/wwwroot/resource_site && wp option update wp_cache false --format=json --allow-root 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print("WP_CACHE: %s" % stdout.read().decode().strip())

ssh.close()
print("\nDone! Cache disabled, GEO data will be live.")
