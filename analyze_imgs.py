import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=10)

# Check a few sample posts - how many have img tags
cmd = """mysql -u wpuser -p'WpPass2024!' wp_skillxm -e '
SELECT ID, post_title, LENGTH(post_content) as len,
  (LENGTH(post_content) - LENGTH(REPLACE(post_content, "<img", ""))) as img_count
FROM wp_posts 
WHERE post_type="post" AND post_status="publish" 
ORDER BY ID DESC LIMIT 10' 2>/dev/null"""

stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
result = stdout.read().decode('utf-8', errors='replace')

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\sample_posts.txt', 'w', encoding='utf-8') as f:
    f.write(result)

# Count total posts with img tags
cmd2 = """mysql -u wpuser -p'WpPass2024!' wp_skillxm -e '
SELECT 
  SUM(CASE WHEN post_content LIKE "%<img%" THEN 1 ELSE 0 END) as with_img,
  SUM(CASE WHEN post_content NOT LIKE "%<img%" THEN 1 ELSE 0 END) as no_img
FROM wp_posts WHERE post_type="post" AND post_status="publish"' 2>/dev/null"""

stdin2, stdout2, stderr2 = ssh.exec_command(cmd2, timeout=10)
result2 = stdout2.read().decode('utf-8', errors='replace')

with open(r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\img_stats.txt', 'w', encoding='utf-8') as f:
    f.write(result2)
    f.write("\n\n--- sample posts ---\n")
    f.write(result)

ssh.close()
print("done")
