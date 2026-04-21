import paramiko
import sys
import requests
import base64

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 创建WordPress应用密码 ===\n")

# 使用WP-CLI创建应用密码（加--allow-root）
print("1. 创建应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password create admin 1 "Auto-Collect" --allow-root --format=json 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:800])

# 如果成功，提取token
if "password" in result.lower():
    print("\n应用密码创建成功!")
    # 解析JSON获取密码
    import json
    try:
        data = json.loads(result)
        new_token = data.get('password', '')
        print(f"新Token: {new_token}")
    except:
        print("无法解析密码，请手动查看上方输出")
else:
    print("\n需要WordPress管理员密码来创建应用密码")

# 检查WordPress配置获取密码
print("\n2. 检查WordPress配置...")
cmd = """grep "WP_USER\|WP_PASS\|ADMIN_PASS" /www/wwwroot/resource_site/wp-config.php 2>/dev/null | head -5"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=10)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:200])

ssh.close()
