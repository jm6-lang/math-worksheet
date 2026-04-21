import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查所有Nginx配置 ===\n")

# 1. 检查所有启用的站点
print("1. 已启用的站点...")
cmd = """ls -la /etc/nginx/sites-enabled/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 2. 检查Nginx主配置
print("\n2. Nginx主配置...")
cmd = """grep -r "include" /etc/nginx/nginx.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 检查default站点
print("\n3. default站点...")
cmd = """cat /etc/nginx/sites-available/default 2>/dev/null | head -30"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 检查skycaiji public目录
print("\n4. skycaiji public目录...")
cmd = """ls -la /www/wwwroot/skycaiji/public/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 5. 直接测试PHP-FPM
print("\n5. 直接测试skycaiji index.php...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/index.php' -H 'Host: caiji.skillxm.cn' 2>/dev/null | head -50"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应长度:", len(content))
print(content[:500])

# 6. 检查是否有.htaccess重定向
print("\n6. 检查.htaccess...")
cmd = """cat /www/wwwroot/skycaiji/public/.htaccess 2>/dev/null || echo "无.htaccess" """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 7. 检查WordPress是否在处理/caiji路径
print("\n7. 检查WordPress是否拦截...")
cmd = """curl -sL --max-time 5 'http://127.0.0.1/caiji/' -H 'Host: www.skillxm.cn' 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
