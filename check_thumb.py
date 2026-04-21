import paramiko
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 先检查新采集的文章有没有缩略图
print("=== 检查最近文章缩略图状态 ===\n")
check_cmd = """cd /www/wwwroot/resource_site && wp post list --post_type=post --posts_per_page=10 --fields=ID,post_title,post_status --format=json --allow-root 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(check_cmd, timeout=30)
posts_raw = stdout.read().decode('utf-8', errors='ignore').strip()

if posts_raw:
    try:
        posts = json.loads(posts_raw)
        ids = [str(p['ID']) for p in posts]
        print("最近10篇文章ID: %s\n" % ", ".join(ids))
    except:
        print("Parse error: %s" % posts_raw[:200])
        ids = []
else:
    print("No output")
    ids = []

# 检查缩略图
for pid in ids[:10]:
    cmd = 'cd /www/wwwroot/resource_site && wp post meta get %s _thumbnail_id --allow-root 2>/dev/null' % pid
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    thumb = stdout.read().decode('utf-8', errors='ignore').strip()
    print("  Post %s: thumbnail_id = %s %s" % (pid, thumb if thumb else "(无)", "" if thumb else "← 需要配图"))

# 检查媒体库里有没有可用图片
print("\n=== 媒体库状态 ===")
cmd = 'cd /www/wwwroot/resource_site && wp media list --fields=ID,filename --format=json --orderby=id --order=desc --per_page=5 --allow-root 2>/dev/null'
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
media_raw = stdout.read().decode('utf-8', errors='ignore').strip()
print(media_raw[:500] if media_raw else "No media")

ssh.close()
