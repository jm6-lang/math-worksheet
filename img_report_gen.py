import paramiko
import json

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Run checks and write to a JSON file
checks = [
    ("mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"attachment\" AND post_mime_type LIKE \"image/%%\"' 2>/dev/null"),
    ("mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_posts WHERE post_type=\"post\" AND post_status=\"publish\"' 2>/dev/null"),
    ("mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT COUNT(*) FROM wp_postmeta WHERE meta_key=\"_thumbnail_id\"' 2>/dev/null"),
    "du -sh /www/wwwroot/resource_site/wp-content/uploads/ 2>/dev/null",
    "ls /www/wwwroot/resource_site/wp-content/uploads/ 2>/dev/null",
]

labels = ["media_images", "total_posts", "posts_with_thumb", "uploads_size", "uploads_folders"]
results = {}

for label, cmd in zip(labels, checks):
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
    out = stdout.read().decode('utf-8', errors='replace').strip()
    results[label] = out

# Write results to file
with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\img_report.txt', 'w', encoding='utf-8') as f:
    f.write(json.dumps(results, ensure_ascii=False, indent=2))

# Check latest post image situation
cmd = """mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT pm.meta_value FROM wp_postmeta pm JOIN wp_posts p ON pm.post_id=p.ID WHERE pm.meta_key="_thumbnail_id" AND p.post_type="post" AND p.post_status="publish" ORDER BY p.ID DESC LIMIT 1' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
thumb_id = stdout.read().decode('utf-8', errors='replace').strip()

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\img_report.txt', 'a', encoding='utf-8') as f:
    f.write(f"\nLatest post thumbnail attachment ID: {thumb_id}")
    if thumb_id.strip():
        cmd2 = f"mysql -u wpuser -p'WpPass2024!' wp_skillxm -e 'SELECT guid FROM wp_posts WHERE ID={thumb_id.strip()}' 2>/dev/null"
        stdin2, stdout2, stderr2 = ssh.exec_command(cmd2, timeout=10)
        thumb_url = stdout2.read().decode('utf-8', errors='replace').strip()
        f.write(f"\nThumbnail URL: {thumb_url}")

ssh.close()
print("Done. Results written to img_report.txt")
