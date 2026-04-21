import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 创建SQL文件并执行 ===\n")

# 创建SQL文件
sql = """INSERT INTO skycaiji_release (task_id, name, module, addtime, config) VALUES (1, 'WordPress发布', 'wordpress', UNIX_TIMESTAMP(), '{"site_url":"https://skillxm.cn","api_token":"s6eW 2kHy 8yqu XNuY JjoK HHOR","post_type":"post","category_id":"7","post_status":"publish","author_id":1}');
"""

sftp = ssh.open_sftp()
with sftp.open('/tmp/insert_release.sql', 'w') as f:
    f.write(sql)
sftp.close()
print("1. SQL文件已创建")

# 执行SQL
print("\n2. 执行SQL...")
cmd = """mysql -u skycaiji -pSkyCaiJi2024! skycaiji < /tmp/insert_release.sql 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
result = stdout.read().decode().strip()
print(result if result else "执行成功")

# 检查结果
print("\n3. 检查发布配置...")
cmd = """mysql -u skycaiji -pSkyCaiJi2024! skycaiji -e "SELECT id, name, module FROM skycaiji_release;" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

# 更新任务配置
print("\n4. 更新任务配置...")
sql2 = """UPDATE skycaiji_task SET config='{"maxContent":5000,"minContent":100,"release_id":1,"rule_id":1}' WHERE id=1;"""
sftp = ssh.open_sftp()
with sftp.open('/tmp/update_task.sql', 'w') as f:
    f.write(sql2)
sftp.close()
cmd = """mysql -u skycaiji -pSkyCaiJi2024! skycaiji < /tmp/update_task.sql 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip() or "任务配置已更新")

ssh.close()

print("\n" + "="*50)
print("配置完成!")
print("="*50)
