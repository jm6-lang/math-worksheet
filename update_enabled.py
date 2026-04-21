import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 更新启用的配置 ===\n")

# 1. 复制新配置到启用目录
print("1. 复制配置...")
cmd = """cp /etc/nginx/sites-available/resource_site.conf /etc/nginx/sites-enabled/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip() or "已复制")

# 2. 验证
print("\n2. 验证...")
cmd = """grep "caiji" /etc/nginx/sites-enabled/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip() or "未找到caiji配置")

# 3. 测试nginx
print("\n3. 测试nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -t 2>&1", timeout=10)
print(stdout.read().decode().strip())

# 4. 重载nginx
print("\n4. 重载nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1", timeout=10)
print(stdout.read().decode().strip() or "已重载")

# 5. 测试
print("\n5. 测试caiji...")
cmd = """curl -sI --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

ssh.close()
