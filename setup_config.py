import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 配置天空采集器数据库 ===\n")

# 1. 查看配置文件模板
print("1. 查看配置模板...")
cmd = """cat /www/wwwroot/skycaiji/vendor/skycaiji/app/install/data/config.php"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
config_template = stdout.read().decode().strip()
print(config_template)

# 2. 查看安装类
print("\n2. 查看安装类...")
cmd = """ls -la /www/wwwroot/skycaiji/vendor/skycaiji/app/install/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 查看入口文件
print("\n3. 查看public/index.php...")
cmd = """cat /www/wwwroot/skycaiji/public/index.php"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 4. 访问网站获取安装向导
print("\n4. 尝试访问安装向导...")
cmd = """curl -sL --max-time 10 'http://localhost/' 2>/dev/null | head -100"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore').strip()
print(content[:500])

ssh.close()
