import paramiko
import sys
import requests
import json

sys.stdout.reconfigure(encoding='utf-8')

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('43.103.5.46', username='root', password='Langlang0.', timeout=15)

print("=== 为用户1创建应用密码 ===\n")

# 为用户lang64875527创建应用密码
print("1. 为用户1创建应用密码...")
cmd = """cd /www/wwwroot/resource_site && wp user application-password create lang64875527 "API-Auto" --porcelain --allow-root 2>&1"""
stdin, stdout, stderr = ssh.exec_command(cmd, timeout=30)
result = stdout.read().decode('utf-8', errors='ignore').strip()
print(f"Token: {result}")

if result and len(result) > 10:
    new_token = result
    
    # 测试API
    print("\n2. 测试发布...")
    headers = {
        "Authorization": f"Bearer {new_token}",
        "Content-Type": "application/json"
    }
    
    test_post = {
        "title": "API Test - Collector Working",
        "content": "<p>This article was posted using WordPress REST API.</p>",
        "status": "publish",
        "author": 1
    }
    
    r = requests.post("https://skillxm.cn/wp-json/wp/v2/posts", headers=headers, json=test_post, timeout=30, verify=False)
    print(f"Status: {r.status_code}")
    
    if r.status_code in [200, 201]:
        data = r.json()
        print(f"Success! Post ID: {data.get('id')}")
        print(f"Link: {data.get('link')}")
        
        # 保存新Token到文件
        print("\n3. 保存Token...")
        with open('C:\\Users\\Administrator\\.qclaw\\workspace-agent-3bb7b585\\api_token.txt', 'w') as f:
            f.write(new_token)
        print(f"Token saved: {new_token}")
    else:
        print(f"Failed: {r.text[:300]}")

ssh.close()
