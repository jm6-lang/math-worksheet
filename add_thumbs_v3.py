import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 用heredoc方式写脚本，避免引号问题
write_script = """cat > /tmp/add_thumbs.py << 'PYEOF'
#!/usr/bin/env python3
import subprocess, urllib.request, os, time

WP_PATH = "/www/wwwroot/resource_site"
DB_PASS = "gMshA29CshK5"

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

def download(url, path):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            if len(data) < 5000:
                raise Exception("too small")
            with open(path, "wb") as f:
                f.write(data)
            return True
    except:
        try:
            fb = "https://placehold.co/800x500/2563eb/ffffff?text=Resource"
            req = urllib.request.Request(fb, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as r:
                with open(path, "wb") as f:
                    f.write(r.read())
                return True
        except:
            return False

sql = "SELECT p.ID FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key='_thumbnail_id' WHERE p.post_type='post' AND p.post_status='publish' AND pm.meta_value IS NULL ORDER BY p.ID DESC LIMIT 20"
cmd = "mysql -u wp_user -p'%s' wp_skillxm -N -e '%s' 2>/dev/null" % (DB_PASS, sql)
r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
ids = [x.strip() for x in r.stdout.strip().split("\\n") if x.strip()]
print("Need thumbs: %d" % len(ids))

ok = 0
for i, pid in enumerate(ids):
    url = IMAGES[int(pid) % len(IMAGES)]
    tmp = "/tmp/th_%s.jpg" % pid
    print("Post %s: " % pid, end="", flush=True)
    if download(url, tmp):
        c = 'cd %s && wp media import "%s" --porcelain --allow-root 2>/dev/null' % (WP_PATH, tmp)
        r2 = subprocess.run(c, shell=True, capture_output=True, text=True, timeout=30)
        mid = r2.stdout.strip()
        if mid.isdigit():
            c2 = "cd %s && wp post meta update %s _thumbnail_id %s --allow-root 2>/dev/null" % (WP_PATH, pid, mid)
            subprocess.run(c2, shell=True, capture_output=True, timeout=10)
            print("OK media=%s" % mid)
            ok += 1
        else:
            print("FAIL %s" % r2.stdout[:40])
    else:
        print("DL FAIL")
    try: os.remove(tmp)
    except: pass
    time.sleep(1)

print("Done: %d/%d" % (ok, len(ids)))
PYEOF"""

stdin, stdout, stderr = ssh.exec_command(write_script, timeout=10)
err = stderr.read().decode('utf-8', errors='ignore')
if err:
    print("Write err:", err[:200])

print("=== 开始添加缩略图 ===\n")
stdin, stdout, stderr = ssh.exec_command('/usr/bin/python3 /tmp/add_thumbs.py 2>&1', timeout=600)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

ssh.close()
