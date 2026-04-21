import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 检查配置结构 ===\n")

# 查找配置文件
print("1. 查找配置文件...")
cmd = """find /www/wwwroot/skycaiji -name "*.php" -path "*/config/*" | head -20"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 查看vendor目录下的配置
print("\n2. vendor/skycaiji目录...")
cmd = """ls -la /www/wwwroot/skycaiji/vendor/skycaiji/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 查看app/config
print("\n3. app/config...")
cmd = """ls -la /www/wwwroot/skycaiji/vendor/skycaiji/app/config/ 2>/dev/null || find /www/wwwroot/skycaiji -name "config.php" | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 查看install目录
print("\n4. install目录...")
cmd = """find /www/wwwroot/skycaiji -type d -name "install" """
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 查看runtime目录
print("\n5. runtime目录...")
cmd = """ls -la /www/wwwroot/skycaiji/runtime/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

ssh.close()
