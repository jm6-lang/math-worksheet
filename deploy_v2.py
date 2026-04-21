import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
sftp = ssh.open_sftp()

# 上传v2脚本
local = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\rewrite_v2.py'
remote = '/www/wwwroot/resource_site/auto_collect/rewrite_v2.py'
sftp.put(local, remote)
sftp.close()
print("Uploaded rewrite_v2.py")

# 先跑3篇测试
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 auto_collect/rewrite_v2.py 0 3 2>&1",
    timeout=30
)
print(stdout.read().decode('utf-8', errors='ignore'))

# 验证内容质量
stdin, stdout, stderr = ssh.exec_command(
    """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
    SELECT post_title, LENGTH(post_content) FROM wp_posts WHERE ID=27;
    " 2>/dev/null""",
    timeout=10
)
print("验证: %s" % stdout.read().decode('utf-8', errors='ignore'))

# 显示第一篇文章的前500字
stdin, stdout, stderr = ssh.exec_command(
    """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
    SELECT LEFT(post_content, 800) FROM wp_posts WHERE ID=27;
    " 2>/dev/null""",
    timeout=10
)
content = stdout.read().decode('utf-8', errors='ignore')
# 去掉\n换行显示
content = content.replace('\\n', '\n')
print("\n=== 文章ID=27内容预览 ===")
print(content)

ssh.close()
