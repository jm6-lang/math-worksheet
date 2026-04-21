import paramiko
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)

# Delete remaining posts and their media
delete_ids = [1818, 1820]
thumb_ids = [1819, 1821]

for pid in delete_ids:
    ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_postmeta WHERE post_id=%d;\" 2>/dev/null" % pid,
        timeout=10
    )
    ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_posts WHERE ID=%d;\" 2>/dev/null" % pid,
        timeout=10
    )
    print("Deleted post %d" % pid)

for mid in thumb_ids:
    ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_postmeta WHERE post_id=%d;\" 2>/dev/null" % mid,
        timeout=10
    )
    ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_posts WHERE ID=%d;\" 2>/dev/null" % mid,
        timeout=10
    )
    print("Deleted media %d" % mid)

# Update published.json - remove woshipm URLs
import time
time.sleep(1)
stdin, stdout, stderr = ssh.exec_command("cat /www/wwwroot/resource_site/auto_collect/published.json", timeout=10)
try:
    urls = json.loads(stdout.read().decode())
except:
    urls = []

kept = [u for u in urls if 'woshipm.com' not in u]
removed = len(urls) - len(kept)

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/published.json', 'w') as f:
    f.write(json.dumps(kept, ensure_ascii=False))
sftp.close()
print("\nRemoved %d woshipm URLs from cache, %d remaining" % (removed, len(kept)))

# Verify
time.sleep(1)
stdin, stdout, stderr = ssh.exec_command(
    """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "SELECT ID, LEFT(post_title,40) as title FROM wp_posts WHERE ID IN (1812,1814,1816,1818,1820,1822) AND post_status='publish';" 2>/dev/null""",
    timeout=10
)
print("\nRemaining:")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
