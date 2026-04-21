import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 查看天空采集器日志 ===\n")

# 检查日志
cmd = """ls -la /www/wwwroot/skycaiji/runtime/log/"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 查看最新日志
cmd = """find /www/wwwroot/skycaiji/runtime/log -name "*.log" -exec tail -30 {} \\;"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
log = stdout.read().decode('utf-8', errors='ignore').strip()
print("\n日志内容:")
print(log[-2000:] if len(log) > 2000 else log)

ssh.close()
