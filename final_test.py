import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 最终测试 ===\n")

# 测试skycaiji
print("1. 测试skycaiji...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应长度:", len(content))
print(content[:500])

# 测试主站
print("\n2. 测试主站...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: www.skillxm.cn' 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应:", content[:200])

ssh.close()
