import paramiko
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 检查用户权限 ===\n")

# 检查admin用户
print("1. 检查admin用户权限...")
cmd = """cd /www/wwwroot/resource_site && wp user get admin --allow-root --fields=user_email,roles,capabilities 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore'))

# 检查REST API权限
print("\n2. 检查REST API状态...")
cmd = """curl -s "https://skillxm.cn/wp-json/wp/v2/" -H "Authorization: Bearer 1f72ufzyMhKTDUk8E45Q19v4" 2>/dev/null | head -50"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
print(stdout.read().decode('utf-8', errors='ignore')[:500])

# 检查用户ID
print("\n3. 获取用户ID...")
cmd = """curl -s "https://skillxm.cn/wp-json/wp/v2/users?search=admin" -H "Authorization: Bearer 1f72ufzyMhKTDUk8E45Q19v4" 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:500])

# 用用户ID发布
print("\n4. 用admin用户发布...")
# admin用户通常是ID=1
test_post = {
    "title": "Test API",
    "content": "<p>Test</p>",
    "status": "publish",
    "author": 1
}

headers = {
    "Authorization": "Bearer 1f72ufzyMhKTDUk8E45Q19v4",
    "Content-Type": "application/json"
}

r = requests.post("https://skillxm.cn/wp-json/wp/v2/posts", headers=headers, json=test_post, timeout=30, verify=False)
print(f"Status: {r.status_code}")
print(r.text[:300])

ssh.close()
