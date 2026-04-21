import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')

print("=== 调试Nginx配置 ===\n")

# 1. 查看完整配置
print("1. 查看Nginx配置...")
cmd = """cat /etc/nginx/sites-available/resource_site.conf"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
config = stdout.read().decode().strip()
print(config)

# 2. 测试本机解析
print("\n2. 测试本机解析...")
cmd = """echo "127.0.0.1 caiji.skillxm.cn" >> /etc/hosts && cat /etc/hosts | grep caiji"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
print(stdout.read().decode().strip())

# 3. 直接测试
print("\n3. 直接访问skycaiji目录...")
cmd = """curl -sL --max-time 10 'http://127.0.0.1/' -H 'Host: caiji.skillxm.cn' 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=15)
content = stdout.read().decode('utf-8', errors='ignore')
print("响应长度:", len(content))
if "skycaiji" in content.lower() or "天空" in content or "采集" in content:
    print("✓ 天空采集器页面!")
    print(content[:1000])
elif "Page not found" in content or "首页" in content:
    print("✗ 返回主站页面")
    print(content[:500])
else:
    print(content[:500])

ssh.close()
