import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

script = '''#!/usr/bin/env python3
import subprocess, urllib.request, os, time

WP = "/www/wwwroot/resource_site"
# 只处理 1785 这篇
pid = "1785"
IMAGES = [
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",
]

def dl(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as r:
            d = r.read()
            if len(d) < 5000: raise Exception("sm")
            with open(path, "wb") as f: f.write(d)
            return True
    except:
        return False

tmp = "/tmp/th_%s.jpg" % pid
print("Retry Post %s: " % pid, end="", flush=True)
if dl(IMAGES[0], tmp):
    ci = 'cd %s && wp media import "%s" --porcelain --allow-root 2>/dev/null' % (WP, tmp)
    ri = subprocess.run(ci, shell=True, capture_output=True, text=True, timeout=30)
    mid = ri.stdout.strip()
    if mid.isdigit():
        ct = "cd %s && wp post meta update %s _thumbnail_id %s --allow-root 2>/dev/null" % (WP, pid, mid)
        subprocess.run(ct, shell=True, capture_output=True, timeout=10)
        print("OK media=%s" % mid)
    else:
        print("FAIL: '%s'" % ri.stdout[:60])
else:
    print("DL FAIL")

try: os.remove(tmp)
except: pass
'''

sftp = ssh.open_sftp()
with sftp.open('/tmp/fix_th.py', 'w') as f:
    f.write(script)
sftp.close()

print("补处理1785...")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/fix_th.py 2>&1', timeout=60)
print(stdout.read().decode('utf-8', errors='ignore'))

# 验证
cmd = "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e \"SELECT p.ID, pm.meta_value as thumb FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key='_thumbnail_id' WHERE p.ID BETWEEN 1777 AND 1788 ORDER BY p.ID DESC;\" 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("\n验证缩略图状态:")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
