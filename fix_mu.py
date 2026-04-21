import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

sftp = ssh.open_sftp()

# Read current mu-plugin
with sftp.open('/www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php', 'r') as f:
    content = f.read().decode('utf-8')

# Fix: change priority from 1 to 99 (run AFTER Yoast so we append, not get overwritten)
# Also fix the top-level return issue
old_line = "if (is_admin()) return;"
new_line = "// if (is_admin()) return;  // removed: return at file level breaks mu-plugin"

if old_line in content:
    content = content.replace(old_line, new_line)
    print("Fixed: removed top-level return")

old_add = "add_action('wp_head', 'geo_ai_optimization', 1);"
new_add = "add_action('wp_head', 'geo_ai_optimization', 99);"

if old_add in content:
    content = content.replace(old_add, new_add)
    print("Fixed: priority 1 -> 99")
else:
    print("WARNING: add_action not found, searching...")
    if "add_action" in content:
        for line in content.split("\n"):
            if "add_action" in line:
                print("  Found: %s" % line.strip())

with sftp.open('/www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php', 'w') as f:
    f.write(content)

sftp.close()

# Verify syntax
stdin, stdout, stderr = ssh.exec_command(
    "php -l /www/wwwroot/resource_site/wp-content/mu-plugins/geo-optimization.php 2>&1",
    timeout=10
)
print("PHP syntax: %s" % stdout.read().decode().strip())

# Test
import urllib.request, re, json, time
time.sleep(1)
req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("JSON-LD count: %d" % len(schemas))
    
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                print("  #%d: %s" % (i+1, data.get('@type','?')))
                if data.get('@type') == 'FAQPage':
                    print("    FAQ: %d questions" % len(data.get('mainEntity', [])))
                elif data.get('@type') == 'Article':
                    print("    title: %s" % data.get('headline','')[:40])
        except:
            print("  #%d: error" % (i+1))
    
    meta_author = re.findall(r'name="author"', body)
    print("Meta author: %d" % len(meta_author))

ssh.close()
