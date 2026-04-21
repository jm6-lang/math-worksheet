import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 修复Nginx default_server问题 ===\n")

# 1. 禁用default站点
print("1. 禁用default站点...")
stdin, stdout, stderr = ssh.exec_command("rm -f /etc/nginx/sites-enabled/default && ls -la /etc/nginx/sites-enabled/", timeout=10)
print(stdout.read().decode().strip())

# 2. 重启Nginx
print("\n2. 重启Nginx...")
stdin, stdout, stderr = ssh.exec_command("nginx -t && nginx -s reload 2>&1", timeout=10)
print(stdout.read().decode().strip())

# 3. 测试采集器
print("\n3. 测试采集器...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应长度:", len(content))
if len(content) > 1000:
    print("✓ 可能成功!")
    print(content[:500])
else:
    print(content)

ssh.close()
