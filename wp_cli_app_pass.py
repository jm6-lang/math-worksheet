import paramiko
import sys
import requests
import base64

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 创建WordPress应用密码 ===\n")

# 使用WP-CLI创建应用密码
print("1. 使用WP-CLI创建应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password create admin 1 "API-Auto" --format=json 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result)

# 检查是否成功
if "uuid" in result or "password" in result.lower():
    print("\n应用密码创建成功!")
else:
    print("\n应用密码创建可能失败，尝试另一种方法...")

ssh.close()

# 本地使用Basic Auth测试
print("\n2. 测试Basic Auth...")
auth = base64.b64encode(b"admin:YourPassword").decode()
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

test_post = {
    "title": "Test Post",
    "content": "<p>Test</p>",
    "status": "publish"
}

try:
    r = requests.post("https://skillxm.cn/wp-json/wp/v2/posts", headers=headers, json=test_post, timeout=30, verify=False)
    print(f"Status: {r.status_code}")
    print(r.text[:300])
except Exception as e:
    print(f"Error: {e}")
