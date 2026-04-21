import paramiko, sys
sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
sftp = ssh.open_sftp()

# 上传脚本
local = r'C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\rewrite_articles.py'
remote = '/www/wwwroot/resource_site/auto_collect/rewrite_articles.py'
sftp.put(local, remote)
print("Uploaded: %s" % remote)

# 检查pymysql
stdin, stdout, stderr = ssh.exec_command("python3 -c 'import pymysql; print(pymysql.__version__)' 2>&1", timeout=10)
result = stdout.read().decode().strip()
if 'ModuleNotFoundError' in result:
    print("Installing pymysql...")
    stdin, stdout, stderr = ssh.exec_command("pip3 install pymysql -q 2>&1", timeout=30)
    print(stdout.read().decode().strip())
else:
    print("pymysql: %s" % result)

# 先跑3篇测试
print("\n=== 测试运行 (3篇) ===")
stdin, stdout, stderr = ssh.exec_command(
    "cd /www/wwwroot/resource_site && python3 auto_collect/rewrite_articles.py 0 3 2>&1",
    timeout=30
)
output = stdout.read().decode('utf-8', errors='ignore')
print(output)

sftp.close()

# 如果成功，验证第一篇的内容
if 'OK' in output:
    print("\n=== 验证第一篇文章内容 ===")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=30)
    stdin, stdout, stderr = ssh.exec_command(
        """mysql -u wp_user -p'gMshA29CshK5' wp_skillxm -N -e "
        SELECT post_title, LEFT(post_content, 500) FROM wp_posts WHERE post_type='post' AND post_status='publish' ORDER BY ID ASC LIMIT 1;
        " 2>/dev/null""",
        timeout=10
    )
    print(stdout.read().decode('utf-8', errors='ignore'))
    ssh.close()
