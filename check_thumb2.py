import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# 直接SQL查
cmd = "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT COUNT(*) as total, SUM(CASE WHEN pm.meta_value IS NULL THEN 1 ELSE 0 END) as no_thumb FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key='_thumbnail_id' WHERE p.post_type='post' AND p.post_status='publish';\" 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("总览:", stdout.read().decode('utf-8', errors='ignore').strip())

# 查最近5篇有无缩略图
cmd2 = "mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e \"SELECT p.ID, LEFT(p.post_title,40) as title, pm.meta_value as thumb FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key='_thumbnail_id' WHERE p.post_type='post' AND p.post_status='publish' ORDER BY p.ID DESC LIMIT 15;\" 2>/dev/null"
stdin, stdout, stderr = ssh.exec_command(cmd2, timeout=15)
print("\n最近15篇:")
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
