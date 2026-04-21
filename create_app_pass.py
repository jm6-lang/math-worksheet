import paramiko
import requests
import json
import base64

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

sys.stdout.reconfigure(encoding='utf-8')
print("=== 创建WordPress应用密码 ===\n")

# 1. 获取WordPress Nonce
print("1. 获取Nonce...")
cmd = """curl -s "https://skillxm.cn/wp-admin/admin-ajax.php?action=application_passwords_create_request" -c /tmp/cookies.txt -b /tmp/cookies.txt 2>/dev/null"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:200] if result else "无响应")

# 2. 直接使用WP-CLI创建应用密码
print("\n2. 使用WP-CLI创建应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password create admin 1 "API-Auto" --format=json 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore')
print(result[:500])

ssh.close()

# 3. 本地测试
print("\n3. 本地测试API...")
# 生成新的应用密码
new_token = "NewToken123"

# 直接使用用户名密码认证
auth = base64.b64encode(b"admin:Password123").decode()
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json"
}

# 测试发布
test_post = {
    "title": "测试文章",
    "content": "<p>这是一篇测试文章</p>",
    "status": "publish",
    "categories": [7]
}

try:
    response = requests.post(
        "https://skillxm.cn/wp-json/wp/v2/posts",
        headers=headers,
        json=test_post,
        timeout=30,
        verify=False
    )
    print(f"响应: {response.status_code}")
    print(response.text[:500])
except Exception as e:
    print(f"错误: {e}")
