import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 通过sftp直接写脚本，避免shell转义地狱
script = '''#!/usr/bin/env python3
import subprocess, urllib.request, os, time

WP = "/www/wwwroot/resource_site"

IMAGES = [
    "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1461749280684-dccba630e2f6?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1559136555-9303baea8ebd?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1537432376149-e8937dfb6564?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1504639725590-34d0984388bd?w=800&h=500&fit=crop",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?w=800&h=500&fit=crop",
]

def dl(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            d = r.read()
            if len(d) < 5000: raise Exception("sm")
            with open(path, "wb") as f: f.write(d)
            return True
    except:
        try:
            fb = "https://placehold.co/800x500/2563eb/ffffff?text=Resource"
            req = urllib.request.Request(fb, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                with open(path, "wb") as f: f.write(r.read())
                return True
        except:
            return False

# 用WP-CLI查缺缩略图的文章
c = "cd %s && wp post list --post_type=post --post_status=publish --fields=ID --format=csv --allow-root 2>/dev/null" % WP
r = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=30)
lines = [x.strip() for x in r.stdout.strip().split(chr(10)) if x.strip() and x.strip() != "ID"]
print("Total published: %d" % len(lines))

need = []
for pid in lines:
    c2 = "cd %s && wp post meta get %s _thumbnail_id --allow-root 2>/dev/null" % (WP, pid)
    r2 = subprocess.run(c2, shell=True, capture_output=True, text=True, timeout=10)
    if not r2.stdout.strip():
        need.append(pid)

# Limit to latest 20
need = need[:20]
print("Need thumbnail: %d" % len(need))
if not need:
    print("All done!")
    exit(0)

ok = 0
for pid in need:
    url = IMAGES[int(pid) % len(IMAGES)]
    tmp = "/tmp/th_%s.jpg" % pid
    print("Post %s: " % pid, end="", flush=True)
    if dl(url, tmp):
        ci = 'cd %s && wp media import "%s" --porcelain --allow-root 2>/dev/null' % (WP, tmp)
        ri = subprocess.run(ci, shell=True, capture_output=True, text=True, timeout=30)
        mid = ri.stdout.strip()
        if mid.isdigit():
            ct = "cd %s && wp post meta update %s _thumbnail_id %s --allow-root 2>/dev/null" % (WP, pid, mid)
            subprocess.run(ct, shell=True, capture_output=True, timeout=10)
            print("OK media=%s" % mid)
            ok += 1
        else:
            print("FAIL %s" % ri.stdout[:40])
    else:
        print("DL FAIL")
    try: os.remove(tmp)
    except: pass
    time.sleep(1)

print("Done: %d/%d" % (ok, len(need)))
'''

sftp = ssh.open_sftp()
with sftp.open('/tmp/add_th.py', 'w') as f:
    f.write(script)
sftp.close()

print("=== 开始为12篇文章添加缩略图 ===\n")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/add_th.py 2>&1', timeout=600)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
