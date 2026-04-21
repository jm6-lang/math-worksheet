import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

cmd = """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -e "SELECT p.ID, LEFT(p.post_title,35) as title, CASE WHEN pm.meta_value IS NOT NULL THEN '✅有图' ELSE '❌无图' END as thumb FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key='_thumbnail_id' WHERE p.post_type='post' AND p.post_status='publish' ORDER BY p.ID DESC LIMIT 20;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
