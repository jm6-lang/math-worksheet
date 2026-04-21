import paramiko
import sys

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查WP-CLI命令 ===\n")

# 检查wp-cli帮助
print("1. WP-CLI application-password命令帮助...")
cmd = """cd /www/wwwroot/resource_site && wp help user application-password create 2>&1 | head -40"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

ssh.close()
