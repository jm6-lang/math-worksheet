import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 测试Nginx+PHP-FPM ===\n")

# 1. 测试访问skycaiji的PHP
print("1. 通过Nginx访问skycaiji...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/index.php' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应长度:", len(content))
if "skycaiji" in content.lower() or "蓝天" in content:
    print("✓ 天空采集器!")
else:
    print(content[:300])

# 2. 检查nginx access log
print("\n2. Nginx access log...")
cmd = """tail -5 /var/log/nginx/access.log 2>/dev/null | tail -3"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 检查nginx error log for caiji
print("\n3. Nginx错误日志...")
cmd = """tail -10 /var/log/nginx/error.log 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 重新加载nginx配置
print("\n4. 重新加载nginx配置...")
stdin, stdout, stderr = ssh.exec_command("nginx -s reload 2>&1", timeout=10)
print(stdout.read().decode().strip() or "已重新加载")

# 5. 再次测试
print("\n5. 再次测试...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print(content[:300])

ssh.close()
