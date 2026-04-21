import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 测试不跟随重定向 ===\n")

# 不跟随重定向
print("1. 不跟随重定向测试...")
cmd = """curl -s --max-time 10 -o /dev/null -w '%{http_code} %{redirect_url}' 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("响应:", stdout.read().decode().strip())

# 直接测试index.php
print("\n2. 直接测试index.php...")
cmd = """curl -s --max-time 10 -o /dev/null -w '%{http_code} %{redirect_url}' 'http://127.0.0.1/index.php' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("响应:", stdout.read().decode().strip())

# 强制测试不带www
print("\n3. 测试不带www...")
cmd = """curl -s --max-time 10 -o /dev/null -w '%{http_code} %{redirect_url}' 'http://127.0.0.1/' -H 'Host: skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print("响应:", stdout.read().decode().strip())

# 检查skycaiji是否做了域名检查
print("\n4. 检查skycaiji重定向...")
cmd = """curl -sI --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null | head -10"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
print(stdout.read().decode().strip())

ssh.close()
