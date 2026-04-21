import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Restart PHP-FPM to clear opcache
print("Restarting PHP-FPM...")
stdin, stdout, stderr = ssh.exec_command("systemctl restart php8.1-fpm 2>&1", timeout=15)
print("PHP-FPM: %s" % stdout.read().decode().strip())
err = stderr.read().decode().strip()
if err:
    print("Error: %s" % err)

# Also restart nginx
stdin, stdout, stderr = ssh.exec_command("systemctl restart nginx 2>&1", timeout=15)
print("Nginx: %s" % stdout.read().decode().strip())

# Check if mu-plugin is loaded
cmd = "cd /www/wwwroot/resource_site && php -r \"define('ABSPATH','/www/wwwroot/resource_site/'); require_once '/www/wwwroot/resource_site/wp-load.php'; if(function_exists('geo_add_structured_data')) echo 'GEO FUNCTION LOADED'; else echo 'NOT LOADED';\" 2>&1"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("PHP check: %s" % stdout.read().decode('utf-8', errors='ignore'))

ssh.close()

# Test after restart
import time, urllib.request, re, json
time.sleep(2)
req = urllib.request.Request("https://www.skillxm.cn/?p=1812", headers={"User-Agent": "Mozilla/5.0"})
with urllib.request.urlopen(req, timeout=10) as r:
    body = r.read().decode('utf-8', errors='ignore')
    
    # Check for GEO comment
    if 'GEO Structured Data' in body:
        print("GEO marker FOUND in page!")
    else:
        print("GEO marker NOT found")
    
    schemas = re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', body, re.DOTALL)
    print("Total JSON-LD: %d" % len(schemas))
    for i, s in enumerate(schemas):
        try:
            data = json.loads(s)
            if '@graph' in data:
                print("  #%d: @graph (%d items)" % (i+1, len(data['@graph'])))
            else:
                stype = data.get('@type','?')
                print("  #%d: %s" % (i+1, stype))
                if stype == 'FAQPage':
                    print("    %d FAQ questions" % len(data.get('mainEntity',[])))
                elif stype == 'Article':
                    print("    headline: %s" % data.get('headline','')[:50])
        except:
            print("  #%d: error" % (i+1))
