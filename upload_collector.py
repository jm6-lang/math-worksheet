import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 上传新采集器 ===\n")

# 读取新采集器
with open(r"C:\Users\Administrator\.qclaw\workspace-agent-3bb7b585\collector_v5.py", "r", encoding="utf-8") as f:
    new_collector = f.read()

# 备份旧版本
stdin, stdout, stderr = ssh.exec_command("cp /www/wwwroot/resource_site/auto_collect/collector.py /www/wwwroot/resource_site/auto_collect/collector_v4.py.bak", timeout=10)
print("旧版本已备份")

# 上传新采集器
sftp = ssh.open_sftp()
with sftp.open('/www/wwwroot/resource_site/auto_collect/collector.py', 'w') as f:
    f.write(new_collector)
sftp.close()
print("新采集器已上传")

# 验证语法
stdin, stdout, stderr = ssh.exec_command("python3 -m py_compile /www/wwwroot/resource_site/auto_collect/collector.py && echo '语法正确'", timeout=10)
print("语法检查:", stdout.read().decode().strip())

# 测试运行
print("\n测试采集器（2分钟）...")
stdin, stdout, stderr = ssh.exec_command("cd /www/wwwroot/resource_site/auto_collect && timeout 120 python3 collector.py 2>&1 | tail -80", timeout=150)
result = stdout.read().decode().strip()
print(result[-3000:] if len(result) > 3000 else result)

# 检查数据库
stdin, stdout, stderr = ssh.exec_command("sqlite3 /www/wwwroot/resource_site/auto_collect/published.db 'SELECT COUNT(*) FROM pub; SELECT MAX(created) FROM pub;'", timeout=10)
print("\n数据库状态:", stdout.read().decode().strip())

ssh.close()
