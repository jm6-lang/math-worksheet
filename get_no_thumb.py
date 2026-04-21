import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

# Step 1: 用SQL直接查出没有缩略图的文章ID，写入文件
sql_cmds = [
    # 查无缩略图的文章ID
    """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "SELECT p.ID FROM wp_posts p LEFT JOIN wp_postmeta pm ON p.ID=pm.post_id AND pm.meta_key='_thumbnail_id' WHERE p.post_type='post' AND p.post_status='publish' AND pm.meta_value IS NULL ORDER BY p.ID DESC;" > /tmp/no_thumb_ids.txt 2>/dev/null""",
    # 看看结果
    "wc -l /tmp/no_thumb_ids.txt",
    "cat /tmp/no_thumb_ids.txt",
]
for cmd in sql_cmds:
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
    print(stdout.read().decode('utf-8', errors='ignore').strip())

ssh.close()
