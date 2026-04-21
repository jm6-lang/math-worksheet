import paramiko
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 测试发布（不指定author） ===\n")

# 使用admin用户(ID=3)的应用密码
token = "BTGVTIxFjxjgKvJ7Fvm2lYxm"

print("1. 测试发布文章...")
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 不指定author，让系统自动使用应用密码关联的用户
test_post = {
    "title": "API Test - Admin User",
    "content": "<p>测试文章，使用admin用户发布。</p>",
    "status": "publish",
    "categories": [7]
}

r = requests.post("https://skillxm.cn/wp-json/wp/v2/posts", headers=headers, json=test_post, timeout=30, verify=False)
print(f"Status: {r.status_code}")

if r.status_code in [200, 201]:
    data = r.json()
    print(f"Success!")
    print(f"Post ID: {data.get('id')}")
    print(f"Link: {data.get('link')}")
    print(f"Author: {data.get('author')}")
else:
    print(f"Failed: {r.text}")

# 再试试admin(ID=3)的token
print("\n2. 检查admin(ID=3)的token...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password list admin --format=json --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:500])

ssh.close()
