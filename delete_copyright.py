import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Delete posts 1814, 1816, 1818, 1820 and their thumbnails + media
delete_ids = [1814, 1816, 1818, 1820]
thumb_ids = [1815, 1817, 1819, 1821]

for pid in delete_ids:
    # Delete post meta
    stdin, stdout, stderr = ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_postmeta WHERE post_id=%d;\" 2>/dev/null" % pid,
        timeout=10
    )
    
    # Delete post
    stdin, stdout, stderr = ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_posts WHERE ID=%d;\" 2>/dev/null" % pid,
        timeout=10
    )
    
    print("Deleted post %d" % pid)

# Delete thumbnail media entries
for mid in thumb_ids:
    stdin, stdout, stderr = ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_postmeta WHERE post_id=%d;\" 2>/dev/null" % mid,
        timeout=10
    )
    stdin, stdout, stderr = ssh.exec_command(
        "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"DELETE FROM wp_posts WHERE ID=%d;\" 2>/dev/null" % mid,
        timeout=10
    )
    print("Deleted media %d" % mid)

# Remove from published.json cache
stdin, stdout, stderr = ssh.exec_command(
    "cat /www/wwwroot/resource_site/auto_collect/published.json", timeout=10
)
import json
try:
    urls = json.loads(stdout.read().decode())
    print("\nCache before: %d URLs" % len(urls))
except:
    urls = []

# Also check woshipm RSS entries that were deleted
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 -c \""
    "import feedparser; f=feedparser.parse('https://www.woshipm.com/feed', request_headers={'User-Agent':'Mozilla/5.0'}); "
    "print(len(f.entries)); [print(e.get('link','')) for e in f.entries[:5]]\" 2>/dev/null",
    timeout=15
)
rss_urls = stdout.read().decode('utf-8', errors='ignore').strip().split('\n')[1:]  # skip count line

# Filter out woshipm URLs from cache
filtered = [u for u in urls if not any(u.startswith('https://www.woshipm.com') for _ in [1]) 
            and not any('woshipm' in u for _ in [1])]
# Actually let's just remove the specific URLs
kept = []
for u in urls:
    if 'woshipm.com' not in u:
        kept.append(u)
    else:
        print("Removed from cache: %s" % u[:80])

sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/published.json', 'w') as f:
    f.write(json.dumps(kept, ensure_ascii=False))
sftp.close()
print("\nCache after: %d URLs" % len(kept))

# Verify remaining posts
stdin, stdout, stderr = ssh.exec_command(
    """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "SELECT ID, LEFT(post_title,40) as title FROM wp_posts WHERE ID IN (1812,1814,1816,1818,1820,1822) AND post_status='publish';" 2>/dev/null""",
    timeout=10
)
print("\nRemaining published:")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
