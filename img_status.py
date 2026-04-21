import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

cmds = [
    ("媒体库图片数",
     "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null"),
    ("文章总数",
     "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"post\" AND post_status=\"publish\"' 2>/dev/null"),
    ("有缩略图文章数",
     "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_postmeta WHERE meta_key=\"_thumbnail_id\"' 2>/dev/null"),
    ("上传目录大小",
     "du -sh /www/wwwroot/resource_site/wp-content/uploads/ 2>/dev/null"),
    ("上传目录结构",
     "ls /www/wwwroot/resource_site/wp-content/uploads/ 2>/dev/null"),
]

for label, cmd in cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    print(f"{label}: {out}")

# Get a sample post content - extract just img src URLs
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT post_content FROM wp_posts WHERE post_type=\"post\" AND post_status=\"publish\" ORDER BY ID DESC LIMIT 1' 2>/dev/null",
    timeout=10
)
content = stdout.read().decode('utf-8', errors='replace')

# Extract image URLs
import re
img_pattern = r'src=["\']([^"\']+)["\']'
images = re.findall(img_pattern, content)
print(f"\n最近文章图片引用数: {len(images)}")
for img in images[:10]:
    print(f"  {img[:100]}")

# Check featured images
stdin, stdout, stderr = ssh.exec_command(
    "mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT pm.meta_value FROM wp_postmeta pm JOIN wp_posts p ON pm.post_id=p.ID WHERE pm.meta_key=\"_thumbnail_id\" AND p.post_type=\"post\" AND p.post_status=\"publish\" ORDER BY p.ID DESC LIMIT 1' 2>/dev/null",
    timeout=10
)
thumb_id = stdout.read().decode('utf-8', errors='replace').strip()
print(f"\n最新文章缩略图attachment ID: {thumb_id}")

if thumb_id.strip():
    stdin, stdout, stderr = ssh.exec_command(
        f"mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT guid FROM wp_posts WHERE ID={thumb_id.strip()}' 2>/dev/null",
        timeout=10
    )
    thumb_url = stdout.read().decode('utf-8', errors='replace').strip()
    print(f"缩略图URL: {thumb_url}")

ssh.close()
